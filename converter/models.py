from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Float, select, desc

from core.db import Base, session_scope


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    from_currency = Column(String, nullable=False)
    to_currency = Column(String, nullable=False)
    rate = Column(Float, nullable=False)

    @classmethod
    async def get_rate(cls, from_currency: str | float | int, to_currency: str | float | int) -> 'ExchangeRate':
        """
        Get the latest exchange rate for the given currencies.

        :param from_currency: The currency to convert from.
        :param to_currency: The currency to convert to.
        :return: The ExchangeRate instance.
        """

        async with session_scope() as session:
            result = await session.execute(
                select(cls).filter_by(from_currency=from_currency, to_currency=to_currency).order_by(desc(cls.created_at))
            )
            instance = result.scalars().first()
            return instance
