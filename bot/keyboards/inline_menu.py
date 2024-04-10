from aiogram.utils.keyboard import InlineKeyboardBuilder


class MainMenu:

    def __init__(self):
        self.kb = InlineKeyboardBuilder()
        self.items = {}

    def place(self):
        for item, callback in self.items.items():
            self.kb.button(
                text=item,
                callback_data=callback,
            )
        self.kb.adjust(2)
        return self.kb.as_markup()
