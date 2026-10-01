from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Состояния опроса
class SurveyStates(StatesGroup):
    name = State()
    age = State()
    city = State()
    language = State()

def register_survey_handlers(dp: Dispatcher):

    # 1. Старт опроса (Срабатывает и на команду, и на кнопку из меню)
    @dp.message(Command("survey")) 
    @dp.message(F.text == "Опрос")  # <-- ИСПРАВЛЕНО: Теперь кнопка аккуратно встроена сюда
    async def cmd_survey(message: Message, state: FSMContext):
        await message.answer(
            "Опрос запущен...\nКак тебя зовут?",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(SurveyStates.name)

    # 2. Обработка имени
    @dp.message(SurveyStates.name)
    async def process_name(message: Message, state: FSMContext):
        if not message.text or message.text.startswith('/'):
            await message.answer("Пожалуйста, введите корректное имя.")
            return
            
        await state.update_data(name=message.text)
        await state.set_state(SurveyStates.age)
        await message.answer("Сколько тебе лет?")

    # 3. Обработка возраста
    @dp.message(SurveyStates.age)
    async def process_age(message: Message, state: FSMContext):
        if not message.text or not message.text.isdigit():
            await message.answer("Ошибка. Введите число...")
            return

        await state.update_data(age=int(message.text))
        await state.set_state(SurveyStates.city)
        await message.answer("В каком городе ты живешь?")

    # 4. Обработка города
    @dp.message(SurveyStates.city)
    async def process_city(message: Message, state: FSMContext):
        if not message.text or message.text.startswith('/'):
            await message.answer("Пожалуйста, введите название города.")
            return

        await state.update_data(city=message.text)
        await state.set_state(SurveyStates.language)
        
        # Создаем клавиатуру выбора языка программирования
        lang_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Python"), KeyboardButton(text="JavaScript")],
                [KeyboardButton(text="C++"), KeyboardButton(text="Java")]
            ],
            resize_keyboard=True
        )
        await message.answer("Какой язык программирования ты изучаешь?", reply_markup=lang_keyboard)

    # 5. Обработка языка и завершение опроса
    @dp.message(SurveyStates.language)
    async def process_language(message: Message, state: FSMContext):
        await state.update_data(language=message.text)
        
        # Получаем все сохраненные данные
        user_data = await state.get_data()
        
        # Формируем итоговый текст
        summary = (
            "Спасибо за ответы! Вот что мы записали:\n\n"
            f"👤 Имя: {user_data.get('name')}\n"
            f"🔢 Возраст: {user_data.get('age')}\n"
            f"🏙️ Город: {user_data.get('city')}\n"
            f"💻 Язык: {user_data.get('language')}"
        )
        
        await message.answer(summary, reply_markup=ReplyKeyboardRemove())
        await state.clear() # Сбрасываем состояние и очищаем данные FSM
