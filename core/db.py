from contextlib import asynccontextmanager

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.settings import DATABASE_URL

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
Base = declarative_base()

Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise
    finally:
        await session.close()


class Manager:

    def __init__(self, model):
        self.model = model

    async def _create_instance(self, defaults: dict = None, **kwargs):
        """
        Create an instance of the model.

        :param session: SQLAlchemy database session.
        :param params: The values to create the instance with.
        :return: Base instance.
        """

        params = {k: v for k, v in kwargs.items() if hasattr(self.model, k)}
        params.update(defaults or {})
        instance = self.model(**params)
        async with session_scope() as session:
            session.add(instance)
        return instance

    async def _get_instance(self, **kwargs):
        async with session_scope() as session:
            result = await session.execute(select(self.model).filter_by(**kwargs))
        instance = result.scalars().first()
        return instance

    async def get_or_create(self, defaults: dict = None, **kwargs) -> tuple:
        """
        Get an object if it exists, otherwise create it.

        :param defaults: Default values for the object.
        :param kwargs: The values to filter by.
        :return: A tuple with the object and a boolean indicating if it was created.
        """
        instance = await self._get_instance(**kwargs)
        if instance:
            return instance, False
        else:
            instance = await self._create_instance(defaults=defaults, **kwargs)
            return instance, True

    async def update_or_create(self, defaults: dict = None, **kwargs) -> tuple:
        """
        Update an object if it exists, otherwise create it.

        :param defaults: Default values for the object.
        :param kwargs: The values to filter by.
        :return: A tuple with the object and a boolean indicating if it was created.
        """

        instance = await self._get_instance(**kwargs)
        if instance:
            async with session_scope() as session:
                for k, v in defaults.items():
                    setattr(instance, k, v)
                    session.add(instance)
            return instance, False
        else:
            instance = await self._create_instance(defaults=defaults, **kwargs)
            return instance, True
