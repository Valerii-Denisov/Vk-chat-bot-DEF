from database import BotDatabase

# спрятать следущие данный в .ЕНВ
user = "postgres"
password = "10011992"
host = "127.0.0.1"
port = "5432"



def generate_bot_database():
    database_name = 'bakery_db'
    bot_database = BotDatabase(user, password, host, port)
    bot_database.create_database(database_name)
    bot_database.create_table(
        database_name,
        '''CREATE TABLE category (ID SERIAL PRIMARY KEY NOT NULL,
                 NAME VARCHAR(255) NOT NULL UNIQUE);''')
    bot_database.fill_table(
        database_name,
        """ INSERT INTO category (NAME) VALUES 
        ('Drinks'), ('Bakery_products'), ('Pie');"""
    )
    bot_database.create_table(
        database_name,
        '''CREATE TABLE Products (ID SERIAL PRIMARY KEY NOT NULL,
                NAME VARCHAR(255) NOT NULL UNIQUE,
                CATEGORYID INTEGER NOT NULL,
                DESCRIPTION TEXT NOT NULL,
                FOTO VARCHAR(255) NOT NULL UNIQUE,
                FOREIGN KEY (CATEGORYID) REFERENCES CATEGORY (Id) ON DELETE CASCADE);''')
    bot_database.fill_table(
        database_name,
        """ INSERT INTO Products (NAME, CATEGORYID, DESCRIPTION, FOTO) 
        VALUES ('Capuchino', 1, 'Coffe with milk', 'photo1'), 
               ('Lemonade', 1, 'lemon with lime', 'photo2'),
               ('Americano', 1, 'lemon with lime', 'photo3'),
               ('Kruasan blat', 2, 'pft,fkj', 'photo4'); 
               """
    )
    print(bot_database.get_data(
        database_name,
    """select name from category"""))

generate_bot_database()
