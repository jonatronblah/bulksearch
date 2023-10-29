from sqlalchemy.ext.declarative import declarative_base

from client_bulksearch.db.meta import meta


# class Base(DeclarativeBase):
#     """Base for all models."""

#     metadata = meta

Base = declarative_base()
