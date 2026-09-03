import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Получаем токен бота
TOKEN = os.getenv("BOT_TOKEN")

# Инициализируем бота и диспетчер (переменные пишутся с маленькой буквы)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Код ответа должен быть внутри функции с правильным отступом
    await message.answer("HELLO!\nЯ твой персональный телеграм-бот")

@dp.message(Command("photo"))
async def cmd_photo(message: Message):
    # Используем готовую рабочую ссылку на картинку из интернета
    photo_url = "https://picsum.photos"
    
    # Отправляем фото напрямую через ссылку
    await message.answer_photo(
        photo=photo_url,
        caption="Ура! Картинка успешно загружена из интернета!"
    )
    await message.answer("Фото отправлено")
    
# Главная функция для запуска бота
async def main():
    print("Бот запущен и готов к работе!")
    # Удаляем вебхуки перед запуском polling, чтобы бот отвечал сразу
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Точка входа должна быть на самом верхнем уровне (без отступов)
if __name__ == "__main__":
    asyncio.run(main())
