from dataclasses import dataclass

from openai import OpenAI

from storage.models import User

from config import config

from bot import exceptions as e


@dataclass
class DialogueBase:

    client: OpenAI
    user: User
    model: str

    def __post_init__(self) -> None:
        model_info: tuple | None = config.GPT_MODELS.get(self.model)
        if not model_info:
            raise e.IncorrectModelError
        self.model: str = model_info[0]
        self.field_name: str = model_info[1]
        self.requests: int = getattr(self.user, self.field_name)
        self.check_requests_amount()

    def check_requests_amount(self) -> None:
        if self.requests <= 0:
            raise e.InsufficientFundsError

    def get_field_name(self) -> str:
        return self.field_name

    def get_requests_amount(self) -> int:
        return self.requests

    def decrease_requests_count(self) -> None:
        self.requests -= 1
