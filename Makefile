bot:
		uvicorn bot.app:app --reload

migrate:
		alembic upgrade head
