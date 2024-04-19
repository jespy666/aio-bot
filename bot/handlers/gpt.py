from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from bot import TextDialogueStates
from bot.keyboards import CancelKB, InlineMenu, DialogueKB
from ai.text import DialogueManager
from storage import crud

from storage.models import User
from ..wrappers import check_user, validators

from config import config


gpt_router = Router()


@gpt_router.message(Command('ask'))
@check_user(with_kwargs=True)
async def ask_model(message: Message, state: FSMContext, **kwargs) -> None:
    session: AsyncSession = kwargs.get('session')
    user: User = kwargs.get('user')
    cancel_btn = CancelKB().place()
    kb = DialogueKB(config.GPT_MODELS.keys()).place()
    user_id = message.chat.id
    await state.update_data(
        session=session,
        user=user,
        user_id=user_id,
        cancel_btn=cancel_btn,
        models_kb=kb,
    )
    msg = (
        '👀 <em><strong>Выбор модели</strong></em>'
    )
    msg2 = (
        '🔽 <em>Выберите модель, которую хотите использовать</em> 🔽'
    )
    await message.answer(msg, reply_markup=cancel_btn)
    await message.answer(msg2, reply_markup=kb)
    await state.set_state(TextDialogueStates.choseModel)


@gpt_router.message(TextDialogueStates.choseModel)
@validators
async def chose_model(message: Message, state: FSMContext) -> None:
    model_name = message.text
    context = await state.get_data()
    user: User = context.get('user')
    cancel_btn = context.get('cancel_btn')
    requests: int = getattr(user, config.GPT_MODELS[model_name][1])
    dialogue = DialogueManager(model_name, requests)
    greeting = dialogue.get_greeting()
    await state.update_data(dialogue=dialogue)
    await message.answer(greeting, reply_markup=cancel_btn)
    await state.set_state(TextDialogueStates.supportDialogue)


@gpt_router.message(TextDialogueStates.supportDialogue)
@validators
async def support_dialogue(message: Message, state: FSMContext) -> None:
    question = message.text
    context = await state.get_data()
    dialogue: DialogueManager = context.get('dialogue')
    session: AsyncSession = context.get('session')
    cancel_btn = context.get('cancel_btn')
    dialogue.add_question_to_context(question)
    answer = dialogue.get_ai_response()
    requests: int = dialogue.get_requests_count()
    field_name: str = config.GPT_MODELS[dialogue.get_field_name()][1]
    await crud.update_user(session, message.chat.id, **{field_name: requests})
    await message.answer(answer, reply_markup=cancel_btn)
    await state.update_data(dialogue=dialogue)
    await state.set_state(TextDialogueStates.supportDialogue)


@gpt_router.callback_query(F.data == 'cancel')
async def cancel_callback(call: CallbackQuery, state: FSMContext):
    items = {
        'О боте': 'about',
        'Главная': 'start',
        'Начать новый диалог': 'ask',
    }
    menu = InlineMenu()
    context = await state.get_data()
    dialogue: DialogueManager | None = context.get('dialogue')
    if not dialogue:
        dialogue = DialogueManager(config.DEFAULT_GPT_MODEL, 1)
    goodbye = dialogue.get_goodbye()
    await call.message.answer(goodbye, reply_markup=menu.place(**items))
    await state.clear()


@gpt_router.callback_query(F.data == 'ask')
async def ask_callback(call: CallbackQuery, state: FSMContext) -> None:
    await ask_model(call.message, state)
