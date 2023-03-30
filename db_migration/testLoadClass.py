from sqlalchemy import create_engine, Column,String
from sqlalchemy.orm import declarative_base
from config.default import POSTGRES_CONN_STRING

base = declarative_base()

class class_codes_snapshot(base):
    __tablename__ = 'classes_snapshot'
    code = Column(String,primary_key=True)


engine = create_engine(POSTGRES_CONN_STRING)
base.metadata.create_all(engine)

