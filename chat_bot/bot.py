import vk_api.vk_api

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from keyboard import make_keyboard
from database.database import BotDatabase

user = "postgres"
password = "10011992"
host = "127.0.0.1"
port = "5432"
settings = dict(one_time=False, inline=True)

class VkBot:
    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        # Даем серверу имя
        self.server_name = server_name

        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)

        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)

        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

    def start(self):
        database_name = 'bakery_db'
        bot_database = BotDatabase(user, password, host, port)
        main_button_name = bot_database.get_data(
            database_name,
            """SELECT NAME FROM CATEGORY"""
        )
        main_keyboard = make_keyboard(settings, main_button_name)
        for event in self.long_poll.listen():  # Слушаем сервер
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
                print(event.type)
                print(event.object.payload.get('type'))
                if event.object.payload.get('type') != 'main':
                    print(event)
                    print(event.object.payload.get('type'))
                    cetegory_keyboard = make_keyboard(
                        settings,
                        bot_database.get_data(
                            database_name,
                            """SELECT NAME FROM Products""",
                        ),
                        event.object.payload.get('type')
                        )
                    print(event.object)
                    self.vk_api.messages.edit(
                        peer_id=event.obj.peer_id,
                        message='ola',
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=(main_keyboard if event.object.payload.get('type') == 'mine' else cetegory_keyboard).get_keyboard(),
                        message_id=event.obj.id,
                    )
