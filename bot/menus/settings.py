from telegram import Update

from bot.keyboard import get_kb
from bot.utils import track_and_route, save_kb_keys, description


@description(_('⚙️ Settings'))
@track_and_route()
async def menu_settings(update: Update, context, user, *args, **kwargs) -> None:
    buttons = [
        [_('⬅️ Back'), _('🏠 Home')],
        [_('🌍 Language')],
    ]
    text = _('This is the settings menu. Select the desired option from the list below.')
    kb = await get_kb(buttons)
    await save_kb_keys(context, buttons)
    await update.message.reply_text(text, reply_markup=kb)
