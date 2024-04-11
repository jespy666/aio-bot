from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.states import AskStates
from bot.keyboards.cancel_kb import CancelKB
from bot.keyboards.inline_menu import InlineMenu
from ai.text import DialogueManager

from crud import UserCRUD
from config import config


gpt_router = Router()


@gpt_router.message(Command('ask'))
async def ask(message: Message, state: FSMContext) -> None:
    dialogue = DialogueManager()
    cancel_kb = CancelKB().place()
    session = UserCRUD(config.DATABASE_URL)
    await session.create_user(message.chat.first_name, message.chat.id)
    await state.update_data(dialogue=dialogue)
    greeting = dialogue.get_greeting()
    await message.answer(greeting, reply_markup=cancel_kb)
    await state.set_state(AskStates.dialogue)


@gpt_router.message(AskStates.dialogue)
async def continue_dialogue(message: Message, state: FSMContext) -> None:
    context = await state.get_data()
    dialogue: DialogueManager = context.get('dialogue')
    cancel_kb = CancelKB().place()
    question = message.text
    dialogue.add_user_message(question)
    answer = dialogue.get_ai_response()
    await message.answer(answer, reply_markup=cancel_kb)
    await state.update_data(dialogue=dialogue)
    await state.set_state(AskStates.dialogue)


@gpt_router.callback_query(F.data == 'cancel')
async def cancel_callback(call: CallbackQuery, state: FSMContext):
    items = {
        'О боте': 'about',
        'Главная': 'start',
        'Начать новый диалог': 'ask',
    }
    menu = InlineMenu()
    goodbye_msg = DialogueManager().get_goodbye()
    await call.message.answer(goodbye_msg, reply_markup=menu.place(**items))
    await state.clear()


@gpt_router.callback_query(F.data == 'ask')
async def ask_callback(call: CallbackQuery, state: FSMContext) -> None:
    await ask(call.message, state)
