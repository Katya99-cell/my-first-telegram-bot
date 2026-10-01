import logging 
import time
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

logger = logging.getLogger(__name__)

class LoggingMiddleWare(BaseMiddleware):

    async def __call__(
        self,
        # ИСПРАВЛЕНО: Корректная аннотация типов для хэндлера в aiogram 3
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        user = data.get("event_from_user")
        
        # ИСПРАВЛЕНО: Безопасное получение данных, если user окажется None
        if user:
            username = f"@{user.username}" if user.username else "без_юзернейма"
            user_info = f"{user.id} {username}"
        else:
            user_info = "Системное событие"

        # Заметьте: здесь мы определяем тип СОБЫТИЯ, а не ошибки
        if isinstance(event, Message): 
            event_type = "Сообщение"
            content = event.text or "<без текста>"
        elif isinstance(event, CallbackQuery):
            event_type = "Callback"
            content = event.data
        else:
            event_type = "Другое"
            content = "-"

        logger.info(f"[{event_type}] {user_info}: {content}")

        start = time.time()

        try:
            result = await handler(event, data)
            el = time.time() - start

            logger.info(f"Обработано за: {el:.3f} сек.")
            return result
            
        except Exception as er:
            el = time.time() - start
            logger.error(f"Ошибка за {el:.3f} сек: {er}")
            raise  # Инструкция raise пишется без круглых скобок
