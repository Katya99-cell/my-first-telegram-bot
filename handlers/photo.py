from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

# ИСПРАВЛЕНО: Импортируем класс Keyboards
from keyboards.reply import Keyboards 

def register_photo_handlers(dp: Dispatcher):

    @dp.message(Command("photo"))
    @dp.message(F.text == "Фото")
    async def cmd_photo(message: Message):
        # ИСПРАВЛЕНО: Заменили ReplyKeyboards на Keyboards
        keyboard = Keyboards.photo_menu()
        await message.answer(
            "Вы перешли в меню управления фото. Выберите действие:",
            reply_markup=keyboard
        )

    @dp.message(F.photo)
    async def handle_user_photo(message: Message):
        # ИСПРАВЛЕНО: Заменили ReplyKeyboards на Keyboards
        keyboard = Keyboards.photo_menu()
        photo_id = message.photo[-1].file_id
        
        await message.reply(
            f"Фото получено и принято в обработку!\n"
            f"💾 <b>ID файла:</b> <code>{photo_id}</code>",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    @dp.callback_query(F.data == "photo_random")
    async def process_random_photo(callback: CallbackQuery):
        await callback.message.answer_photo(
            photo="https://picsum.photos", 
            caption="Вот твое случайное фото! 🌟"
        )
        await callback.answer()

    @dp.callback_query(F.data == "photo_back")
    async def process_photo_back(callback: CallbackQuery):
        # ИСПРАВЛЕНО: Заменили ReplyKeyboards на Keyboards
        main_keyboard = Keyboards.main_menu() 
        await callback.message.answer(
            "Возвращаюсь в главное меню.",
            reply_markup=main_keyboard
        )
        await callback.message.delete()
        await callback.answer()
