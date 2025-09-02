import psycopg2

from dags.utils import get_env


class Postgres:

    def __init__(self):
        self.__host = get_env('POSTGRES_HOST')
        self.__port = get_env('POSTGRES_PORT')
        self.__database = get_env('POSTGRES_DATABASE')
        self.__user = get_env('POSTGRES_USER')
        self.__password = get_env('POSTGRES_PASSWORD')
        self.__connection_server = None
        self.__connection_database = None

    def create_database(self):
        self._connect_server()



    def _connect_server(self):
        if not self.__connection_server:
            self.__connection_server = psycopg2.connect(
                host=self.__host,
                port=self.__port,
                user=self.__user,
                password=self.__password
            )

    def _connect_database(self):
        if not self.__connection_database:
            self.__connection_database = psycopg2.connect(
                host=self.__host,
                port=self.__port,
                database=self.__database,
                user=self.__user,
                password=self.__password
            )
