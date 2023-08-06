# -*- coding: utf-8 -*-
from copy import deepcopy

from pip_services3_commons.data import IIdentifiable, IdGenerator

from pip_services3_postgres.persistence.PostgresPersistence import PostgresPersistence


class IdentifiablePostgresPersistence(IIdentifiable, PostgresPersistence):
    """
    Abstract persistence component that stores data in PostgreSQL
    and implements a number of CRUD operations over data items with unique ids.
    The data items must implement :class:`IIdentifiable <pip_services3_commons.data.IIdentifiable.IIdentifiable>` interface.

    In basic scenarios child classes shall only override :func:`get_page_by_filter <pip_services3_postgres.persistence.IdentifiableJsonPostgresPersistence.get_page_by_filter>`,
    :func:`get_list_by_filter <pip_services3_postgres.persistence.IdentifiableJsonPostgresPersistence.get_list_by_filter>` or :func:`delete_by_filter <pip_services3_postgres.persistence.IdentifiableJsonPostgresPersistence.delete_by_filter>`
    operations with specific filter function.
    All other operations can be used out of the box.

    In complex scenarios child classes can implement additional operations by
    accessing **self._collection** and **self._model** properties.

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

        class MyPostgresPersistence(IdentifiablePostgresJsonPersistence):

            def __init__(self):
                super(MyPostgresPersistence, self).__init__('mydata', MyDataPostgresSchema())

            def __compose_filter(self, filter):
                filter = filter or FilterParams()
                criteria = []

                name = filter.get_as_nullable_string('name')
                if name is not None:
                    criteria.append({'name':name})

                return { '$and': criteria } if len(criteria) > 0 else None

            def get_page_by_filter(self, correlation_id, filter, paging):
                return super().get_page_by_filter(correlation_id, self.__compose_filter(filter), paging, None, None)

        persistence = MyPostgresPersistence()
        persistence.configure(ConfigParams.from_tuples(
            "host", "localhost",
            "port", 27017
        ))

        persistence.open("123")

        persistence.create("123", {'id': "1", 'name': "ABC"})
        page = persistence.get_page_by_filter('123', FilterParams.from_tuples('name', 'ABC'), None)
        print(page.data)  # Result: { id: "1", name: "ABC" }

        persistence.delete_by_id("123", "1")
        # ...

    """

    def __init__(self, table_name):
        """
        Creates a new instance of the persistence component.

        :param table_name: (optional) a collection name.
        """
        super(IdentifiablePostgresPersistence, self).__init__(table_name)

        if table_name is None:
            Exception("Table name could not be null")

    def _convert_from_public_partial(self, value):
        """
        Converts the given object from the public partial format.

        :param value: the object to convert from the public partial format.
        :return: the initial object.
        """
        return self._convert_to_public(value)

    def get_list_by_ids(self, correlation_id, ids):
        """
        Gets a list of data items retrieved by given unique ids.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param ids: ids of data items to be retrieved
        :return: data list
        """
        params = self._generate_parameters(ids)
        query = "SELECT * FROM " + self._quote_identifier(self._table_name) + " WHERE \"id\" IN(" + params + ")"
        result = self._client.query(query, ids)
        items = result['items']

        if items is not None:
            self._logger.trace(correlation_id, "Retrieved %d from %s", len(items), self._table_name)
        items = list(map(self._convert_from_public_partial, items))

        return items

    def get_one_by_id(self, correlation_id, id):
        """
        Gets a data item by its unique id.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param id: an id of data item to be retrieved.
        :return: data item
        """
        query = "SELECT * FROM " + self._quote_identifier(self._table_name) + " WHERE \"id\"=%s"
        params = [id]

        result = self._client.query(query, params)
        item = result['items'][0] or None if result['items'] and len(result['items']) else None

        if item is None:
            self._logger.trace(correlation_id, "Nothing found from %s with id = %s", self._table_name, id)
        else:
            self._logger.trace(correlation_id, "Retrieved from %s with id = %s", self._table_name, id)

        return self._convert_to_public(item)

    def create(self, correlation_id, item):
        """
        Creates a data item.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param item: an item to be created.
        :return: created item
        """
        if item is None:
            return

        # Assign unique id
        new_item = item
        if new_item['id'] is None:
            new_item = deepcopy(new_item)
            new_item['id'] = item['id'] or IdGenerator.next_long()

        return super().create(correlation_id, new_item)

    def set(self, correlation_id, item):
        """
        Sets a data item. If the data item exists it updates it,
        otherwise it create a new data item.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param item: a item to be set.
        :return: updated item
        """
        if item is None:
            return

        # Assign unique id
        if item.get('id') is None:
            item = deepcopy(item)
            item['id'] = item['id'] or IdGenerator.next_long()

        row = self._convert_from_public(item)
        columns = self._generate_columns(row)
        params = self._generate_parameters(row)
        set_params = self._generate_set_parameters(row)
        values = self._generate_values(row)
        values += deepcopy(values)

        query = "INSERT INTO " + self._quote_identifier(self._table_name) + " (" + columns + ")" \
                + " VALUES (" + params + ")" \
                + " ON CONFLICT (\"id\") DO UPDATE SET " + set_params + " RETURNING *"

        result = self._client.query(query, values)
        self._logger.trace(correlation_id, "Set in %s with id = %s", self._quote_identifier(self._table_name),
                           item['id'])

        new_item = self._convert_to_public(result['items'][0]) if result['items'] and len(
            result['items']) == 1 else None

        return new_item

    def update(self, correlation_id, item):
        """
        Updates a data item.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param item: an item to be updated.
        :return: updated item
        """
        if item is None or item.get('id') is None:
            return

        row = self._convert_from_public(item)
        params = self._generate_set_parameters(row)
        values = self._generate_values(row)
        values.append(item['id'])

        query = "UPDATE " + self._quote_identifier(self._table_name) \
                + " SET " + params + " WHERE \"id\"=%s RETURNING *"

        result = self._client.query(query, values)

        self._logger.trace(correlation_id, "Updated in %s with id = %s", self._table_name, item['id'])
        new_item = self._convert_to_public(result['items'][0]) if result['items'] and len(
            result['items']) == 1 else None

        return new_item

    def update_partially(self, correlation_id, id, data):
        """
        Updates only few selected fields in a data item.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param id: an id of data item to be updated.
        :param data: a map with fields to be updated.
        :return:  updated item
        """
        if data is None or id is None:
            return

        row = self._convert_from_public_partial(data)
        params = self._generate_set_parameters(row)
        values = self._generate_values(row)
        values.append(id)

        query = "UPDATE " + self._quote_identifier(self._table_name) \
                + " SET " + params + " WHERE \"id\"=%s RETURNING *"

        result = self._client.query(query, values)

        self._logger.trace(correlation_id, "Updated partially in %s with id = %s", self._table_name, id)
        new_item = self._convert_to_public(result['items'][0]) if result['items'] and len(
            result['items']) == 1 else None

        return new_item

    def delete_by_id(self, correlation_id, id):
        """
        Deleted a data item by it's unique id.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param id: an id of the item to be deleted
        :return: deleted item
        """
        values = [id]

        query = "DELETE FROM " + self._quote_identifier(self._table_name) + " WHERE \"id\"=%s RETURNING *"

        result = self._client.query(query, values)

        self._logger.trace(correlation_id, "Deleted from %s with id = %s", self._table_name, id)
        deleted_item = self._convert_to_public(result['items'][0]) if result['items'] and len(
            result['items']) == 1 else None

        return deleted_item

    def delete_by_ids(self, correlation_id, ids):
        """
        Deletes multiple data items by their unique ids.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param ids: ids of data items to be deleted.
        :return: None for success
        """
        params = self._generate_parameters(ids)
        query = "DELETE FROM " + self._quote_identifier(self._table_name) + " WHERE \"id\" IN(" + params + ")"

        result = self._client.query(query, ids)
        count = result['rowcount'] if result['rowcount'] else 0
        self._logger.trace(correlation_id, "Deleted %d items from %s", count, self._table_name)
