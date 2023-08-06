# -*- coding: utf-8 -*-

from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory

from pip_services3_postgres.persistence.PostgresConnection import PostgresConnection


class DefaultPostgresFactory(Factory):
    """
    Creates Postgres components by their descriptors.

    See: :class:`PostgresConnection <pip_services3_postgres.persistence.PostgresConnection.PostgresConnection>`,
    :class:`Factory <pip_services3_components.build.Factory.Factory>`
    """
    descriptor = Descriptor("pip-services", "factory", "postgres", "default", "1.0")
    postgres_connection_descriptor = Descriptor("pip-services", "connection", "postgres", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(DefaultPostgresFactory, self).__init__()
        self.register_as_type(DefaultPostgresFactory.postgres_connection_descriptor, PostgresConnection)
