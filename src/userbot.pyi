import asyncio

from telethon import TelegramClient

from configuration import Configuration


class UserBot:
    def __new__(cls, configuration: Configuration, loop: asyncio.AbstractEventLoop) -> UserBot: ...

    client: TelegramClient = ...
