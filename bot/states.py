from aiogram.fsm.state import StatesGroup, State


class AskStates(StatesGroup):
    dialogue = State()
