from typing import Literal

from openai import OpenAI

from .dialogue import DialogueBase

from storage.models import User


class ImageGenerator(DialogueBase):

    def __init__(self, client: OpenAI, user: User, model: str) -> None:
        super().__init__(client, user, model)

    async def generate_image(
            self,
            prompt: str,
            size: Literal[
                "256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"
            ],
            quality: Literal["standard", "hd"] = 'standard'
    ) -> str:

        self.check_requests_amount()
        response = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
        )
        image_url = response.data[0].url
        return image_url
