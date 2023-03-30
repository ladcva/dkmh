from sqlalchemy import create_engine, Column,String, PrimaryKeyConstraint, DateTime, BigInteger, Identity
from sqlalchemy.orm import declarative_base
from config.default import POSTGRES_CONN_STRING

base = declarative_base()

class class_codes_snapshot(base):
    __tablename__ = 'classes_snapshot'
    __table_args__ = (
        PrimaryKeyConstraint('class_id', name='class_id'),
    )
    class_id = Column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    code = Column(String,unique=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)


engine = create_engine(POSTGRES_CONN_STRING)
base.metadata.create_all(engine)

