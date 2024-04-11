bot:
		uvicorn bot.app:app --reload

sqlite3:
		python3 storage/sqlite.py
