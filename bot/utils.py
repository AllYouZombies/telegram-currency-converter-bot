import logging

from users.models import User
from utils.localization import activate_locale


logging = logging.getLogger(__name__)


def show_typing():
    """
    Show typing status while processing func.
    """

    def wrapper(func):
        async def wrapped(update, context, *args, **kwargs):
            chat_id = update.effective_chat.id
            await context.bot.send_chat_action(chat_id=chat_id, action='typing')
            return await func(update, context, *args, **kwargs)

        return wrapped

    return wrapper


def description(text):
    """
    Set command description in docstring.

    :param text: Description text
    """
    def decorator(func):
        func.__doc__ = text
        return func

    return decorator


def assign_user_and_localize():
    """
    Assign user and localize the bot.
    """

    def wrapper(func):
        async def wrapped(update, context, *args, **kwargs):
            user = await User.from_update(update)
            lang = user.language_code
            activate_locale(lang)
            return await func(update, context, user, *args, **kwargs)
        return wrapped

    return wrapper


class History:
    max_size = 10

    def __iter__(self):
        return iter(self._history)

    def __len__(self):
        return len(self._history)

    def __getitem__(self, index):
        return self._history[index]

    def __init__(self):
        self._history = list()

    def __repr__(self):
        return self._history.__repr__()

    def __str__(self):
        return self._history.__str__()

    def add(self, item):
        logging.debug(f'Adding {item} to history.')
        if self._history and self._history[-1] == item:
            logging.debug(f'{item} is already in history. Skipping.')
            return
        if len(self._history) == self.max_size:
            self._history.pop(0)
        self._history.append(item)
        logging.debug(f'Added {item} to history. History: {self._history}')

    def pop(self):
        return self._history.pop()

    def clear(self):
        self._history.clear()


def track_and_route():
    """
    Track user's actions and route them to corresponding handlers.
    Save actions, menu history, current menu and other info to the context.
    """

    def wrapper(func):
        async def wrapped(update, context, *args, **kwargs):
            user_data = context.user_data
            router = user_data['router'] = user_data.get('router', dict())
            history = router['history'] = router.get('history', History())
            history.add(func.__name__)
            return await func(update, context, *args, **kwargs)
        return wrapped

    return wrapper


async def save_kb_keys(context, keys):
    """
    Save keyboard keys to the context.
    """

    def _flatten(list_obj):
        for item in list_obj:
            if isinstance(item, list):
                yield from _flatten(item)
            else:
                yield item

    keys = list(_flatten(keys))

    context.user_data['router']['current_kb_keys'] = keys
