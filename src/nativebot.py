import asyncio

from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.sessions import MemorySession
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import User, ChannelParticipantsAdmins

from configuration import Configuration


class NativeBot:
    def __new__(cls, configuration, loop):
        if type(configuration) is not Configuration:
            raise TypeError("'configuration' must be instance of 'configuration.Configuration'")

        self = super().__new__(cls)

        self.__configuration = configuration

        self.__client = TelegramClient(
            MemorySession(),
            configuration.api_id,
            configuration.api_hash,
            loop=loop
        )
        self.__client.parse_mode = "html"
        self.__client.start(bot_token=configuration.bot_token)
        print("Native bot launched")

        asyncio.ensure_future(self.__init(configuration, loop), loop=loop)

        return self

    async def __init(self, configuration, loop):
        self.__client.on(NewMessage(
            incoming=True,
            pattern="/start[@\s]?",
            func=lambda event: isinstance(event.chat, User)
        ))(
            self.__on_start
        )
        self.__client.on(NewMessage(
            incoming=True,
            pattern="/help[@\s]?",
            func=lambda event: isinstance(event.chat, User)
        ))(
            self.__on_help
        )

        self.__client.on(NewMessage(
            incoming=True,
            pattern="/access_channel[@\s]?",
            func=lambda event: isinstance(event.chat, User)
        ))(
            self.__on_access_channel
        )

    @property
    def client(self):
        return self.__client

    async def __on_start(self, event):
        in_g = event.chat in await self.__client.get_participants(self.__configuration.group_id)
        in_c = event.chat in await self.__client.get_participants(self.__configuration.channel_id)
        if in_g and in_c:
            await self.__client.send_message(
                event.chat.id,
                """
Добро пожавловать к друиду торгового духа, чем могу быть полезен?

Для просмотра полного списка моих услуг напиши /help
"""
            )
        elif in_g or in_c:
            await self.__client.send_message(
                event.chat.id,
                f"""
Добро пожавловать к друиду торгового духа, я могу быть полезен тем, что сообщу тебе, что ты еще не присоединился к торговому {
                f"<a href='{(await self.__client(ExportChatInviteRequest(self.__configuration.channel_id))).link}'>каналу</a>" if in_g else f"<a href='{(await self.__client(ExportChatInviteRequest(self.__configuration.group_id))).link}'>чату</a>"
                }!

Для просмотра полного списка моих услуг напиши /help
"""
            )

        else:
            await self.__client.send_message(
                event.chat.id,
                f"""
Добро пожавловать к друиду торгового духа! Первый раз у нас? Скорее заходи в наши <a href='{(await self.__client(ExportChatInviteRequest(self.__configuration.group_id))).link}'>чат</a> и <a href='{(await self.__client(ExportChatInviteRequest(self.__configuration.channel_id))).link}'>канал</a> и присоединяйся к веселым торгам!

Для просмотра полного списка моих услуг напиши /help
"""
            )  # todo cache requests

    async def __on_help(self, event):
        in_g = event.chat in await self.__client.get_participants(self.__configuration.group_id)
        in_c = event.chat in await self.__client.get_participants(self.__configuration.channel_id)
        x = "\u274c"
        v = "\u2705"
        await self.__client.send_message(
            event.chat.id,
            f"""
<b>Полный список моих услуг:</b>
<code>{v if in_g else x}</code>Зайти в чат по <a href='{(await self.__client(ExportChatInviteRequest(self.__configuration.group_id))).link}'>сcылке</a>
<code>{v if in_c else x}</code>Зайти на канал по <a href='{(await self.__client(ExportChatInviteRequest(self.__configuration.channel_id))).link}'>сcылке</a>
<code>{v if event.chat in await  self.__client.get_participants(self.__configuration.channel_id, filter=ChannelParticipantsAdmins) else x}</code>Получить права на канале командой /access_channel
"""
        )  # todo cache requests

    async def __on_access_channel(self, event):
        in_c = event.chat in await self.__client.get_participants(self.__configuration.channel_id)
        in_ca = event.chat in await self.__client.get_participants(self.__configuration.channel_id, filter=ChannelParticipantsAdmins)
        if not in_c:
            await self.__client.send_message(
                event.chat.id,
                f"Мне некому выдать твои права на канале, придется тебе на него подписатся по <a href='{(await self.__client(ExportChatInviteRequest(self.__configuration.channel_id))).link}'>сcылке</a>"
            ) # todo cache requests
        elif in_ca:
            await self.__client.send_message(
                event.chat.id,
                f"Я ценю твой юмор, но больше дозволенного ты не получишь."
            )
        else:
            await self.__client.edit_admin(
                self.__configuration.channel_id,
                event.chat.id,
                change_info=False,
                post_messages=True,
                edit_messages=False,
                delete_messages=False,
                ban_users=False,
                invite_users=False,
                pin_messages=False,
                add_admins=False,
                manage_call=False,
                anonymous=False,
                is_admin=True,
                title="простой смертный"
            )
            await self.__client.send_message(
                event.chat.id,
                f"Ты получил свои права. Да начнутся великие торги!"
            )
