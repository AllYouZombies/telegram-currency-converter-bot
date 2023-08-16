from sqlalchemy import Column, BigInteger, String

from core.db import TableDeclarativeBase


class User(TableDeclarativeBase):
    """
    A Telegram user who used the bot at least once.
    """

    # Telegram data
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    username = Column(String)
    language = Column(String, nullable=False)

    # Extra table parameters
    __tablename__ = "users"

