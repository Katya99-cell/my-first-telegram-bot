from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from database.db import Database
from keyboards.reply import Keyboards

def register_start_handlers(dp: Dispatcher):

    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        keyboard = Keyboards.main_menu()
        await message.answer(
            "Привет!\nЯ твой персональный телеграм-бот.\nЧем могу быть полезен?",
            reply_markup=keyboard
        )
    @dp.message(Command("crash"))
    async def cmd_crash(message: Message):
        result = 1 / 0
        await message.answer(str(result))
        
    @dp.message(F.text == "Старт")
    async def handle_start_button(message: Message):
        keyboard = Keyboards.main_menu()
        await message.answer(
            "Я уже здесь!\nЧем могу быть полезен?",
            reply_markup=keyboard
        )

    @dp.message(F.text == "Помощь")
    @dp.message(Command("help"))
    async def handle_help_button(message: Message):
        await message.answer(
            "<b>ПОМОЩЬ:</b>\n"
            "Доступные команды:\n"
            "1. /start — главное меню\n"
            "2. /photo — показать фото\n"
            "3. /help — справочный материал\n"
            "4. /history — история опросов\n\n"
            "Используй кнопки внизу для навигации!",
            parse_mode="HTML"
        )
    
    # ХЭНДЛЕР-ЗАГЛУШКА ОТСЮДА УДАЛЕНА, ЧТОБЫ НЕ БЛОКИРОВАТЬ ДРУГИЕ ФАЙЛЫ
