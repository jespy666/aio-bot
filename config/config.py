from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
GPT_MODEL = os.getenv('GPT_MODEL')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
