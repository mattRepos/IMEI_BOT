from .white_list_middleware import WhiteListMiddleware
from .callback_answer_middleware import CallbackAnswerMiddleware


all_middlewares = [
    WhiteListMiddleware(),
    CallbackAnswerMiddleware()
]

