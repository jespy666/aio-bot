from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


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
