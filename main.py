import asyncio  # Для асинхронной работы
import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import Bot, Dispatcher, F  # Основные классы для работы с ботом
from aiogram.filters import Command  # Для обработки команд
from aiogram.types import TelegramObject, Message, CallbackQuery, FSInputFile  # Для работы с сообщениями

from config import BotConfig
from handlers import register_all_handlers

# Импортируем middleware из папки middlewares (убедитесь, что там верный регистр букв W/w)
from middlewares.logging_middleware import LoggingMiddleWare
from middlewares.auth import AdminMiddleware
from middlewares.error_middleware import ErrorsMiddleware

from handlers import start
from handlers import history
from database.db import Database  


class TelegramBot:
    def __init__(self):
        # Инициализируем бота и диспетчер
        self.bot = Bot(token="8994837787:AAGRDC264FqoeDAHecQx1Cg_FthgQG8siQc")
        self.dp = Dispatcher()
        self.db = Database()
        
        # Сохраняем базу данных в контекст диспетчера aiogram
        self.dp['db'] = self.db 
        
        # Настраиваем все слои промежуточного ПО (включая защиту)
        self._setup_middlewares()
        
        # Передаем диспетчер для регистрации обработчиков
        register_all_handlers(self.dp)

        logging.info("Бот инициализирован...")

    def _setup_middlewares(self):
        """
        Регистрируем все middleware в правильном порядке.
        Запрос проходит сквозь них сверху вниз.
        """
        # 1. Логирование и обработка ошибок — на самый верхний уровень
        self.dp.update.outer_middleware(LoggingMiddleWare())
        self.dp.update.outer_middleware(ErrorsMiddleware(7965113363))
        
        # 2. Защита админки (AdminMiddleware) — проверяется перед тем, как запрос пойдет в хэндлеры
        self.dp.update.outer_middleware(AdminMiddleware())

    async def start(self):
        bot_info = await self.bot.me()
        print(f"Бот запущен!\nИмя бота: {bot_info.first_name}\nUsername: {bot_info.username}\nID: {bot_info.id}")
        
        # Запуск polling
        await self.dp.start_polling(self.bot, skip_updates=True)


async def main():
    bot = TelegramBot()
    await bot.start()


if __name__ == "__main__":
    # 1. Создаем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # Задаем общий уровень логирования

    # 2. Определяем формат логирования (дата, время, имя логгера, уровень, сообщение)
    log_formatter = logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 3. Настраиваем FileHandler (запись в файл bot.log в кодировке UTF-8)
    file_handler = logging.FileHandler(filename="bot.log", encoding="utf-8")
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    # 4. Настраиваем StreamHandler (вывод в консоль)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

    # Запускаем асинхронный процесс бота
    asyncio.run(main())
