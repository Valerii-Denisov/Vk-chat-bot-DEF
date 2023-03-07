import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from chat_bots.get_data import get_yaml_data
from peewee import Model
from peewee import PeeweeException
from peewee import IntegrityError
import peewee


database_data = get_yaml_data('/home/valerii/Vk-chat-bot-DEF/database.yaml')


def create_database(database_parameters):
    try:
        connection = psycopg2.connect(
            user=database_parameters.get('user'),
            password=database_parameters.get('password'),
            host=database_parameters.get('host'),
            port=database_parameters.get('port'),
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        database_name = database_parameters.get('database_name')
        sql_create_database = 'CREATE DATABASE {0}'.format(database_name)
        cursor.execute(sql_create_database)
    except (Exception, Error) as error:
        print(
            'Ошибка при создании базы данных {0}'.format(database_name, ),
            error,
        )
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Соединение c PostgreSQL закрыто.')


def get_connection(database_parameters):
    return peewee.PostgresqlDatabase(
        database=database_parameters.get('database_name'),
        user=database_parameters.get('user'),
        password=database_parameters.get('password'),
        host=database_parameters.get('host'),
        port=database_parameters.get('port'),
    )


class Categories(Model):
    name = peewee.CharField(max_length=255, unique=True)

    class Meta:
        database = get_connection(database_data.get('database'))


class Products(Model):
    name = peewee.CharField(max_length=255, unique=True)
    description = peewee.TextField(null=False)
    foto = peewee.CharField(max_length=255, unique=True)
    category_id = peewee.ForeignKeyField(
        Categories,
        on_delete='cascade',
        field='name',
    )

    class Meta:
        database = get_connection(database_data.get('database'))


def generate_bot_database(
        model_list,
        database_parameters,
        category_list,
        product_list,
):
    create_database(database_parameters)
    bot_database = get_connection(database_parameters)
    bot_database.create_tables(model_list)
    bot_database.connect()
    for category in category_list:
        try:
            string = Categories(name=category)
            string.save()
        except(Exception, IntegrityError) as error1:
            print('Ошибка создания записи. Такая запись уже существует или '
                  'неверно указан внешний ключ. Ошибка: {0}'.format(error1))
        except(Exception, PeeweeException) as error2:
            print('Ошибка базы данных. Ошибка {0}'.format(error2))
    for product in product_list:
        try:
                string = Products(
                    name=product.get('name'),
                    description=product.get('description'),
                    foto=product.get('foto'),
                    category_id=product.get('category'),
                )
                string.save()
        except(Exception, IntegrityError) as error1:
            print('Ошибка создания записи. Такая запись уже существует или '
                  'неверно указан внешний ключ. Ошибка: {0}'.format(error1))
        except(Exception, PeeweeException) as error2:
            print('Ошибка базы данных. Ошибка {0}'.format(error2))
    bot_database.close()



