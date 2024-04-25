from typing import Literal
import os

from tempfile import TemporaryDirectory

from openai import OpenAI

from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, Document
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardMarkup

from ai.image_editor import ImageEditor

from ..states import ImgEditStates
from ..keyboards import CancelKB, DialogueKB
from ..wrappers import validators
from ..validators import validate_input_file, validate_size

from storage.models import User

from config import config


gpt_img_edit_router = Router()

MODEL = 'DALL-E 2'


@gpt_img_edit_router.message(Command('edit'))
async def ask_original(
        message: Message,
        state: FSMContext,
        user: User
) -> None:

    cancel_btn: InlineKeyboardMarkup = CancelKB().place()
    user_id: int = user.id
    await state.update_data(
        user_id=user_id,
        cancel_btn=cancel_btn,
    )
    msg = (
        '<em><strong>Загрузка оригинальной картинки</strong>\n\n'
        'Загрузите изображение, которое хотите изменить\n\n'
        '❗️ Формат изображения ▶️ <strong>.PNG</strong>\n'
        '❗️ Изображение должно быть <strong>квадратным</strong></em>'
    )
    await message.answer(msg, reply_markup=cancel_btn)
    await state.set_state(ImgEditStates.original)


@gpt_img_edit_router.message(ImgEditStates.original)
@validators
async def ask_erased(message: Message, state: FSMContext) -> None:
    context = await state.get_data()
    cancel_btn: InlineKeyboardMarkup = context.get('cancel_btn')
    original_png: Document = message.document
    validate_input_file(original_png)
    temp_dir = TemporaryDirectory()
    original_img_path: str = os.path.join(temp_dir.name, 'original.png')
    await message.bot.download(
        file=original_png,
        destination=original_img_path
    )
    await state.update_data(
        temp_dir=temp_dir,
        original_img_path=original_img_path
    )
    msg = (
        '<em><strong>Загрузка маски для редактирования</strong>\n\n'
        'Загрузите изображение с вырезанной областью,'
        ' которую хотите изменить\n\n'
        '❗️ Формат изображения ▶️ <strong>.PNG</strong>\n'
        '❗️ Изображение должно быть <strong>квадратным</strong></em>'
    )
    await message.answer(msg, reply_markup=cancel_btn)
    await state.set_state(ImgEditStates.erased)


@gpt_img_edit_router.message(ImgEditStates.erased)
@validators
async def ask_size(message: Message, state: FSMContext) -> None:
    context = await state.get_data()
    cancel_btn: InlineKeyboardMarkup = context.get('cancel_btn')
    kb = DialogueKB(config.IMAGE_SIZES[MODEL]).place(
        placeholder='Выберите размер изображения'
    )
    erased_png: Document = message.document
    validate_input_file(erased_png)
    temp_dir: TemporaryDirectory = context.get('temp_dir')
    erased_img_path: str = os.path.join(temp_dir.name, 'erased.png')
    await message.bot.download(file=erased_png, destination=erased_img_path)
    await state.update_data(sizes_kb=kb, erased_img_path=erased_img_path)
    msg = (
        '<em><strong>Выберите размер изображения</strong></em>'
    )
    msg2 = (
        '<em>Необходимо выбрать размер генерируемой картинки</em>'
    )
    await message.answer(msg, reply_markup=cancel_btn)
    await message.answer(msg2, reply_markup=kb)
    await state.set_state(ImgEditStates.size)


@gpt_img_edit_router.message(ImgEditStates.size)
async def ask_prompt(message: Message, state: FSMContext) -> None:
    context = await state.get_data()
    cancel_btn: InlineKeyboardMarkup = context.get('cancel_btn')
    size: str = message.text
    validate_size(size, MODEL)
    msg = (
        '<em><strong>Введите запрос (prompt)\n\n'
        'Пример запроса:</strong>\n\n'
        '"Изображение кошки с зелеными глазами на траве"</em>'
    )
    await message.answer(msg, reply_markup=cancel_btn)
    await state.update_data(size=size)
    await state.set_state(ImgEditStates.prompt)


@gpt_img_edit_router.message(ImgEditStates.prompt)
async def edit_image(message: Message, state: FSMContext, user: User) -> None:
    context = await state.get_data()
    prompt: str = message.text
    client = OpenAI(api_key=config.OPENAI_KEY)
    temp_dir: TemporaryDirectory = context.get('temp_dir')
    original_img_path: str = context.get('original_img_path')
    erased_img_path: str = context.get('erased_img_path')
    size: Literal["256x256", "512x512", "1024x1024"] = context.get('size')
    dialogue = ImageEditor(client, user, original_img_path, erased_img_path)
    image_url: str = await dialogue.edit_image(prompt, size)
    await message.answer_photo(image_url, caption=prompt)
    temp_dir.cleanup()
    await state.clear()


@gpt_img_edit_router.callback_query(F.data == 'edit')
async def edit_callback(
        callback: CallbackQuery,
        state: FSMContext,
        user: User
) -> None:

    await ask_original(callback.message, state, user)
