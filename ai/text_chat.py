from openai import OpenAI

from random import choice

from storage.models import User

from .dialogue import DialogueBase


class TextDialogue(DialogueBase):

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

    def __init__(
            self,
            client: OpenAI,
            user: User,
            model: str,
            context: list = None
    ) -> None:

        super().__init__(client, user, model)
        self.context = context if context else []
        self.requests = self.get_requests_amount()

    def get_greeting(self) -> str:
        return choice(self.GREETINGS)

    def get_goodbye(self) -> str:
        return choice(self.GOODBYES)

    def add_question_to_context(self, question: str) -> None:
        self.context.append({"role": "user", "content": question})

    def _add_answer_to_context(self, ai_response: str) -> None:
        self.context.append({"role": "assistant", "content": ai_response})

    def get_ai_response(self) -> str:
        self.check_requests_amount()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.context,
        )
        ai_response = response.choices[0].message.content
        self._add_answer_to_context(ai_response)
        self.decrease_requests_count()
        return ai_response
