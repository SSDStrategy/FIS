from sqlalchemy import create_engine
from sqlalchemy.orm import create_session

engine = create_engine("sqlite+pysqlite:///db.sqlite", echo=True)
session = create_session(engine)

from data.models import *

Base.metadata.create_all(engine)
