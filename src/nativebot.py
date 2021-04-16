from telethon import TelegramClient
from telethon.sessions import MemorySession

from configuration import Configuration


class NativeBot:
    def __new__(cls, configuration, loop):
        if type(configuration) is not Configuration:
            raise TypeError("'configuration' must be instance of 'configuration.Configuration'")

        self = super().__new__(cls)

        self.__client = TelegramClient(
            MemorySession(),
            configuration.api_id,
            configuration.api_hash,
            loop=loop
        )
        self.__client.start(bot_token=configuration.bot_token)

        print("Native bot launched")

        return self

    @property
    def client(self):
        return self.__client
