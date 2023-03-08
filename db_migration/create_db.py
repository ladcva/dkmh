from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Define the database engine
engine = create_engine('sqlite:///', echo=True)

# Define the base class
Base = declarative_base()

# Define the Subject table
class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    classes = relationship('Class', secondary='subject_class')

# Define the Class table
class Class(Base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True)
    code = Column(String)
    semester_id = Column(Integer, ForeignKey('semester.id'))
    semester = relationship('Semester', back_populates='classes')

# Define the Subject_Class association table
subject_class = Table('subject_class', Base.metadata,
                      Column('subject_id', Integer, ForeignKey('subject.id')),
                      Column('class_id', Integer, ForeignKey('class.id')))

# Define the Semester table
class Semester(Base):
    __tablename__ = 'semester'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    classes = relationship('Class', back_populates='semester')

# Define the Historical_Semester table
class HistoricalSemester(Base):
    __tablename__ = 'historical_semester'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

# Create the database tables
Base.metadata.create_all(engine)
