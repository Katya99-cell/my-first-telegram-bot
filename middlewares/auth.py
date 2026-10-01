# Содержимое файла middlewares/auth.py
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

class AdminMiddleware(BaseMiddleware):
    def __init__(self):
        self.admin_ids = [7965113363]  # Ваш ID
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        if user.id not in self.admin_ids:
            if isinstance(event, Message):
                await event.answer("У вас отсутствует доступ к данному боту.")
            return  # Сбрасываем апдейт, дальше он не пойдет

        return await handler(event, data)
