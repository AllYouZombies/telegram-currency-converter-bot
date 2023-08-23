import asyncio
import logging

from sqlalchemy import Column, BigInteger, String, Boolean
from telegram import Update

from core.db import Base, Manager, engine, session_scope
from core.settings import DEFAULT_LANGUAGE


log = logging.getLogger('users.models')


class User(Base):
    """
    A Telegram user who used the bot at least once.
    """

    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    username = Column(String)
    language_code = Column(String, nullable=False, default=DEFAULT_LANGUAGE)

    lock_lang = Column(Boolean, default=False)

    @classmethod
    async def from_update(cls, update: Update) -> 'User':
        """
        Get or create a user from the given update.

        :param update: Update instance
        :return: User instance
        """

        defaults = {
            'first_name': update.effective_user.first_name,
            'last_name': update.effective_user.last_name,
            'username': update.effective_user.username,
        }
        log.debug(f'Created default values: {defaults}')

        user, created = await User.objects.update_or_create(user_id=update.effective_user.id, defaults=defaults)
        log.debug(f'User: {user}, created: {created}')
        if created or not user.lock_lang:
            log.debug(f'Updating user language code: {update.effective_user.language_code}')
            async with session_scope() as session:
                user.language_code = update.effective_user.language_code
                session.add(user)
        return user


# Add a custom manager to the models
setattr(User, 'objects', Manager(User))
