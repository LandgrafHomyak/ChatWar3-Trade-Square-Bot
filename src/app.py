import asyncio

from configuration import Configuration
from nativebot import NativeBot
from userbot import UserBot


class CW3TradeSquareBotApp:
    def __new__(cls, configuration):
        if type(configuration) is not Configuration:
            raise TypeError("'configuration' must be instance of 'configuration.Configuration'")

        self = super().__new__(cls)

        self.__configuration = configuration

        self.__loop = asyncio.get_event_loop()  # todo on new event loop doesn't works userbot configuration

        self.__userbot = UserBot(configuration, self.__loop)
        self.__nativebot = NativeBot(configuration, self.__loop)
        self.__userbot.nativebot = self.__nativebot.client
        self.__nativebot.userbot = self.__userbot.client

        self.__both_connected_locker = asyncio.locks.Lock(loop=self.__loop)

        return self

    async def __run_until_disconnected(self):
        if self.__both_connected_locker.locked():
            raise RuntimeError("App executed twice")

        await self.__both_connected_locker.acquire()  # todo doesn't works

        ub_task = self.__loop.create_task(self.__userbot.client.run_until_disconnected())
        ub_task.add_done_callback(self.__both_connected_locker.release)
        nb_task = self.__loop.create_task(self.__nativebot.client.run_until_disconnected())
        nb_task.add_done_callback(self.__both_connected_locker.release)

        await self.__both_connected_locker.acquire()
        self.__both_connected_locker.release()

    def run_until_disconnected(self):
        self.__loop.run_until_complete(self.__run_until_disconnected())

    def exec(self):
        self.run_until_disconnected()
        print("Disconnected...")
        return 1
