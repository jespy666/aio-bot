from aiogram.fsm.state import StatesGroup, State


class TextDialogueStates(StatesGroup):
    choseModel = State()
    supportDialogue = State()
