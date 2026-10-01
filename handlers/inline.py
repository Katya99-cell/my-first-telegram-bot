import os
from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData

from database.db import Database

class InlineSurveyStates(StatesGroup):
    name = State()
    age = State()
    city = State()
    language = State()

class LanguageCallback(CallbackData, prefix="lang"):
    name: str

def register_inline_handlers(dp: Dispatcher):

    @dp.message(Command("inline_survey"))
    @dp.message(F.text == "Инлайн-опрос")
    async def cmd_survey(message: Message, state: FSMContext):
        await message.answer("Опрос запущен...\n\nКак тебя зовут?")
        await state.set_state(InlineSurveyStates.name)

    @dp.message(InlineSurveyStates.name)
    async def process_name(message: Message, state: FSMContext):
        if not message.text or message.text.startswith('/'):
            await message.answer("Пожалуйста, введите корректное имя.")
            return
        await state.update_data(name=message.text)
        await state.set_state(InlineSurveyStates.age)
        await message.answer("Сколько тебе лет?")

    @dp.message(InlineSurveyStates.age)
    async def process_age(message: Message, state: FSMContext):
        if not message.text or not message.text.isdigit():
            await message.answer("Ошибка. Введите число месяцев/лет...")
            return
        await state.update_data(age=int(message.text))
        await state.set_state(InlineSurveyStates.city)
        await message.answer("В каком городе ты живешь?")

    @dp.message(InlineSurveyStates.city)
    async def process_city(message: Message, state: FSMContext):
        if not message.text or message.text.startswith('/'):
            await message.answer("Пожалуйста, введите название города.")
            return
        await state.update_data(city=message.text)
        await state.set_state(InlineSurveyStates.language)

        inline_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Python 🐍", callback_data=LanguageCallback(name="Python").pack()),
                    InlineKeyboardButton(text="JavaScript 🟨", callback_data=LanguageCallback(name="JavaScript").pack())
                ],
                [
                    InlineKeyboardButton(text="C++ 🟦", callback_data=LanguageCallback(name="C++").pack()),
                    InlineKeyboardButton(text="Java ☕", callback_data=LanguageCallback(name="Java").pack())
                ]
            ]
        )
        await message.answer("Какой язык программирования ты изучаешь?", reply_markup=inline_kb)

    @dp.callback_query(InlineSurveyStates.language, LanguageCallback.filter())
    async def process_language(callback: CallbackQuery, callback_data: LanguageCallback, state: FSMContext, db: Database):
        await state.update_data(language=callback_data.name)
        user_data = await state.get_data()
        
        summary = (
            "🎉 **Опрос успешно завершен!**\n\n"
            f"👤 **Имя:** {user_data.get('name')}\n"
            f"🔢 **Возраст:** {user_data.get('age')}\n"
            f"🏙️ **Город:** {user_data.get('city')}\n"
            f"💻 **Изучаемый язык:** {user_data.get('language')}"
        )
        
        # Надежно сохраняем в базу данных
        try:
            await db.add_survey(
                user_id=callback.from_user.id,
                name=user_data.get('name'),
                age=user_data.get('age'),
                city=user_data.get('city'),
                language=user_data.get('language')
            )
        except Exception as e:
            print(f"Ошибка при записи опроса в БД: {e}")
        
        await callback.message.delete()
        
        # НАДЁЖНАЯ ПРОВЕРКА: Если локального файла "core/img 1.jpg" нет, шлем обычный красивый текст
        photo_path = "core/img 1.jpg"
        if os.path.exists(photo_path):
            photo = FSInputFile(photo_path)
            await callback.message.answer_photo(
                photo=photo,
                caption=summary,
                parse_mode="Markdown"
            )
        else:
            # Если картинки нет — просто отправляем текст без падений из-за внешних сайтов
            await callback.message.answer(
                text=summary,
                parse_mode="Markdown"
            )
        
        await callback.answer()
        await state.clear()
