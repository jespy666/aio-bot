import logging
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import register_routes, register_callback_query
from config import config


WEBHOOK_PATH = config.WEBHOOK_PATH
WEBHOOK_URL = config.WEBHOOK_URL + WEBHOOK_PATH

storage = MemoryStorage()

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=storage)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(url=WEBHOOK_URL)
    try:
        yield
    finally:
        await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)

register_routes(dp)
register_callback_query(dp)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s'
               u' [%(asctime)s] - %(name)s - %(message)s',
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
