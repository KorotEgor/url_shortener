from sqlalchemy import create_engine

from url_shortener.db.scheme import Base


db_engine = create_engine("sqlite://", echo=True)

Base.metadata.create_all(db_engine)
