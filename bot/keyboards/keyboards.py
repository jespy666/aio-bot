from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class InlineMenu:

    def __init__(self):
        self.kb = InlineKeyboardBuilder()

    def place(self, **kwargs):
        for item, callback in kwargs.items():
            self.kb.button(
                text=item,
                callback_data=callback,
            )
        self.kb.adjust(2)
        return self.kb.as_markup()


class DialogueKB:

    def __init__(self, buttons: list):
        self.buttons = [[KeyboardButton(text=button) for button in buttons]]

    def place(self, placeholder=None) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=self.buttons,
            is_persistent=False,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=placeholder,
        )


class CancelKB:

    def __init__(self):
        self.kb = InlineKeyboardBuilder()
        self.cancel_button = InlineKeyboardButton(
            text='Завершить общение',
            callback_data='cancel',
        )

    def place(self):
        self.kb.add(self.cancel_button)
        self.kb.adjust(1)
        return self.kb.as_markup()
