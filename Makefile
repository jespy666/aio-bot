.PHONY: migrations bot

bot:
		uvicorn bot.app:app --reload

migrations:
		alembic revision --autogenerate -m "$(name)"

migrate:
		alembic upgrade head

lint:
		ruff check .