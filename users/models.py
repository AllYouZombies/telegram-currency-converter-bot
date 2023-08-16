from sqlalchemy import Column, BigInteger, String

from core.db import Base, Manager, engine


class User(Base):
    """
    A Telegram user who used the bot at least once.
    """

    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    username = Column(String)
    language_code = Column(String, nullable=False)

    @classmethod
    def from_update(cls, update):
        defaults = {
            'first_name': update.effective_user.first_name,
            'last_name': update.effective_user.last_name,
            'username': update.effective_user.username,
            'language_code': update.effective_user.language_code,
        }

        user, created = User.objects.update_or_create(user_id=update.effective_user.id, defaults=defaults)
        return user


# Add a custom manager to the models
setattr(User, 'objects', Manager(User))

# Create all tables in the engine. This is equivalent to "Create Table"
Base.metadata.create_all(engine)
