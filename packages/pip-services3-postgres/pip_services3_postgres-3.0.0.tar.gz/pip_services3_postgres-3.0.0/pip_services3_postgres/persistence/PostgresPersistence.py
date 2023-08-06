# -*- coding: utf-8 -*-

import random

from pip_services3_commons.config import IConfigurable, ConfigParams
from pip_services3_commons.convert import LongConverter
from pip_services3_commons.data import PagingParams, DataPage
from pip_services3_commons.errors import InvalidStateException, ConnectionException
from pip_services3_commons.refer import IReferenceable, IUnreferenceable, IReferences, DependencyResolver
from pip_services3_commons.run import IOpenable, ICleanable
from pip_services3_components.log import CompositeLogger
from psycopg2 import ProgrammingError

from pip_services3_postgres.persistence.PostgresConnection import PostgresConnection


class PostgresPersistence(IReferenceable, IUnreferenceable, IConfigurable, IOpenable, ICleanable):
    """
    Abstract persistence component that stores data in PostgreSQL using plain driver.

    This is the most basic persistence component that is only
    able to store data items of any type. Specific CRUD operations
    over the data items must be implemented in child classes by
    accessing **self._db** or **self._collection** properties.

    ### Configuration parameters ###
        - collection:                  (optional) Postgres collection name
        - connection(s):
            - discovery_key:             (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>`
            - host:                      host name or IP address
            - port:                      port number (default: 27017)
            - uri:                       resource URI or connection string with all parameters in it
        - credential(s):
            - store_key:                 (optional) a key to retrieve the credentials from :class:`ICredentialStore <pip_services3_components.auth.ICredentialStore.ICredentialStore>`
            - username:                  (optional) user name
            - password:                  (optional) user password
        - options:
            - connect_timeout:      (optional) number of milliseconds to wait before timing out when connecting a new client (default: 0)
            - idle_timeout:         (optional) number of milliseconds a client must sit idle in the pool and not be checked out (default: 10000)
            - max_pool_size:        (optional) maximum number of clients the pool should contain (default: 10)

    ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>` components to pass log messages components to pass log messages
        - `*:discovery:*:*:1.0`        (optional) :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>` services
        - `*:credential-store:*:*:1.0` (optional) :class:`ICredentialStore <pip_services3_components.auth.ICredentialStore.ICredentialStore>` stores to resolve credentials

    Example:

    .. code-block:: python

        class MyPostgresPersistence(PostgresPersistence):

            def __init__(self):
                super(MyPostgresPersistence, self).__init__('mydata')

            def get_by_name(self, correlation_id, name):
                criteria = {'name': name}
                return self._model.find_one(criteria)

            def set(self, correlation_id, item):
                criteria = {'name': item['name']}
                options = { 'upsert': True, 'new': True }
                return self._model.find_one_and_update(criteria, item, options)

        persistence = MyPostgresPersistence()
        persistence.configure(ConfigParams.from_tuples(
            "host", "localhost",
            "port", 27017
        ))

        persistence.open("123")
        persistence.set("123", {'name': "ABC"})

        item = persistence.get_by_name("123", "ABC")
        print(item) # Result: { 'name': "ABC" }

    """

    _default_config = ConfigParams.from_tuples(
        "collection", None,
        "dependencies.connection", "*:connection:postgres:*:1.0",

        # connections.*
        # credential.*

        "options.max_pool_size", 2,
        "options.keep_alive", 1,
        "options.connect_timeout", 5000,
        "options.auto_reconnect", True,
        "options.max_page_size", 100,
        "options.debug", True
    )

    def __init__(self, table_name):
        """
        Creates a new instance of the persistence component.

        :param table_name: (optional) a table name.
        """
        # The PostgreSQL table object.
        self._table_name = table_name

        self.__config: ConfigParams = None
        self.__references: IReferences = None
        self.__opened: bool = None
        self.__local_connection: bool = None
        self.__schema_statements = []

        # The dependency resolver.
        self._dependency_resolver = DependencyResolver(PostgresPersistence._default_config)

        # The logger.
        self._logger = CompositeLogger()

        # The PostgreSQL connection component.
        self._connection: PostgresConnection = None

        # The PostgreSQL connection pool object.
        self._client = None

        # The PostgreSQL database name.
        self._database_name = None

        self._max_page_size = 100

    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        config = config.set_defaults(PostgresPersistence._default_config)
        self.__config = config

        self._dependency_resolver.configure(config)

        self._max_page_size = config.get_as_integer_with_default("options.max_page_size", self._max_page_size)

        self._table_name = config.get_as_string_with_default('collection', self._table_name)
        self._table_name = config.get_as_string_with_default('table', self._table_name)

    def set_references(self, references):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self.__references = references
        self._logger.set_references(references)

        # Get connection
        self._dependency_resolver.set_references(references)
        self._connection = self._dependency_resolver.get_one_optional('connection')
        # Or create a local one
        if self._connection is None:
            self._connection = self.__create_connection()
            self.__local_connection = True
        else:
            self.__local_connection = False

    def unset_references(self):
        """
        Unsets (clears) previously set references to dependent components.
        """
        self._connection = None

    def __create_connection(self):
        connection = PostgresConnection()

        if self.__config:
            connection.configure(self.__config)

        if self.__references:
            connection.set_references(self.__references)

        return connection

    def _ensure_index(self, name, keys, options=None):
        """
        Adds index definition to create it on opening

        :param keys: index keys (fields)
        :param options: index options
        """
        builder = 'CREATE'

        options = options or {}

        if options.get('unique'):
            builder += " UNIQUE"

        builder += " INDEX IF NOT EXISTS " + self._quote_identifier(name) + " ON " + self._quote_identifier(
            self._table_name)

        if options.get('type'):
            builder += " " + options['type']

        fields = ''
        for key in keys:
            if fields != '':
                fields += ", "
            fields += key
            asc = keys[key]
            if not asc:
                fields += " DESC"

        builder += " (" + fields + ")"

        self._ensure_schema(builder)

    def _auto_create_objects(self, schema_statement):
        """
        Adds a statement to schema definition.
        This is a deprecated method. Use ensureSchema instead.

        :param schema_statement: a statement to be added to the schema
        """
        self._ensure_schema(schema_statement)

    def _ensure_schema(self, schema_statement):
        """
        Adds a statement to schema definition

        :param schema_statement: a statement to be added to the schema
        """
        self.__schema_statements.append(schema_statement)

    def _clear_schema(self):
        """
        Clears all auto-created objects
        """
        self.__schema_statements = []

    def _define_schema(self):
        # Todo: override in child classes
        pass

    def _convert_to_public(self, value):
        """
        Converts object value from internal to public format.

        :param value: an object in internal format to convert.
        :return: converted object in public format.
        """
        return value

    def _convert_from_public(self, value):
        """
        Convert object value from public to internal format.

        :param value: an object in public format to convert.
        :return: converted object in internal format.
        """
        return value

    def _quote_identifier(self, value):

        if value is None or value == '':
            return value

        if value[0] == '"':
            return value

        return '"' + value + '"'

    def is_opened(self):
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self.__opened

    def open(self, correlation_id):
        """
        Opens the component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :return: raise error or None no errors occured.
        """
        if self.__opened:
            return

        if self._connection is None:
            self._connection = self.__create_connection()
            self.__local_connection = True

        if self.__local_connection:
            self._connection.open(correlation_id)

        if self._connection is None:
            raise InvalidStateException(correlation_id, 'NO_CONNECTION', 'PostgreSQL connection is missing')

        if not self._connection.is_opened():
            self.__opened = False
            raise ConnectionException(correlation_id, "CONNECT_FAILED", "PostgreSQL connection is not opened")

        self._client = self._connection.get_connection()
        # add query method
        self._client.query = self.__query

        self._database_name = self._connection.get_database_name()

        # Define database schema
        self._define_schema()

        # Recreate objects
        try:
            self._create_schema(correlation_id)
            self.__opened = True
            self._logger.debug(correlation_id,
                               "Connected to postgres database %s, collection %s",
                               self._database_name,
                               self._quote_identifier(self._table_name))
        except Exception as err:
            raise ConnectionException(correlation_id, "CONNECT_FAILED", "Connection to postgres failed").with_cause(err)

    def close(self, correlation_id):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :return: raise error or None no errors occured.
        """
        if not self.__opened:
            return

        if self._connection is None:
            raise InvalidStateException(correlation_id, 'NO_CONNECTION', 'Postgres connection is missing')

        if self.__local_connection:
            self._connection.close(correlation_id)

            self.__opened = False
            self._client = None
        else:
            self.__opened = False
            self._client = None

    # def __query(self, query, params=None):
    #
    #     conn = self._client.getconn()
    #     cursor = conn.cursor()
    #
    #     if params:
    #         cursor.execute(query, params)
    #     else:
    #         cursor.execute(query)
    #
    #     response = cursor.fetchall()
    #
    #     conn.commit()
    #     cursor.close()
    #     self._client.putconn(conn)
    #     return response, cursor

    def __query(self, query, params=None):
        result = {'rowcount': None,
                  'items': [],
                  'statusmessage': None
                  }

        conn = self._client.getconn()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        try:
            response = cursor.fetchall()
            column_names = [column.name for column in cursor.description]
            for obj in response:
                result['items'].append(dict(zip(column_names, obj)))
        except ProgrammingError:
            pass

        # affected rows
        result.update({'rowcount': cursor.rowcount,
                       'statusmessage': cursor.statusmessage})

        conn.commit()
        cursor.close()
        conn.close()
        self._client.putconn(conn)
        return result

    def clear(self, correlation_id):
        """
        Clears component state.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :return: raise error or None no errors occured.
        """

        # Return error if collection is not set
        if self._table_name is None:
            raise Exception('Table name is not defined')

        query = "DELETE FROM " + self._quote_identifier(self._table_name)

        try:
            # self._client.query(query) # TODO
            conn = self._client.getconn()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
            self._client.putconn(conn)

        except Exception as err:
            raise ConnectionException(correlation_id, "CONNECT_FAILED", "Connection to postgres failed").with_cause(err)

    def _create_schema(self, correlation_id):
        if self.__schema_statements is None or len(self.__schema_statements) == 0:
            return None

        # Check if table exist to determine weither to auto create objects
        query = "SELECT to_regclass('" + self._table_name + "')"

        result = self._client.query(query)

        # If table already exists then exit
        if result['items'] and len(result['items']) > 0 and result['items'][0]['to_regclass'] is not None:
            return

        self._logger.debug(correlation_id,
                           'Table ' + self._table_name + ' does not exist. Creating database objects...')

        # Run all DML commands
        try:
            for dlm in self.__schema_statements:
                self._client.query(dlm)
        except Exception as err:
            self._logger.error(correlation_id, err, 'Failed to autocreate database object')

    def _generate_columns(self, values):
        """
        Generates a list of column names to use in SQL statements like: "column1,column2,column3"

        :param values: an array with column values or a key-value map
        :return: a generated list of column names
        """
        values = values.keys()

        result = ''
        for value in values:
            if result != '':
                result += ','
            result += self._quote_identifier(value)

        return result

    def _generate_parameters(self, values):
        """
        Generates a list of value parameters to use in SQL statements like: "%s,%s,%s"

        :param values:
        :return: a generated list of value parameters
        """
        values = values if not isinstance(values, dict) else values.keys()

        result = ''
        for val in values:
            if result != '':
                result += ','
            result += '%s'  # "$" + index;

        return result

    def _generate_set_parameters(self, values):
        """
        Generates a list of column sets to use in UPDATE statements like: column1=%s,column2=%s

        :param values: a key-value map with columns and values
        :return: a generated list of column sets
        """
        result = ''
        index = 1
        for column in values.keys():
            if result != '':
                result += ','
            result += self._quote_identifier(column) + '=%s'  # "=$" + index;
            index += 1

        return result

    def _generate_values(self, values):
        """
        Generates a list of column parameters

        :param values: a key-value map with columns and values
        :return: a generated list of column values
        """
        return list(values.values())

    def get_page_by_filter(self, correlation_id, filter, paging, sort, select):
        """
        Gets a page of data items retrieved by a given filter and sorted according to sort parameters.
        This method shall be called by a public getPageByFilter method from child class that
        receives FilterParams and converts them into a filter function.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param filter: (optional) a filter JSON object
        :param paging: (optional) paging parameters
        :param sort: (optional) sorting JSON object
        :param select: (optional) projection JSON object
        :return: a data page or error
        """
        select = select if select and len(select) > 0 else '*'
        query = "SELECT " + select + " FROM " + self._quote_identifier(self._table_name)

        # Adjust max item count based on configuration
        paging = paging or PagingParams()

        skip = paging.get_skip(-1)
        take = paging.get_take(self._max_page_size)
        paging_enabled = paging.total

        if filter and filter != '':
            query += " WHERE " + filter

        if sort:
            query += " ORDER BY " + sort

        if skip >= 0:
            query += " OFFSET " + str(skip)

        query += " LIMIT " + str(take)

        result = self._client.query(query)
        items = result['items']

        if items is not None:
            self._logger.trace(correlation_id, "Retrieved %d from %s", len(items), self._table_name)

        items = list(map(self._convert_to_public, items))

        if paging_enabled:
            query = 'SELECT COUNT(*) AS count FROM ' + self._quote_identifier(self._table_name)
            if filter is not None and filter != '':
                query += " WHERE " + filter

            result = self._client.query(query)

            count = LongConverter.to_long(result['rows'][0]['count']) if result['rows'] and len(
                result['rows']) == 1 else 0

            return DataPage(items, count)
        else:
            return DataPage(items)

    def get_count_by_filter(self, correlation_id, filter):
        """
        Gets a number of data items retrieved by a given filter.
        This method shall be called by a public getCountByFilter method from child class that
        receives FilterParams and converts them into a filter function.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param filter: (optional) a filter JSON object
        :return: a data page or error
        """
        query = 'SELECT COUNT(*) AS count FROM ' + self._quote_identifier(self._table_name)

        if filter and filter != '':
            query += " WHERE " + filter

        result = self._client.query(query)

        count = LongConverter.to_long(result['items'][0]['count']) if result['items'] and len(
            result['items']) == 1 else 0

        if count is not None:
            self._logger.trace(correlation_id, "Counted %d items in %s", count, self._table_name)

        return count

    def get_list_by_filter(self, correlation_id, filter, sort, select):
        """
        Gets a list of data items retrieved by a given filter and sorted according to sort parameters.

        This method shall be called by a public getListByFilter method from child class that
        receives FilterParams and converts them into a filter function.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param filter: (optional) a filter JSON object
        :param sort: (optional) sorting JSON object
        :param select: (optional) projection JSON object
        :return: data list
        """

        select = select if len(select) > 0 else '*'
        query = "SELECT " + select + " FROM " + self._quote_identifier(self._table_name)

        if filter and filter != '':
            query += " WHERE " + filter

        if sort:
            query += " ORDER BY " + sort

        items = self._client.query(query)

        if items is not None:
            self._logger.trace(correlation_id, "Retrieved %d from %s", len(items), self._table_name)

        items = list(map(self._convert_to_public, items))

        return items

    def get_one_random(self, correlation_id, filter):
        """
        Gets a random item from items that match to a given filter.
        This method shall be called by a public getOneRandom method from child class that
        receives FilterParams and converts them into a filter function.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param filter: (optional) a filter JSON object
        :return: a random item
        """
        query = 'SELECT COUNT(*) AS count FROM ' + self._quote_identifier(self._table_name)
        if filter and filter != '':
            query += " WHERE " + filter

        result = self._client.query(query)

        query = "SELECT * FROM " + self._quote_identifier(self._table_name)

        if filter and filter != '':
            query += " WHERE " + filter

        count = result['rows'].count if result['rows'] and len(result['rows']) == 1 else 0
        pos = random.randint(0, count - 1)
        query += f" OFFSET {pos} LIMIT 1"

        result = self._client.query(query)

        items = result['rows']
        item = items[0] if items is not None and len(items) > 0 else None

        if item is None:
            self._logger.trace(correlation_id, "Random item wasn't found from %s", self._table_name)
        else:
            self._logger.trace(correlation_id, "Retrieved random item from %s", self._table_name)

        item = self._convert_to_public(item)

        return item

    def create(self, correlation_id, item):
        """
        Creates a data item.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param item: an item to be created.
        :return: created item
        """
        if not item:
            return

        row = self._convert_from_public(item)
        columns = self._generate_columns(row)
        params = self._generate_parameters(row)
        values = self._generate_values(row)

        query = "INSERT INTO " + self._quote_identifier(
            self._table_name) + " (" + columns + ") VALUES (" + params + ") RETURNING *"

        result = self._client.query(query, values)
        self._logger.trace(correlation_id, "Created in %s with id = %s", self._table_name, row['id'])

        new_item = self._convert_to_public(result['items'][0]) if result['items'] and result['items'][0] and len(
            result['items']) == 1 else None

        return new_item

    def delete_by_filter(self, correlation_id, filter):
        """
        Deletes data items that match to a given filter.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param filter: (optional) a filter JSON object.
        :return: null for success
        """
        query = "DELETE FROM " + self._quote_identifier(self._table_name)
        if filter and filter != '':
            query += " WHERE " + filter

        result = self._client.query(query)

        count = result['rowcount'] if result['rowcount'] else 0

        self._logger.trace(correlation_id, "Deleted %d items from %s", count, self._table_name)
