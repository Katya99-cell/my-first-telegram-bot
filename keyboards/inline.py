from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class InlineKeyboards:

    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:

        keyboard = InlineKeyboardMarkup (
            [
                [
                    InlineKeyboardButton (
                        text="Информация",
                        callback_data="info"
                    ),
                    InlineKeyboardButton (
                        text="Фото",
                        callback_data="photo"
                    ),

                ],
                [
                    InlineKeyboardButton (
                        text="Опрос",
                        callback_data="survey"
                    ),
                    InlineKeyboardButton (
                        text="Закрыть",
                        callback_data="close"
                    ),
                ]
            ]
        )
        return keyboard

    @staticmethod
    def pagination(page: int, total_pages: int):

        buttons = []

        if page > 0:
            buttons.append(
                InlineKeyboardButton(text="Назад", callback_data=f"page_{page-1}")
            )
        buttons.append(
            InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data="current")
        )

        if page < total_pages - 1:
            buttons.append(
                InlineKeyboardButton(text="Вперед", callback_data=f"page_{page+1}")
        ) 

        return InlineKeyboardMarkup(inline_keyboard=[buttons])