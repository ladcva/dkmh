from sqlalchemy import ARRAY, BigInteger, Column, DateTime, Identity, Integer, PrimaryKeyConstraint, create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database
from config.default import POSTGRES_CONN_STRING
from db_migration import init_load


base = declarative_base()

class SemesterSnapshot(base):
    __tablename__ = 'semester_snapshot'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='id'),
    )

    id = Column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    list_semester_id = Column(ARRAY(Integer()))
    details = Column(JSONB)
    start_time = Column(DateTime)
    end_time = Column(DateTime)


if __name__ == '__main__':

    # To create table and database dkmh
    engine = create_engine(POSTGRES_CONN_STRING, echo=True)
    # base.metadata.create_all(engine, checkfirst=True)
    
    if not database_exists(engine.url):
        create_database(engine.url)
        base.metadata.create_all(engine, checkfirst=True)
        init_load.init_load()
    else:
        base.metadata.create_all(engine, checkfirst=True)
        init_load.init_load()
