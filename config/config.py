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
GPT_MODEL = os.getenv('GPT_MODEL')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
