from sqlalchemy import create_engine
from sqlalchemy.ext import declarative
from sqlalchemy.orm import sessionmaker

from core.settings import DATABASE_URL

"""
Database engine and session factory.

Usage:
from core.db import Session

session = Session()
"""


# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a base class to define all the database subclasses
TableDeclarativeBase = declarative.declarative_base()

# Bind the engine to the metadata of the base class so that the
TableDeclarativeBase.TableDeclarativeBase.metadata.bind = engine

# Create all tables in the engine. This is equivalent to "Create Table"
TableDeclarativeBase.TableDeclarativeBase.metadata.create_all()

# Prepare the engine for declarative access
declarative.DeferredReflection.prepare(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
