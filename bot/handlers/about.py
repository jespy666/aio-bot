from aiogram.filters import Command
from aiogram import types, Router

from bot.keyboards.main_menu import MainMenu

about_router = Router()

msg = 'Здесь будет описание бота!'


@about_router.message(Command('about'))
async def about(message: types.Message) -> None:
    menu = MainMenu().place()
    await message.answer(
        msg,
        reply_markup=menu,
    )


async def about_callback(callback: types.CallbackQuery) -> None:
    menu = MainMenu().place()
    await callback.message.answer(
        msg,
        reply_markup=menu,
    )
