import asyncio

from telethon import TelegramClient

from configuration import Configuration


class NativeBot:
    def __new__(cls, configuration: Configuration, loop: asyncio.AbstractEventLoop) -> NativeBot: ...

    client: TelegramClient = ...
