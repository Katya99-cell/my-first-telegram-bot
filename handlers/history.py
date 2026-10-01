from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database.db import Database
from keyboards.inline import InlineKeyboards

PAGE_SIZE = 3

def register_history_handlers(dp: Dispatcher):

    # 1. Вызов истории по команде или кнопке
    @dp.message(Command("history"))
    @dp.message(F.text == "История")
    async def cmd_history(message: Message):
        user_id = message.from_user.id
        # Вызываем метод напрямую через класс Database
        surveys = await Database.get_user_surveys(user_id)

        if not surveys:
            await message.answer("У тебя нет сохранённых опросов!\nПройди опрос: /inline_survey")
            return

        total_pages = (len(surveys) + PAGE_SIZE - 1) // PAGE_SIZE
        await show_page(message, surveys, page=0, total_pages=total_pages, edit=False)

    # 2. Функция отображения конкретной страницы истории
    async def show_page(message: Message, surveys: list, page: int, total_pages: int, edit: bool = False):
        start = page * PAGE_SIZE
        end = start + PAGE_SIZE
        page_items = surveys[start:end]

        text = f"📜 **История ваших опросов** (Страница {page + 1} из {total_pages}):\n\n"

        for i, survey in enumerate(page_items, start=start + 1):
            name, age, city, language, created_at = survey[:5]
            # Форматируем дату, если она пришла объектом datetime
            date_str = created_at.strftime('%d.%m.%Y %H:%M') if hasattr(created_at, 'strftime') else created_at
            text += (
                f"**Запись №{i}** ({date_str})\n"
                f"👤 Имя: {name}\n"
                f"🔢 Возраст: {age}\n"
                f"🏙️ Город: {city}\n"
                f"💻 Язык: {language}\n"
                f"───────────────────\n"
            )

        keyboard = InlineKeyboards.pagination(page, total_pages)

        if edit:
            try:
                await message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
            except Exception:
                await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
        else:
            await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

    # 3. Обработчик кликов пагинации
    @dp.callback_query(F.data.startswith("page_"))
    async def handle_pagination(callback: CallbackQuery):
        if callback.data == "page_noop":
            await callback.answer()
            return

        page = int(callback.data.split("_")[1])
        user_id = callback.from_user.id
        
        surveys = await Database.get_user_surveys(user_id)
        total_pages = (len(surveys) + PAGE_SIZE - 1) // PAGE_SIZE

        await show_page(callback.message, surveys, page, total_pages, edit=True)
        await callback.answer()

        # 4. Запрос на подтверждение очистки истории через команду или инлайн-кнопку
    @dp.message(Command("clear_history"))
    @dp.callback_query(F.data == "history_clear_confirm")
    async def confirm_clear(event: Message | CallbackQuery):
        user_id = event.from_user.id
        surveys = await Database.get_user_surveys(user_id)

        if not surveys:
            text_no_surveys = "У тебя нет опросов для удаления"
            if isinstance(event, CallbackQuery):
                await event.answer(text_no_surveys, show_alert=True)
            else:
                await event.answer(text_no_surveys)
            return

        confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да, удалить", callback_data="history_clear_yes"),
                InlineKeyboardButton(text="❌ Отмена", callback_data="history_clear_no")
            ]
        ])
        
        text_confirm = "⚠️ Вы уверены, что хотите полностью стереть историю ваших опросов?"
        
        if isinstance(event, CallbackQuery):
            await event.message.edit_text(text_confirm, reply_markup=confirm_kb)
            await event.answer()
        else:
            await event.answer(text_confirm, reply_markup=confirm_kb)
            
    # 6. Обработка отмены удаления истории
    @dp.callback_query(F.data == "history_clear_no")
    async def process_clear_no(callback: CallbackQuery):
        user_id = callback.from_user.id
        surveys = await Database.get_user_surveys(user_id)
        
        if not surveys:
            await callback.message.edit_text("У тебя нет сохранённых опросов!")
            await callback.answer()
            return
            
        total_pages = (len(surveys) + PAGE_SIZE - 1) // PAGE_SIZE
        
        # Безопасно перерисовываем первую страницу истории вместо кнопок подтверждения
        await show_page(callback.message, surveys, page=0, total_pages=total_pages, edit=True)
        await callback.answer("Удаление отменено")
    @dp.callback_query(F.data == "history_clear_yes")
    async def process_clear_yes(callback: CallbackQuery):
        user_id = callback.from_user.id
        
        # 1. Удаляем данные из базы через SQLAlchemy
        await Database.clear_user_history(user_id)
        
        # 2. Обязательно редактируем текст сообщения, убирая старые кнопки
        await callback.message.edit_text("🗑️ Вся ваша история опросов успешно и безвозвратно удалена!")
        
        # 3. Отвечаем на сам callback, чтобы кнопка перестала "мигать" или "зависать"
        await callback.answer()