from aiogram import Dispatcher
from .start import start_router
from .about import about_router
from .gpt import gpt_router
from .balance import balance_router


def register_routes(dp: Dispatcher) -> None:
    dp.include_router(start_router)
    dp.include_router(about_router)
    dp.include_router(gpt_router)
    dp.include_router(balance_router)
