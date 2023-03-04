import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from peewee import Model
import peewee


# спрятать в переменные среды/файл конфигурации
db_user = "postgres"
db_password = "10011992"
db_host = "127.0.0.1"
db_port = "5432"
db_name = 'bakery_db'
categories = ['Напитки', 'Сладкая выпечка', 'Торты']
products = [
    {'name': 'Американо', 'description': 'Обычный кофе', 'foto': 'foto2222', 'category': 'Напитки'},
    {'name': 'Булка', 'description': 'булка', 'foto': 'foto2223', 'category': 'Сладкая выпечка'},
    {'name': 'Торт', 'description': 'торт', 'foto': 'foto2224', 'category': 'Торты'},
]




class BotDatabase:

    def __init__(self, user, password, host, port, database_name):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name

    def create_database(self):
        try:
            connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            sql_create_database = 'CREATE DATABASE {0}'.format(
                self.database_name,
            )
            cursor.execute(sql_create_database)
        except (Exception, Error) as error:
            print(
                'Ошибка при создании базы данных {0}'.format(
                    self.database_name,
                ),
                error,
            )
        finally:
            if connection:
                cursor.close()
                connection.close()
                print('База данных создана. Соединение закрыто')

    def get_connection(self):
        return peewee.PostgresqlDatabase(
            database=self.database_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )


bot_db = BotDatabase(db_user, db_password, db_host, db_port, db_name)

class Categories(Model):
    name = peewee.CharField(max_length=255, unique=True)

    class Meta:
        database = bot_db.get_connection()


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
        database = bot_db.get_connection()


def generate_bot_database(model_list, database, category_list, product_list):
    database.create_database()
    connection = database.get_connection()
    connection.create_tables(model_list)
    connection.connect()
    for category in category_list:
        string = Categories(name=category)
        string.save()
    for product in product_list:
        string = Products(
            name=product.get('name'),
            description=product.get('description'),
            foto=product.get('foto'),
            category_id=product.get('category'),
        )
        string.save()
    connection.close()


# generate_bot_database([Categories, Products], bot_db, categories, products)
