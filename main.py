from app.config.settings import TELEGRAM_BOT_TOKEN
from app.database.init_db import initialize_database


def main():
    initialize_database(force_recreate=False)
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN is not set. Add it to .env before running the bot.")
        return
    from app.bot.telegram_bot import run_bot
    run_bot()


if __name__ == "__main__":
    main()
