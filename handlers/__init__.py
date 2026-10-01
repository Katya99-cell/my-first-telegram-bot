from aiogram import Dispatcher
from .start import register_start_handlers
from .photo import register_photo_handlers
from .survey import register_survey_handlers
from .history import register_history_handlers
from .stats import register_stats_handlers
from .inline import register_inline_handlers
from .others import register_others_hendlers

def register_all_handlers(dp: Dispatcher):

    register_start_handlers(dp)

    register_photo_handlers(dp)

    register_survey_handlers(dp)

    register_history_handlers(dp)

    register_stats_handlers(dp)

    register_inline_handlers(dp)

    register_others_hendlers(dp)

    print("все обработчики зарегестрированы!")