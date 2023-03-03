import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class BotDatabase:

    def __init__(self, user, password, host, port):
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def create_database(self, database_name):
        try:
            connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            sql_create_database = 'CREATE DATABASE {0}'.format(database_name)
            cursor.execute(sql_create_database)
        except (Exception, Error) as error:
            print(
                'Ошибка при создании базы данных {0}'.format(database_name),
                error,
            )
        finally:
            if connection:
                cursor.close()
                connection.close()
                print('База данных создана. Соединение закрыто')

    def connection_to_database(self, database_name):
        try:
            connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=database_name,
            )
        except (Exception, Error) as error:
            print(
                'Ошибка при подключении к базе данных {0}'.format(
                    database_name
                ),
                error,
            )
        finally:
            if connection:
                print('Подключение к базе данных успешно.')
                return connection

    def close_conection(self, connection, cursor):
        if connection:
            cursor.close()
            connection.close()
            print('Соединение закрыто')

    def create_table(self, database_name, table_query):
        try:
            connection = self.connection_to_database(database_name)
            cursor = connection.cursor()
            cursor.execute(table_query)
            connection.commit()
            print("Таблица успешно создана в PostgreSQL")
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.close_conection(connection, cursor)

    def fill_table(self, database_name, insert_query):
        try:
            connection = self.connection_to_database(database_name)
            cursor = connection.cursor()
            cursor.execute(insert_query)
            connection.commit()
            print("Таблица успешно заполнена в PostgreSQL")
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.close_conection(connection, cursor)

    def get_data(self, database_name, select_query):
        try:
            connection = self.connection_to_database(database_name)
            cursor = connection.cursor()
            cursor.execute(select_query)
            connection.commit()
            print("Данные успешно получены")
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.close_conection(connection, cursor)


