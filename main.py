from telegram.ext import ApplicationBuilder, CommandHandler

from bot.main import start
from core.settings import BOT_TOKEN
# from utils import localization
# from core import settings


bot = ApplicationBuilder().token(BOT_TOKEN).build()

bot.add_handler(CommandHandler("start", start))


def main():
    bot.run_polling()


if __name__ == '__main__':
    main()
