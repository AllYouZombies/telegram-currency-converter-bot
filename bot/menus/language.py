import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboard import get_kb
from bot.menus.dispatcher import menu_dispatcher
from bot.utils import track_and_route, description, save_kb_keys
from core.db import session_scope
from core.settings import SUPPORTED_LANGS
from utils.localization import activate_locale

logging = logging.getLogger(__name__)


@description(_('🌍 Language'))
@track_and_route()
async def menu_language(update: Update, context: ContextTypes.DEFAULT_TYPE, user, *args, **kwargs) -> None:
    lang_name = next((i[1] for i in SUPPORTED_LANGS if i[0] == user.language_code), _('Unknown'))
    text = _('Your current language is %s.\n\nChoose your language from list below.') % lang_name
    buttons = [[_('⬅️ Back'), _('🏠 Home')]] + list(
        i[1] for i in SUPPORTED_LANGS if i[0] != user.language_code
    )
    kb = await get_kb(buttons)
    await save_kb_keys(context, buttons)
    context.user_data['router']['next_menu'] = '__set_language'
    await update.message.reply_text(text, reply_markup=kb)


async def __set_language(update: Update, context: ContextTypes.DEFAULT_TYPE, user, *args, **kwargs) -> None:
    chosen_lang = update.message.text
    lang_code, lang_name = next((i for i in SUPPORTED_LANGS if i[1] == chosen_lang), (None, None))
    if lang_code is None:
        context.user_data['router']['history'].pop()
        context.user_data['router']['next_menu'] = 'menu_language'
        return await menu_dispatcher(update, context, user, *args, **kwargs)
    elif lang_code == user.language_code:
        text = _('Your language is not changed.')
        await update.message.reply_text(text)
    else:
        async with session_scope() as session:
            user.language_code = lang_code
            user.lock_lang = True
            session.add(user)
        activate_locale(lang_code)
        text = _('Your language is changed to %s.') % lang_name
    context.user_data['router']['history'].pop()
    context.user_data['router']['next_menu'] = 'menu_settings'
    await update.message.reply_text(text)
    return await menu_dispatcher(update, context, user, *args, **kwargs)
