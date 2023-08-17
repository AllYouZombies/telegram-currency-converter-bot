from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboard import Keyboard
from users.models import User
from utils.localization import activate_locale


async def _command_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = await User.from_update(update)
    lang = user.language_code
    activate_locale(lang)
    text = _('Hello, %s') % user.first_name
    keys = [
        (_('Just a button'), 'just_a_button'),
    ]
    kb = await Keyboard().get_inline_kb(keys)
    await update.message.reply_text(text, reply_markup=kb)
