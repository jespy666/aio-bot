from dataclasses import dataclass
from typing import Dict, Union, Callable

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup
)


class InlineKeyboard:

    def __init__(self) -> None:
        self.kb = InlineKeyboardBuilder()

    def place(self, buttons: Dict[str: str]) -> InlineKeyboardMarkup:
        for item, callback in buttons.items():
            self.kb.button(text=item, callback_data=callback)
        self.kb.adjust(2)
        return self.kb.as_markup()


class ReplyKeyboard:
    @staticmethod
    def place(buttons: list, placeholder=None) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=button) for button in buttons]],
            is_persistent=False,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=placeholder,
        )
