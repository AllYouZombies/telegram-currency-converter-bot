import datetime

from sqlalchemy import select, Date, cast, null, Float

from converter.models import ExchangeRate
from core.db import session_scope


class ExchangeRateSource:
    """
    Base class for integration with exchange rate sources.
    Sends requests to the given endpoint, parses the response and saves the exchange rate to the database.
    Returns the ExchangeRate instance.

    :param endpoint: The endpoint to send requests to.
    :param bulk: Whether to retrieve exchange rates in bulk or one by one.
    """

    source_name = ''
    endpoint = ''
    bulk = False
    coef = 1

    async def get_params(self, from_curr: str, to_curr: str) -> dict:
        """
        Get the parameters to send with the request.

        :param from_curr: The currency to convert from.
        :param to_curr: The currency to convert to.
        :return: The parameters.
        """

        pass

    async def get_rates(self):
        """
        Get the exchange rates for the given currencies.
        """

        pass

    async def get_rate(self, from_currency: str | float | int, to_currency: str | float | int):
        """
        Get the latest exchange rate for the given currencies.

        :param from_currency: The currency to convert from.
        :param to_currency: The currency to convert to.
        """

        raise NotImplementedError

    async def _check_existing(self,
                              from_currency: str,
                              to_currency: str,
                              rate: float,
                              source: str = source_name,
                              bank_name: str = None,
                              buy_rate: float = None,
                              sell_rate: float = None) -> bool:
        async with session_scope() as session:
            axisting = await session.execute(select(ExchangeRate).filter(
                cast(ExchangeRate.created_at, Date) == datetime.datetime.utcnow().date(),
                ExchangeRate.source == source,
                ExchangeRate.bank_name == bank_name,
                ExchangeRate.from_currency == from_currency,
                ExchangeRate.to_currency == to_currency,
                cast(ExchangeRate.rate, Float) == rate,
                cast(ExchangeRate.buy_rate, Float) == buy_rate if buy_rate else ExchangeRate.buy_rate.is_(null()),
                cast(ExchangeRate.sell_rate, Float) == sell_rate if sell_rate else ExchangeRate.sell_rate.is_(null())
            ))
            if len(axisting.scalars().all()) > 0:
                return True
        return False

    async def save_exchange_rate(self,
                                 from_curr: str,
                                 to_curr: str,
                                 rate: float,
                                 source: str = source_name,
                                 bank_name: str = None,
                                 buy_rate: float = None,
                                 sell_rate: float = None):
        """
        Save the exchange rate for the given currencies to the database.

        :param from_curr: The currency to convert from.
        :param to_curr: The currency to convert to.
        :param bank_name: Bank name
        :param source: The source of the exchange rate.
        :param buy_rate: The buy rate.
        :param sell_rate: The sell rate.
        :param rate: The exchange rate.
        """

        async with session_scope() as session:
            exchange_rate = ExchangeRate(from_currency=from_curr,
                                         to_currency=to_curr,
                                         rate=rate,
                                         source=source,
                                         bank_name=bank_name,
                                         buy_rate=buy_rate,
                                         sell_rate=sell_rate)
            session.add(exchange_rate)
