from aiogram.utils.keyboard import InlineKeyboardBuilder


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
