from sqlalchemy import Column, String, JSON, ARRAY, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os


engine = create_engine(os.getenv("DATABASE_URL"))
Base = declarative_base()


class Repository(Base):
    __tablename__ = "Repository"

    name = Column(String, primary_key=True, nullable=False)
    packages = Column(ARRAY(JSON), nullable=False)

    def __repr__(self) -> str:
        return "<(name={0.name}, packages={0.package})>".format(self)


class LastUpdate(Base):
    __tablename__ = "Last Update"

    title = Column(String, primary_key=True, nullable=False)
    update_date = Column(String, nullable=False)

    def __repr__(self) -> str:
        return "<(title={0.title}, update_date={0.update_date})>".format(self)


Base.metadata.create_all(engine)
SessionObject = sessionmaker(bind=engine)
db: Session = SessionObject()