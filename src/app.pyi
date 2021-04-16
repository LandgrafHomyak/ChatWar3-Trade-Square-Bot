from typing import NoReturn

from configuration import Configuration


class CW3TradeSquareBotApp:
    def __new__(cls, configuration: Configuration) -> CW3TradeSquareBotApp: ...

    def exec(self) -> int: ...

    def run_until_disconnected(self) -> NoReturn: ...
