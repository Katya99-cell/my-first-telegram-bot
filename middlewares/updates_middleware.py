from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message as TelegramMessage
from database.db import async_session, User, Message as DBMessage
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

class UpdatesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramMessage, Dict[str, Any]], Awaitable[Any]],
        event: TelegramMessage,
        data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, TelegramMessage) or not event.from_user:
            return await handler(event, data)

        user_id = event.from_user.id
        username = event.from_user.username
        text_content = event.text or "[Медиа/Другое]"

        async with async_session() as session:
            # Upsert пользователя (создаем, если нет, или обновляем username/last_seen)
            # Пример для SQLite (замените на pg_insert, если используете PostgreSQL)
            stmt = sqlite_insert(User).values(
                id=user_id, username=username
            ).on_conflict_do_update(
                index_elements=[User.id],
                set_={"username": username} # last_seen обновится автоматически через onupdate=func.now()
            )
            await session.execute(stmt)

            # Сохраняем историю сообщений (Задание 4)
            new_message = DBMessage(user_id=user_id, text=text_content)
            session.add(new_message)
            
            await session.commit()

        return await handler(event, data)
