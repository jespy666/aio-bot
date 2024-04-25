from typing import Literal

from openai import OpenAI

from .dialogue import DialogueBase

from storage.models import User


class ImageEditor(DialogueBase):

    MODEL = 'DALL-E 2'

    def __init__(
            self,
            client: OpenAI,
            user: User,
            original_img_path: str,
            erased_img_path: str,
    ) -> None:
        super().__init__(client, user, self.MODEL)
        self.original_img_path = original_img_path
        self.erased_img_path = erased_img_path

    async def edit_image(
            self,
            prompt: str,
            output_size: Literal["256x256", "512x512", "1024x1024"]
    ) -> str:

        self.check_requests_amount()
        response = self.client.images.edit(
            image=open(self.original_img_path, 'rb'),
            mask=open(self.erased_img_path, 'rb'),
            prompt=prompt,
            n=1,
            size=output_size,
        )
        image_url = response.data[0].url
        return image_url
