from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base
from config.default import POSTGRES_CONN_STRING

base = declarative_base()

class Class(base):
    __tablename__ = 'classes'
    code = Column(String,primary_key=True)
    name = Column(String)
    semesters = relationship('Semester', secondary='class_semester_association')

class Semester(base):
    __tablename__ = 'semesters'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class ClassSemesterAssociation(base):
    __tablename__ = 'class_semester_association'
    class_id = Column(String, ForeignKey('classes.code'), primary_key=True)
    semester_id = Column(Integer, ForeignKey('semesters.id'), primary_key=True)

class RecentSemesterClasses(base):
    __tablename__ = 'recent_semester_classes'
    id = Column(Integer, primary_key=True)
    class_code = Column(String, ForeignKey('classes.code'))
    semester_id = Column(Integer, ForeignKey('semesters.id'))
    room = Column(String)
    time_slot = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)


engine = create_engine(POSTGRES_CONN_STRING)
base.metadata.create_all(engine)