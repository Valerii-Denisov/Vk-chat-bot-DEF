from get_data import get_yaml_data
from database.database_processor import generate_bot_database
from database.database_processor import Categories, Products


database_data = get_yaml_data('/home/valerii/Vk-chat-bot-DEF/database.yaml')
generate_bot_database(
    [Categories, Products],
    database_data.get('database'),
    database_data.get('categories'),
    database_data.get('products'),
)
