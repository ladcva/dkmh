from sqlalchemy import ARRAY, BigInteger, DateTime, Identity, PrimaryKeyConstraint, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship


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
    
class ClassCodesSnapshot(base):
    __tablename__ = 'classes_snapshot'
    __table_args__ = (
        PrimaryKeyConstraint('class_id', name='class_id'),
    )
    class_id = Column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    code = Column(String,unique=True)
class Class(base):
    __tablename__ = 'classes'
    code = Column(String,primary_key=True)
    name = Column(String)
    semesters = relationship('Semester', secondary='class_semester_association')

class Semester(base):
    __tablename__ = 'semesters'
    id = Column(String, primary_key=True)
    name = Column(String)

class ClassSemesterAssociation(base):
    __tablename__ = 'class_semester_association'
    class_id = Column(String, ForeignKey('classes.code'), primary_key=True)
    semester_id = Column(String, ForeignKey('semesters.id'), primary_key=True)

class RecentSemesterClasses(base):
    __tablename__ = 'recent_semester_classes'
    class_code = Column(String, ForeignKey('classes.code'), primary_key=True)
    subject_name = Column(String)
    course_code = Column(String, primary_key=True)
    guid = Column(String, primary_key=True)
    semester_id = Column(String, ForeignKey('semesters.id'))
    room = Column(String)
    time_slot = Column(String)
    lecturer = Column(String)
    from_to = Column(String)

class UsersRegisteredClasses(base):
    __tablename__ = 'users_registrated_classes'     # fix loi chinh ta
    id = Column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    name = Column(String)
    cookie = Column(String)
    classes_registered = Column(String)