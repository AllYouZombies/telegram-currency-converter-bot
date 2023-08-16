from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from core.settings import BOT_TOKEN
from users.models import User
from utils.localization import activate_locale


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = User.from_update(update)
    lang = user.language_code
    user.objects.session.close()
    activate_locale(lang)
    text = _('Hello, %s') % user.first_name
    await update.message.reply_text(text)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", hello))

bot = app
