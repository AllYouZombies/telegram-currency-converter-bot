from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboard import get_kb
from bot.utils import track_and_route, save_kb_keys, description


@description(_('🏠 Home'))
@track_and_route()
async def menu_main(update: Update, context: ContextTypes.DEFAULT_TYPE, user, *args, **kwargs) -> None:
    buttons = [
        [_('⚙️ Settings'), _('❓ Help')],
    ]
    text = _('Hello, %s') % user.first_name
    kb = await get_kb(buttons)
    await save_kb_keys(context, buttons)
    await update.message.reply_text(text, reply_markup=kb)
