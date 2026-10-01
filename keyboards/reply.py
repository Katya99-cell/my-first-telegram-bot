from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    ReplyKeyboardRemove
)

class Keyboards:

    @staticmethod
    def main_menu():
        # Создаем старые кнопки
        btn_start = KeyboardButton(text="Старт")
        btn_photo = KeyboardButton(text="Фото")
        
        # Кнопки для запуска опросов
        btn_survey = KeyboardButton(text="Опрос")
        btn_inline_survey = KeyboardButton(text="Инлайн-опрос")
        
        # Кнопка Помощь и новая кнопка История!
        btn_help = KeyboardButton(text="Помощь")
        btn_history = KeyboardButton(text="История") 

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [btn_start, btn_photo], 
                [btn_survey, btn_inline_survey],  
                [btn_help, btn_history] # Теперь кнопка "История" на месте!
            ],
            resize_keyboard=True,
            one_time_keyboard=False,
        )
        return keyboard

    @staticmethod
    def photo_menu():
        """Создает инлайн-клавиатуру для меню фото"""
        btn_random = InlineKeyboardButton(text="Случайное фото", callback_data="photo_random")
        btn_cnl = InlineKeyboardButton(text="Назад", callback_data="photo_back")

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [btn_random], 
                [btn_cnl]
            ]
        )
        return keyboard

    @staticmethod
    def remove():
        """Удаляет Reply-клавиатуру"""
        return ReplyKeyboardRemove()
