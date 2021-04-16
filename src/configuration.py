import json

CONFIG_TYPING = {
    "api-id": int,
    "api-hash": str,
    "userbot-phone": str,
    "bot-token": str,
    "channel-id": int,
    "group-id": int,
    "userbot-session-name": str
}


class UnexpectedConfigurationArgumentsError(Exception):
    def __init__(self, iterable):
        self.args = tuple(iterable)


class RequiredConfigurationArgumentsError(Exception):
    def __init__(self, iterable):
        self.args = tuple(iterable)


class ConfigurationArgumentsTypeError(Exception):
    def __init__(self, key, req, exp):
        self.key = key
        self.req = req
        self.exp = exp


class Configuration:
    def __new__(cls, *, api_id, api_hash, userbot_phone, bot_token, channel_id, group_id, userbot_session_name):
        if type(api_id) is not CONFIG_TYPING["api-id"]:
            raise TypeError(
                f"'api_id' must be a {repr(CONFIG_TYPING['api-id'].__name__)}, not {repr(type(api_id).__name__)}"
            )

        if type(api_hash) is not CONFIG_TYPING["api-hash"]:
            raise TypeError(
                f"'api_hash' must be a {repr(CONFIG_TYPING['api-hash'].__name__)}, not {repr(type(api_hash).__name__)}"
            )

        if type(userbot_phone) is not CONFIG_TYPING["userbot-phone"]:
            raise TypeError(
                f"'userbot_phone' must be a {repr(CONFIG_TYPING['userbot-phone'].__name__)}, not {repr(type(userbot_phone).__name__)}"
            )

        if type(bot_token) is not CONFIG_TYPING["bot-token"]:
            raise TypeError(
                f"'bot_token' must be a {repr(CONFIG_TYPING['bot-token'].__name__)}, not {repr(type(bot_token).__name__)}"
            )

        if type(channel_id) is not CONFIG_TYPING["channel-id"]:
            raise TypeError(
                f"'channel_id' must be a {repr(CONFIG_TYPING['channel-id'].__name__)}, not {repr(type(channel_id).__name__)}"
            )

        if type(group_id) is not CONFIG_TYPING["group-id"]:
            raise TypeError(
                f"'group_id' must be a {repr(CONFIG_TYPING['group-id'].__name__)}, not {repr(type(group_id).__name__)}"
            )

        if type(userbot_session_name) is not CONFIG_TYPING["userbot-session-name"]:
            raise TypeError(
                f"'userbot_session_name' must be a {repr(CONFIG_TYPING['userbot-session-name'].__name__)}, not {repr(type(userbot_session_name).__name__)}"
            )

        self = super().__new__(cls)

        self.__api_id = api_id
        self.__api_hash = api_hash
        self.__userbot_phone = userbot_phone
        self.__bot_token = bot_token
        self.__channel_id = channel_id
        self.__group_id = group_id
        self.__userbot_session_name = userbot_session_name

        return self

    @classmethod
    def from_dict(cls, dct):
        if not isinstance(dct, dict):
            raise TypeError("'dct' must be a dict")

        in_keys = set(dct.keys())
        tp_keys = set(CONFIG_TYPING.keys())

        if in_keys != tp_keys:
            if in_keys & tp_keys == tp_keys:
                raise UnexpectedConfigurationArgumentsError(in_keys - tp_keys)
            else:
                raise RequiredConfigurationArgumentsError(tp_keys - in_keys)

        for k in tp_keys:
            if type(dct[k]) is not CONFIG_TYPING[k]:
                raise ConfigurationArgumentsTypeError(k, CONFIG_TYPING[k], type(dct[k]))

        return cls(
            api_id=dct["api-id"],
            api_hash=dct["api-hash"],
            userbot_phone=dct["userbot-phone"],
            bot_token=dct["bot-token"],
            channel_id=dct["channel-id"],
            group_id=dct["group-id"],
            userbot_session_name=dct["userbot-session-name"]
        )

    @classmethod
    def from_json(cls, string_or_fp):
        if isinstance(string_or_fp, str):
            return cls.from_dict(json.loads(string_or_fp))
        else:
            return cls.from_dict(json.load(string_or_fp))

    @property
    def api_id(self):
        return self.__api_id

    @property
    def api_hash(self):
        return self.__api_hash

    @property
    def userbot_phone(self):
        return self.__userbot_phone

    @property
    def bot_token(self):
        return self.__bot_token

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def group_id(self):
        return self.__group_id

    @property
    def userbot_session_name(self):
        return self.__userbot_session_name
