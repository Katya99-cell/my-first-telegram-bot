import os
from dotenv import load_dotenv #? Для работы с переменными средами

class BotConfig:

    _token = None

    @classmethod
    def load(cls):

        load_dotenv() #? Для чтения переменных сред

        cls._token = os.getenv("BOT_TOKEN") #? Подгружаем токен

        if not cls._token:
            raise ValueError(
                "Токен бота не найден!"
            )

    @classmethod
    def get_token(cls): #? Для получения токена
        return cls._token

BotConfig.load()