from dotenv import load_dotenv
import os

load_dotenv()

# db settings
match os.getenv('DATABASE'):
    case db if db == 'sqlite':
        DATABASE_URL = 'sqlite+aiosqlite:///dev.db'
    case _:
        pass

# tg bot related settings
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')

# OpenAI related settings
IMAGE_MODEL = os.getenv('IMAGE_MODEL')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

GPT_MODELS = {
    'GPT 3.5 Turbo': ('gpt-3.5-turbo', 'gpt3_requests'),
    'GPT 4': ('gpt-4', 'gpt4_requests'),
}

DEFAULT_GPT_MODEL = 'GPT 3.5 Turbo'

