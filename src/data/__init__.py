import os
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import create_session

sqlite = "db.sqlite"

if "PYTEST_RUN_CONFIG" in os.environ:
    sqlite = str(uuid.uuid1()) + '.sqlite'

print(f"database name: {sqlite}")

engine = create_engine("sqlite+pysqlite:///%s" % sqlite, echo=True)
session = create_session(engine)

from data.models import *

Base.metadata.create_all(engine)
