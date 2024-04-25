from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

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
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

GPT_MODELS = {
    'GPT 3.5 Turbo': ('gpt-3.5-turbo', 'gpt3_requests'),
    'GPT 4': ('gpt-4', 'gpt4_requests'),
    'DALL-E 3': ('dall-e-3', 'image_requests'),
    'DALL-E 2': ('dall-e-2', 'image_requests'),
}

TEXT_MODELS = {
    'GPT 3.5 Turbo': ('gpt-3.5-turbo', 'gpt3_requests'),
    'GPT 4': ('gpt-4', 'gpt4_requests'),
}

IMAGE_MODELS = {
    'DALL-E 3': ('dall-e-3', 'image_requests'),
    'DALL-E 2': ('dall-e-2', 'image_requests'),
}

IMAGE_SIZES = {
    'DALL-E 3': ["1024x1024", "1792x1024", "1024x1792"],
    'DALL-E 2': ["256x256", "512x512", "1024x1024"],
}

DEFAULT_GPT_MODEL = 'GPT 3.5 Turbo'

DEFAULT_IMG_MODEL = 'DALL-E 2'
