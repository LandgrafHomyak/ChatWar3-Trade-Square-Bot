import asyncio

from telethon import TelegramClient
from telethon.events import ChatAction
from telethon.sessions import MemorySession
from telethon.tl.functions.messages import ExportChatInviteRequest

from configuration import Configuration


class UserBot:
    def __new__(cls, configuration, loop):
        if type(configuration) is not Configuration:
            raise TypeError("'configuration' must be instance of 'configuration.Configuration'")

        self = super().__new__(cls)

        self.__configuration = configuration

        self.__client = TelegramClient(
            configuration.userbot_session_name,
            configuration.api_id, configuration.api_hash,
            loop=loop
        )
        self.__client.parse_mode = "html"
        self.__client.start(phone=lambda: configuration.userbot_phone)
        print("User bot launched")

        asyncio.ensure_future(self.__init(configuration, loop), loop=loop)

        return self

    async def __init(self, configuration, loop):
        await self.__client.get_dialogs()
        # await self.__client.get_entity(89616296)
        self.__client.on(
            ChatAction(
                configuration.group_id,
                func=lambda __event: __event.user_joined or __event.user_added
            )
        )(
            self.__on_new_user_in_group,
        )

        print("User bot configured")

    @property
    def client(self):
        return self.__client

    async def __on_new_user_in_group(self, event):
        new_u = await event.get_user()
        if new_u.bot:
            await event.reply("Ботам тут не рады, проваливай!")
            await self.__client.kick_participant(event.chat.id, new_u.id)
            return

        await event.reply(
            f"""
<a href='tg://user?id={new_u.id}'>{new_u.first_name}</a>, добро пожаловать на <i>Рыночную площадь без <a href='tg://user?id={89616296}'>Свеи</a> или v2.0</i>!

<b>Здесь нет каких то жестоких правил, но есть несколько рекомендаций и советов:</b>
\u2734\ufe0f Чтобы предложить что либо на продажу или купить, нужно зайти на <a href='{(await self.__client(ExportChatInviteRequest(self.__configuration.channel_id))).link}'>канал</a>, а потом написать в лс <a href='tg://user?id={(await self.nativebot.get_me()).id}'>боту</a> <code>/access_channel</code> чтобы получить права на публикацию
\u2734\ufe0f На канале можно постить сообщения только с тегами <code>#wtb</code> или <code>#wts</code>
\u2734\ufe0f Правило хорошего тона - отвечать на предложения реплаем или в комментариях, чтобы было удобно отслеживать торг
\u2734\ufe0f Продолжение следует... 
""")  # todo cache requests
