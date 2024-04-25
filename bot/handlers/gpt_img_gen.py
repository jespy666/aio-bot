from openai import OpenAI

from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from ai.image_generator import ImageGenerator

from ..states import ImgGenStates
from ..keyboards import CancelKB, DialogueKB
from ..wrappers import validators

from storage.models import User

from config import config


gpt_img_gen_router = Router()


@gpt_img_gen_router.message(Command('generate'))
async def ask_model(message: Message, state: FSMContext, user: User) -> None:
    cancel_btn = CancelKB().place()
    kb = DialogueKB(config.IMAGE_MODELS.keys()).place(
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
    await state.set_state(ImgGenStates.model)


@gpt_img_gen_router.message(ImgGenStates.model)
@validators
async def ask_size(message: Message, state: FSMContext) -> None:
    model = message.text
    kb = DialogueKB(config.IMAGE_SIZES[model]).place(
        placeholder='Выберите размер изображения'
    )
    context = await state.get_data()
    cancel_btn = context.get('cancel_btn')
    msg = (
        '<em>Выберите размер генерируемого изображения</em>'
    )
    msg2 = (
        f'<em>Для модели <strong>{model}</strong>\n'
        f'🔽Доступны следующие размеры 🔽</em>'
    )
    await message.answer(msg, reply_markup=cancel_btn)
    await message.answer(msg2, reply_markup=kb)
    await state.update_data(sizes_kb=kb, model=model)
    await state.set_state(ImgGenStates.size)


@gpt_img_gen_router.message(ImgGenStates.size)
@validators
async def ask_quality(message: Message, state: FSMContext) -> None:
    size = message.text
    kb = DialogueKB(['standard', 'hd']).place(
        placeholder='Выберите качество изображения'
    )
    context = await state.get_data()
    cancel_btn = context.get('cancel_btn')
    msg = (
        '<em>Выберите качество генерируемого изображения</em>'
    )
    msg2 = (
        '<em>*Высокое качество изображения\n'
        'расходует 2 запроса</em>'
    )
    await message.answer(msg, reply_markup=cancel_btn)
    await message.answer(msg2, reply_markup=kb)
    await state.update_data(quality_kb=kb, size=size)
    await state.set_state(ImgGenStates.quality)


@gpt_img_gen_router.message(ImgGenStates.quality)
@validators
async def ask_prompt(message: Message, state: FSMContext) -> None:
    quality = message.text
    context = await state.get_data()
    cancel_btn = context.get('cancel_btn')
    msg = (
        '<em><strong>Введите запрос (prompt)\n\n'
        'Пример запроса:</strong>\n\n'
        '"Изображение кошки с зелеными глазами на траве"</em>'
    )
    await message.answer(msg, reply_markup=cancel_btn)
    await state.update_data(quality=quality)
    await state.set_state(ImgGenStates.prompt)


@gpt_img_gen_router.message(ImgGenStates.prompt)
@validators
async def generate_image(
        message: Message,
        state: FSMContext,
        user: User
) -> None:

    prompt = message.text
    context = await state.get_data()
    model = context.get('model')
    size = context.get('size')
    quality = context.get('quality')
    client = OpenAI(api_key=config.OPENAI_KEY)
    dialogue = ImageGenerator(client, user, model)
    image_url = await dialogue.generate_image(prompt, size, quality)
    await message.answer_photo(image_url, caption=prompt)
    await state.clear()


@gpt_img_gen_router.callback_query(F.data == 'generate')
async def generate_callback(
        callback: CallbackQuery,
        state: FSMContext,
        user: User
) -> None:

    await ask_model(callback.message, state, user)
