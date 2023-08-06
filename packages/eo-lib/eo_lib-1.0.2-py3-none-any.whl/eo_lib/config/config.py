from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "postgres://seon:seon@localhost/eo_lib/_ontology"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()

class Config():
	""" Represents an abstract class that will be used to another models."""

    def create_database(self):
        Base.metadata.create_all(engine)
