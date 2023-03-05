#!/usr/bin/env python
"""The main script of the project."""

from chat_bots.bot import VkBot
from chat_bots.get_data import get_yaml_data


def main():
    configuration = get_yaml_data('config.yaml')
    server = VkBot(
        configuration.get('vk_api_token'),
        configuration.get('group_id'),
        configuration.get('server_name'),
    )
    server.start()
    print('Chat-bot is starting')


if __name__ == '__main__':
    main()
