from telegram.ext import ApplicationBuilder, CommandHandler

from bot.main import start
from core.settings import BOT_TOKEN


def main():
    from core import settings
    from utils import localization

    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.run_polling()


if __name__ == '__main__':
    main()
