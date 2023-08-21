from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Float, select, desc

from core.db import Base, session_scope


def default_rate(context):
    return context.get_current_parameters()['rate']


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    from_currency = Column(String, nullable=False)
    to_currency = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    source = Column(String, nullable=True)
    buy_rate = Column(Float, nullable=True, default=default_rate)
    sell_rate = Column(Float, nullable=True, default=default_rate)

    @classmethod
    async def get_rates(cls,
                        from_currency: str | float | int,
                        to_currency: str | float | int) -> list:
        """
        Get the latest exchange rate for the given currencies.

        :param from_currency: The currency to convert from.
        :param to_currency: The currency to convert to.
        :return: The ExchangeRate instance.
        """

        async with session_scope() as session:
            query = select(cls).filter_by(
                from_currency=from_currency,
                to_currency=to_currency
            )
            query = query.order_by(desc(cls.created_at))

            result = await session.execute(query)
            results = result.scalars().all()
            return results
