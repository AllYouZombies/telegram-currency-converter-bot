from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import sessionmaker

from core.settings import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Manager:

    def __init__(self, model):
        self.model = model
        self.session = Session()

    async def _create_instance(self, session, defaults: dict = None, **kwargs):
        """
        Create an instance of the model.

        :param session: SQLAlchemy database session.
        :param params: The values to create the instance with.
        :return: Base instance.
        """

        params = {k: v for k, v in kwargs.items() if hasattr(self.model, k)}
        params.update(defaults or {})
        instance = self.model(**params)
        session.add(instance)
        await session.commit()
        return instance

    async def _get_instance(self, session, **kwargs):
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

        instance = await self._get_instance(self.session, **kwargs)
        if instance:
            return instance, False
        else:
            instance = await self._create_instance(self.session, defaults=defaults, **kwargs)
            return instance, True

    async def update_or_create(self, defaults: dict = None, **kwargs) -> tuple:
        """
        Update an object if it exists, otherwise create it.

        :param defaults: Default values for the object.
        :param kwargs: The values to filter by.
        :return: A tuple with the object and a boolean indicating if it was created.
        """

        instance = await self._get_instance(self.session, **kwargs)
        if instance:
            for k, v in defaults.items():
                setattr(instance, k, v)
            await self.session.commit()
            return instance, False
        else:
            instance = await self._create_instance(self.session, defaults=defaults, **kwargs)
            return instance, True
