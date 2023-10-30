from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey

db = SQLAlchemy(app)

class studentDetails(db.Model):
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    email_id = Column(String)
    password = Column(String)

class staffDetails(db.Model):
    user_id = Column(String, primary_key=True)
    user_name = Column(String)
    email_id = Column(String)
    password = Column(String)
    is_admin = Column(Boolean)

class course(db.Model):
    course_code=Column(String,primary_key=True)
    course_name=Column(String)
    course_type=Column(String)
    total_credits=Column(Integer)
    semester_in=Column(Integer)

class classTaken(db.Model):
    class_id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String, ForeignKey(course.course_code))
    class_date = Column(Date)
    class_hour = Column(Integer)

class attendance(db.Model):
    attendance_id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer,ForeignKey(classTaken.class_id))
    user_id = Column(Integer,ForeignKey(studentDetails.user_id))
    status = Column(Boolean)

class studentEnrolled(db.Model):
    enroll_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer,ForeignKey(studentDetails.user_id))
    course_code = Column(String,ForeignKey(course.course_code))

class teacherAssigned(db.Model):
    assigned_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String,ForeignKey(staffDetails.user_id))
    course_code = Column(String,ForeignKey(course.course_code))
