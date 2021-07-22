from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.schema import ForeignKey
import os


engine = create_engine(os.getenv("SECONDARY_DATABASE_URL"))
Base = declarative_base()


class Repository(Base):
    __tablename__ = "Repository"

    name = Column(String, primary_key=True, nullable=False)
    packages = relationship("Package")

    def __repr__(self) -> str:
        return "<(name={0.name}, packages={0.packages})>".format(self)


class Package(Base):
    __tablename__ = "Package"

    placeholder = Column(Integer, primary_key=True, nullable=False)
    
    architecture = Column(String, nullable=False)
    author = Column(String, nullable=False)
    dependencies = Column(ARRAY(String), nullable=False)
    depiction = Column(String, nullable=False)
    description = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    free = Column(Integer, nullable=False)
    icon = Column(String, nullable=False)
    maintainer = Column(String, nullable=False)
    name = Column(String, nullable=False)
    package = Column(String, nullable=False)
    repo = Column(String, nullable=False)
    repo_name = Column(String, ForeignKey("Repository.name"), nullable=False)
    section = Column(String, nullable=False)
    tag = Column(ARRAY(String), nullable=False)
    version = Column(String, nullable=False)

    def __repr__(self) -> str:
        return "<architecture={0.architecture}, author={0.author}, dependencies={0.dependencies}, depiction={0.depiction}, description={0.description}, filename={0.filename}, free={0.free}, icon={0.icon}, maintainer={0.maintainer}, name={0.name}, package={0.package}, repo={0.repo}, repo_name={0.repo_name}, section={0.section}, tag={0.tag}, version={0.version}>".format(self)

    def to_dict(self) -> dict:
        return {
            "architecture": self.architecture,
            "author": self.author,
            "dependencies": self.dependencies,
            "depiction": self.depiction,
            "description": self.description,
            "filename": self.filename,
            "free": True if self.free == 1 else False,
            "icon": self.icon,
            "maintainer": self.maintainer,
            "name": self.name,
            "package": self.package,
            "repo": self.repo,
            "repo name": self.repo_name,
            "section": self.section,
            "tag": self.tag,
            "version": self.version
        }


SessionObject = sessionmaker(bind=engine)
db: Session = SessionObject()
