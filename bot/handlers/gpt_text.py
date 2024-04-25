from openai import OpenAI

from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from ..states import TextStates
from bot.keyboards import CancelKB, InlineMenu, DialogueKB

from ai.text import TextDialogue

from storage.models import User
from storage import crud

from ..wrappers import validators

from config import config


gpt_text_router = Router()


@gpt_text_router.message(Command('ask'))
async def ask_model(message: Message, state: FSMContext, user: User) -> None:
    cancel_btn = CancelKB().place()
    kb = DialogueKB(config.TEXT_MODELS.keys()).place(
        placeholder='Выберите модель данных'
    )
    user_id = user.id
    await state.update_data(
        user_id=user_id,
        cancel_btn=cancel_btn,
        models_kb=kb,
    )
    msg = (
        '👀 <em><strong>Выбор модели</strong>\n\n'
        'Выберите модель, которую хотите использовать</em>'
    )
    msg2 = (
        '<em>*Для выбора модели,\nвоспользуйтесь'
        ' встроенной клавиатурой снизу</em>'
    )

    await message.answer(msg, reply_markup=cancel_btn)
    await message.answer(msg2, reply_markup=kb)
    await state.set_state(TextStates.choseModel)


@gpt_text_router.message(TextStates.choseModel)
@validators
async def chose_model(message: Message, state: FSMContext, user: User) -> None:
    model = message.text
    context = await state.get_data()
    cancel_btn = context.get('cancel_btn')
    client = OpenAI(api_key=config.OPENAI_KEY)
    dialogue = TextDialogue(client, user, model)
    greeting = dialogue.get_greeting()
    await state.update_data(dialogue=dialogue)
    await message.answer(greeting, reply_markup=cancel_btn)
    await state.set_state(TextStates.supportDialogue)


@gpt_text_router.message(TextStates.supportDialogue)
@validators
async def support_dialogue(
        message: Message,
        state: FSMContext,
        session: AsyncSession
) -> None:

    question = message.text
    context = await state.get_data()
    dialogue: TextDialogue = context.get('dialogue')
    user_id: int = context.get('user_id')
    cancel_btn = context.get('cancel_btn')
    dialogue.add_question_to_context(question)
    answer: str = dialogue.get_ai_response()
    requests: int = dialogue.get_requests_amount()
    field_name: str = dialogue.get_field_name()
    await crud.update_user(session, user_id, **{field_name: requests})
    await message.answer(answer, reply_markup=cancel_btn)
    await state.update_data(dialogue=dialogue)
    await state.set_state(TextStates.supportDialogue)


@gpt_text_router.callback_query(F.data == 'cancel')
async def cancel_callback(
        callback: CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
        user: User
) -> None:

    items = {
        'О боте': 'about',
        'Главная': 'start',
        'Начать новый диалог': 'ask',
    }
    menu = InlineMenu().place(**items)
    context = await state.get_data()
    dialogue: TextDialogue | None = context.get('dialogue')
    if not dialogue:
        client = OpenAI(api_key=config.OPENAI_KEY)
        dialogue = TextDialogue(client, user, config.DEFAULT_GPT_MODEL)
    goodbye = dialogue.get_goodbye()
    await session.commit()
    await callback.message.answer(goodbye, reply_markup=menu)
    await state.clear()


@gpt_text_router.callback_query(F.data == 'ask')
async def ask_callback(
        callback: CallbackQuery,
        state: FSMContext,
        user: User
) -> None:

    await ask_model(callback.message, state, user)
