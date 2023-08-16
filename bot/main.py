from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from core.settings import BOT_TOKEN
from utils.localization import activate_locale


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = update.effective_user.language_code
    activate_locale(lang)
    text = _('Hello, %s') % update.effective_user.first_name
    await update.message.reply_text(text)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", hello))

bot = app
