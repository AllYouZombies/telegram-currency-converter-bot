import asyncio

from sqlalchemy import Column, BigInteger, String, Boolean

from core.db import Base, Manager, engine
from core.settings import DEFAULT_LANGUAGE


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
    async def from_update(cls, update):
        defaults = {
            'first_name': update.effective_user.first_name,
            'last_name': update.effective_user.last_name,
            'username': update.effective_user.username,
        }

        user, created = await User.objects.update_or_create(user_id=update.effective_user.id, defaults=defaults)
        if created or not user.lock_lang:
            user.language_code = update.effective_user.language_code
            await user.objects.session.commit()
        return user


# Add a custom manager to the models
setattr(User, 'objects', Manager(User))
