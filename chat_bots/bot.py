import vk_api.vk_api

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from chat_bots.keyboard import make_keyboard
from chat_bots.database.database_processor import Categories, Products

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
                    self.vk_api.messages.send(
                        user_id=event.obj['user_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj['peer_id'],
                        keyboard=main_keyboard.get_empty_keyboard(),
                        message='Для начала работы пришлите боту сообщение',
                    )
                else:
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
