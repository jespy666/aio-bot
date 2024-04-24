from aiogram import Dispatcher

from .start import start_router
from .about import about_router
from .gpt_text import gpt_text_router
from .gpt_images import gpt_image_router
from .balance import balance_router

from storage.session import session_factory

from ..middlewares.session_mw import SessionMiddleware
from ..middlewares.user_mw import UserMiddleware


def register_routes(dp: Dispatcher) -> None:
    dp.include_router(start_router)
    dp.include_router(about_router)
    dp.include_router(gpt_text_router)
    dp.include_router(gpt_image_router)
    dp.include_router(balance_router)


def register_middlewares(dp: Dispatcher) -> None:
    dp.update.middleware(SessionMiddleware(session_pool=session_factory))
    dp.update.middleware(UserMiddleware(session_pool=session_factory))
