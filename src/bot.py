from aiogram import Bot, Dispatcher


class BotManager:
    def __init__(
        self,
        dispatcher: Dispatcher | None = None,
        bot: Bot | None = None,
    ) -> None:
        self._dispatcher: Dispatcher = dispatcher
        self._bot: Dispatcher = bot

    def setup_dispatcher(self, dispatcher: Dispatcher) -> None:
        self._dispatcher = dispatcher

    def get_dispatcher(self) -> Dispatcher:
        return self._dispatcher

    def setup_bot(self, bot: Bot) -> None:
        self._bot = bot

    def get_bot(self) -> Bot:
        return self._bot
