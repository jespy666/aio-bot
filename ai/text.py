from openai import OpenAI
from random import choice

from config import config


class DialogueManager:

    greetings = (
        'Приветствую! В чем я могу вам помочь сегодня?',
        'Рад видеть вас снова. Готов помочь в вашем запросе.',
        'Какие задачи я могу помочь вам решить?',
    )

    goodbye_msgs = (
        'Если возникнут новые вопросы, не стесняйтесь обращаться. Удачи!',
        'Буду ждать вашего следующего визита. Удачи в делах!',
        'Пока! A я всегда здесь, если вам понадобится помощь.',
    )

    def __init__(self, context: list = None):
        self.client = OpenAI(api_key=config.OPENAI_KEY)
        self.context = context if context else []

    def get_greeting(self) -> str:
        return choice(self.greetings)

    def get_goodbye(self) -> str:
        return choice(self.goodbye_msgs)

    def add_user_message(self, question: str) -> None:
        self.context.append({"role": "user", "content": question})

    def get_ai_response(self) -> str:
        response = self.client.chat.completions.create(
            model=config.GPT_MODEL,
            messages=self.context,
        )
        ai_response = response.choices[0].message.content
        self._add_ai_message(ai_response)
        return ai_response

    def _add_ai_message(self, ai_response: str) -> None:
        self.context.append({"role": "assistant", "content": ai_response})
