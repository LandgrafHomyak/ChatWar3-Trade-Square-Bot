from telethon import TelegramClient
from telethon.sessions import MemorySession

from configuration import Configuration


class UserBot:
    def __new__(cls, configuration, loop):
        if type(configuration) is not Configuration:
            raise TypeError("'configuration' must be instance of 'configuration.Configuration'")

        self = super().__new__(cls)

        self.__client = TelegramClient(
            configuration.userbot_session_name,
            configuration.api_id, configuration.api_hash,
            loop=loop
        )
        self.__client.start(phone=lambda: configuration.userbot_phone)

        print("User bot launched")

        return self

    @property
    def client(self):
        return self.__client
