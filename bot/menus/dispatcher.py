import logging
import os

from telegram import Update

from bot.utils import show_typing, assign_user_and_localize
from core.settings import BASE_DIR
from utils.localization import rev_translate


logging = logging.getLogger(__name__)


def _get_modules():
    _modules = os.listdir(os.path.join(BASE_DIR, 'bot', 'menus'))
    for x in _modules:
        if (os.path.isfile(os.path.join(BASE_DIR, 'bot', 'menus', x))
                and not x.startswith('_')
                and not x.startswith('dispatcher')):
            yield x


async def _get_handler(modules, func_name):
    for _module in modules:
        _module = __import__('bot.menus.%s' % _module[:-3], fromlist=['bot.menus'])
        _funcs = [cmd for cmd in dir(_module) if callable(getattr(_module, cmd))]
        _func_name = next((cmd for cmd in _funcs if rev_translate(getattr(_module, cmd).__doc__) == func_name), None)
        _handler = getattr(_module, func_name, None) or (getattr(_module, _func_name, None) if _func_name else None)
        if _handler:
            return _handler
    return None


@show_typing()
@assign_user_and_localize()
async def menu_dispatcher(update: Update, context, user, *args, **kwargs) -> None:
    """
    Menu button dispatcher.
    This method is called when user clicks on a menu button.
    It calls corresponding menu handler.

    :param update: Update instance
    :param context: Context instance
    :param user: User instance
    """

    router = context.user_data['router']
    input_text = update.message.text
    if input_text == _('🏠 Home'):
        router['next_menu'] = None
    next_menu = router.pop('next_menu', None)
    if input_text == _('⬅️ Back'):
        router['next_menu'] = None
        if router['history']:
            current_menu = router['history'].pop()
            while router['history'] and router['history'][-1] == current_menu:
                current_menu = router['history'].pop()
        next_menu = router['history'][-1] if router['history'] else None
    if not next_menu:
        current_kb_keys = router.get('current_kb_keys')
        if current_kb_keys and input_text in current_kb_keys:
            next_menu = rev_translate(input_text)
    else:
        args = (input_text, *args)
    modules = _get_modules()
    handler = await _get_handler(modules, next_menu if next_menu else 'menu_main')
    if handler:
        return await handler(update, context, user, *args, **kwargs)
    else:
        logging.error('No menu handler found for %s.' % next_menu)
        return await menu_no_handler(update, context, user, *args, **kwargs)


async def menu_no_handler(update: Update, context, user, *args, **kwargs) -> None:
    """
    Default handler for unknown commands.
    """
    text = _('Sorry, I don\'t understand you.')
    await update.message.reply_text(text)
