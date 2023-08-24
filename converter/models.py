from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Float, select, desc, func, and_

from core.db import Base, session_scope


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    from_currency = Column(String, nullable=False)
    to_currency = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    source = Column(String, nullable=True)
    buy_rate = Column(Float, nullable=True)
    sell_rate = Column(Float, nullable=True)

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
            subquery = (
                select(cls.source, func.max(cls.created_at).label('max_created_at'))
                .filter_by(from_currency=from_currency, to_currency=to_currency)
                .group_by(cls.source)
                .alias()
            )

            query = (
                select(cls)
                .join(
                    subquery,
                    and_(
                        cls.source == subquery.c.source,
                        cls.created_at == subquery.c.max_created_at
                    )
                )
            )

            result = await session.execute(query)
            results = result.scalars().all()
            return results
