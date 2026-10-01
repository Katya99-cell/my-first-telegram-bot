from aiogram import Dispatcher, F
from aiogram.types import Message

def register_others_hendlers(dp: Dispatcher):

    @dp.message(F.text)
    async def handle_other_button(message: Message):

        if "привет" in message.text.lower():
            await message.answer("Снова привет! Я уже здесь!\nЧем могу быть полезен?")
        else:
            await message.answer("Я не понял твою команду.\nИспользуй стандартные команды или меню!...")