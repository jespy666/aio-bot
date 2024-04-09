from aiogram.filters import Command
from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from openai import OpenAI

from config import config
from bot.states import AskStates


gpt_router = Router()
client = OpenAI(api_key=config.OPENAI_KEY)


@gpt_router.message(Command('ask'))
async def ask(message: types.Message, state: FSMContext) -> None:
    await message.answer('🔽 Задайте мне вопрос 🔽')
    await state.set_state(AskStates.WaitingForQuestion)


async def process_question(message: types.Message, state: FSMContext):
    question = message.text
    response = client.chat.completions.create(
        model=config.GPT_MODEL,
        messages=[
            {"role": "user", "content": question},
        ]
    )
    answer = response.choices[0].message
    print(answer)
    await message.answer(str(answer))
    await state.clear()
