from aiogram.fsm.state import StatesGroup, State


class TextDialogueStates(StatesGroup):
    choseModel = State()
    supportDialogue = State()


class ImageDialogueStates(StatesGroup):
    model = State()
    size = State()
    quality = State()
    prompt = State()
