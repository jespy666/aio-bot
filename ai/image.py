# from openai import OpenAI
# from config import config
# #
# #
# client = OpenAI(api_key=config.OPENAI_KEY)
#
# response = client.chat.completions.create(
#     model=config.GPT_MODEL,
#     messages=[
#         {'role': 'user', 'content': 'сколько будет 2+2?'}
#     ]
# )
# print(response.choices[0].message.content)

# response = client.images.generate(
#   model="dall-e-3",
#   prompt="autistic wife",
#   size="1024x1024",
#   quality="standard",
#   n=1,
# )
#
# image_url = response.data[0].url
# print(image_url)
