from openai import OpenAI
from random import choice

from config import config
from bot import exceptions as e


class DialogueManager:

    GREETINGS = (
        'Приветствую! В чем я могу вам помочь сегодня?',
        'Рад видеть вас снова. Готов помочь в вашем запросе.',
        'Какие задачи я могу помочь вам решить?',
    )

    GOODBYES = (
        'Если возникнут новые вопросы, не стесняйтесь обращаться. Удачи!',
        'Буду ждать вашего следующего визита. Удачи в делах!',
        'Пока! A я всегда здесь, если вам понадобится помощь.',
    )

    def __init__(self, model: str, requests: int, context: list = None):
        self.client = OpenAI(api_key=config.OPENAI_KEY)
        self.context = context if context else []
        self.requests = requests
        self.model_name = model
        try:
            self.model = config.GPT_MODELS[model][0]
        except KeyError:
            raise e.IncorrectModelError
        self._check_requests_count()

    def get_greeting(self) -> str:
        return choice(self.GREETINGS)

    def get_goodbye(self) -> str:
        return choice(self.GOODBYES)

    def _check_requests_count(self) -> None:
        if self.requests <= 0:
            raise e.EmptyRequestsError

    def get_requests_count(self) -> int:
        return self.requests

    def get_field_name(self) -> str:
        return self.model_name

    def add_question_to_context(self, question: str) -> None:
        self.context.append({"role": "user", "content": question})

    def _add_answer_to_context(self, ai_response: str) -> None:
        self.context.append({"role": "assistant", "content": ai_response})

    def get_ai_response(self) -> str:
        self._check_requests_count()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.context,
        )
        ai_response = response.choices[0].message.content
        self._add_answer_to_context(ai_response)
        self._decrease_request_count()
        return ai_response

    def _decrease_request_count(self) -> None:
        self.requests -= 1

