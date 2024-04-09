from aiogram import Dispatcher, F
from .start import start_router, start_callback
from .about import about_router, about_callback
from .gpt import gpt_router


def register_routes(dp: Dispatcher) -> None:
    dp.include_router(start_router)
    dp.include_router(about_router)
    dp.include_router(gpt_router)


def register_callback_query(dp: Dispatcher) -> None:
    dp.callback_query.register(about_callback, F.data == 'about')
    dp.callback_query.register(start_callback, F.data == 'start')
