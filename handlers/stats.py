from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from database.db import async_session, User, Survey
from sqlalchemy import select, func
from database.db import Database

def register_stats_handlers(dp: Dispatcher):

    @dp.message(Command("stats"))
    async def cmd_stats(message: Message): 

        total_surveys = await Database.count_all_surveys()
        total_users = await Database.count_users()
        user_surveys = await Database.count_surveys_user(message.from_user.id)

        text = (
            "Статистика бота:\n\n"
            f"Всего пользоватлей: {total_users}\n"
            f"Всего опросов: {total_surveys}\n"
            f"Твоих опросов: {user_surveys}"
        )

        await message.answer(text)

