# from io import BytesIO
#
# from openai import OpenAI
# import base64
# from PIL import Image
#
# # from .dialogue import DialogueBase
#
#
# from config import config
#
#
# client = OpenAI(api_key=config.OPENAI_KEY)
# #
# #
# response = client.images.generate(
#       model="dall-e-2",
#       prompt="Красивый логотип нейросети",
#       size="256x256",
#       quality="standard",
#       response_format='b64_json',
#       n=1,
# )
# #
# # image_url = response.data[0].url
# # print(image_url)
#
# image_data = base64.b64decode(response.data[0].url)
# image = Image.open(BytesIO(image_data))
# print(image)
#
#
# # class ImageDialogue(DialogueBase):
# #     pass
