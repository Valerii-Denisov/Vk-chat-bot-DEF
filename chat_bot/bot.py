import vk_api.vk_api

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from keyboard import make_keyboard
from database.database_processor import Categories, Products

db_user = "postgres"
db_password = "10011992"
db_host = "127.0.0.1"
db_port = "5432"
db_name = 'bakery_db'
settings = dict(one_time=True, inline=False)


class VkBot:
    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()

    def start(self):
        main_button_name = [category.name for category in Categories.select()]
        main_keyboard = make_keyboard(settings, main_button_name)
        for event in self.long_poll.listen():
            print(event)
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.obj.message['text'] != '':
                    if event.from_user:
                        self.vk_api.messages.send(
                            user_id=event.obj.message['from_id'],
                            random_id=get_random_id(),
                            peer_id=event.obj.message['from_id'],
                            keyboard=main_keyboard.get_keyboard(),
                            message='Выберите категорию',
                        )
            elif event.type == VkBotEventType.MESSAGE_EVENT:
                category_button_name = [
                    product.name for product in Products.select().where(
                        Products.category_id == event.object.payload.get('type')
                    )]
                if event.object.payload.get('type') in main_button_name:
                    category_keyboard = make_keyboard(
                        settings,
                        category_button_name,
                        event.object.payload.get('type'),
                    )
                    self.vk_api.messages.send(
                        user_id=event.obj['user_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj['peer_id'],
                        message='Выберете продукт',
                        keyboard=category_keyboard.get_keyboard(),
                    )
                elif event.object.payload.get('type') == 'mine':
                    self.vk_api.messages.send(
                        user_id=event.obj['user_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj['peer_id'],
                        keyboard=main_keyboard.get_keyboard(),
                        message='Выберите категорию',
                    )
                elif event.object.payload.get('type') == 'close':
                    print('boom-boom')
                    self.vk_api.messages.send(
                        user_id=event.obj['user_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj['peer_id'],
                        keyboard=main_keyboard.get_empty_keyboard(),
                        message='Для возобновления работы пришлите боту любое сообщение',
                    )
                else:
                    print('boom')
                    print(event.object.payload.get('type'))
                    product = Products.get(
                        Products.name == event.object.payload.get('type'),
                    )
                    self.vk_api.messages.send(
                        user_id=event.obj['user_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj['peer_id'],
                        message=product.description,
                        keyboard=category_keyboard.get_keyboard(),
                        attachment=product.foto,
                    )
