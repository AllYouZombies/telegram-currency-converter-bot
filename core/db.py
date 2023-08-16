from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import sessionmaker

from core.settings import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)


class Manager:

    def __init__(self, model):
        self.model = model
        self.session = Session()

    def _create_instance(self, session, defaults: dict = None, **kwargs):
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
        session.commit()
        return instance

    def _get_instance(self, session, **kwargs):
        instance = session.query(self.model).filter_by(**kwargs).first()
        return instance

    def get_or_create(self, defaults: dict = None, **kwargs) -> tuple:
        """
        Get an object if it exists, otherwise create it.

        :param defaults: Default values for the object.
        :param kwargs: The values to filter by.
        :return: A tuple with the object and a boolean indicating if it was created.
        """

        instance = self._get_instance(self.session, **kwargs)
        if instance:
            return instance, False
        else:
            instance = self._create_instance(self.session, defaults=defaults, **kwargs)
            return instance, True

    def update_or_create(self, defaults: dict = None, **kwargs) -> tuple:
        """
        Update an object if it exists, otherwise create it.

        :param defaults: Default values for the object.
        :param kwargs: The values to filter by.
        :return: A tuple with the object and a boolean indicating if it was created.
        """

        instance = self._get_instance(self.session, **kwargs)
        if instance:
            for k, v in defaults.items():
                setattr(instance, k, v)
            self.session.commit()
            return instance, False
        else:
            instance = self._create_instance(self.session, defaults=defaults, **kwargs)
            return instance, True
