#!/usr/bin/python3
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import scoped_session, sessionmaker
import sys


Base = declarative_base()

engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
session_factory = sessionmaker(
    bind=engine, expire_on_commit=False)
session = scoped_session(session_factory)

db_session = session()

from app.models.users import User
from app.models.place import Place

Base.metadata.create_all(engine)
