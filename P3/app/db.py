import os
import sys

sys.path.append(os.getcwd())


from datetime import datetime

from sqlalchemy import create_engine, desc
from sqlalchemy import (CheckConstraint, UniqueConstraint,
    Column, DateTime, Integer, String)

from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///migrations_test.db')

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        UniqueConstraint('student_email',
            name='unique_email'),
        CheckConstraint('student_grade BETWEEN 1 AND 12',
            name='grade_between_1_and_12'))

    student_id = Column(Integer(), primary_key=True)
    student_name = Column(String(), index=True)
    student_email = Column(String(55))
    student_grade = Column(Integer())
    student_birthday = Column(DateTime())
    student_enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.student_id}: " \
            + f"{self.student_name}, " \
            + f"Grade {self.student_grade}"
