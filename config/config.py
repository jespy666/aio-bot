from dotenv import load_dotenv
import os

load_dotenv()

# tg bot related settings
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')

# OpenAI related settings
GPT_MODEL = os.getenv('GPT_MODEL')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
