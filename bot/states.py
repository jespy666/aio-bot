from aiogram.fsm.state import StatesGroup, State


class TextStates(StatesGroup):
    choseModel = State()
    supportDialogue = State()


class ImgGenStates(StatesGroup):
    model = State()
    size = State()
    quality = State()
    prompt = State()


class ImgEditStates(StatesGroup):
    original = State()
    erased = State()
    size = State()
    prompt = State()
