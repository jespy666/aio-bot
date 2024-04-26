bot:
		uvicorn bot.app:app --reload

migrate:
		alembic upgrade head

lint:
		ruff check .