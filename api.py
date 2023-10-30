from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from model import app
from model import *

api = Api(app)

stud_fields= {
   'user_id': fields.Integer,
   'user_name': fields.String,
   'email_id': fields.String,
   'password': fields.String
}

staff_fields= {
   'user_id': fields.String,
   'user_name': fields.String,
   'email_id': fields.String,
   'password': fields.String,
   'is_admin': fields.Boolean
}

course_fields= {
   'course_code': fields.String,
   'course_name': fields.String,
   'course_type': fields.String,
   'total_credits':fields.Integer,
   'semester_in': fields.Integer
}

enroll_fields= {
   'user_id': fields.Integer,
   'course_code': fields.String
}

student_get_args = reqparse.RequestParser()
student_get_args.add_argument("user_id", type=int, help="user_id is required", required=True)
student_get_args.add_argument("password", type=str, help="password is required", required=True)
student_get_args.add_argument("user_name", type=str)

student_post_args = reqparse.RequestParser()
student_post_args.add_argument("user_id", type=int, help="user_id is required", required=True)
student_post_args.add_argument("user_name", type=str, help="user_name is required", required=True)
student_post_args.add_argument("email_id", type=str, help="email_id is required", required=True)
student_post_args.add_argument("password", type=str, help="password is required", required=True)

student_put = reqparse.RequestParser()
student_put.add_argument("user_id", type=int, help="user_id is required", required=True)
student_put.add_argument("password", type=str, help="password is required", required=True)

staff_get = reqparse.RequestParser()
staff_get.add_argument("user_id", type=str, help="user_id is required", required=True)
staff_get.add_argument("password", type=str, help="password is required", required=True)
staff_get.add_argument("user_name", type=str)

staff_post = reqparse.RequestParser()
staff_post.add_argument("user_id", type=str, help="user_id is required", required=True)
staff_post.add_argument("user_name", type=str, help="user_name is required", required=True)
staff_post.add_argument("email_id", type=str, help="email_id is required", required=True)
staff_post.add_argument("password", type=str, help="password is required", required=True)
staff_post.add_argument("is_admin", type=bool, help = "are you a admin or not is must", required = True)

staff_put = reqparse.RequestParser()
staff_put.add_argument("user_id", type=str, help="user_id is required", required=True)
staff_put.add_argument("password", type=str, help="password is required", required=True)

course_get = reqparse.RequestParser()
course_get.add_argument("course_code", type=str, help="course_code is required", required=True)
course_get.add_argument("course_name", type=str)
course_get.add_argument("course_type", type=str)
course_get.add_argument("total_credits", type=int)
course_get.add_argument("semester_in", type=int)

course_post = reqparse.RequestParser()
course_post.add_argument("course_code", type=str, help="course_code is required", required=True)
course_post.add_argument("course_name", type=str, help="course_name is required", required=True)
course_post.add_argument("course_type", type=str, help="course_type is required", required=True)
course_post.add_argument("total_credits", type=int, help="total_credits is required", required=True)
course_post.add_argument("semester_in", type=int, help="semester_in is required", required=True)

enroll_get = reqparse.RequestParser()
enroll_get.add_argument("user_id", type=int, help="user_id is required", required=True)
enroll_get.add_argument("course_code", type=str, help="course_code is required", required=True)

enroll_post = reqparse.RequestParser()
enroll_post.add_argument("user_id", type=int, help="user_id is required", required=True)
enroll_post.add_argument("course_code", type=str, help="course_code is required", required=True)

class students(Resource):
    # to read from the database for login
    @marshal_with(stud_fields)
    def get(self): 
        args = student_get_args.parse_args()
        user = studentDetails.query.filter_by(user_id=args["user_id"]).first()
        if not user:
            abort(404, message="Could not find such user")
        elif user and args["password"] != user.password:
            abort(409, message="Incorrect password")
        args['user_name'] = user.user_name
        args['email_id'] = user.email_id
        return args
   
   # to store in database for registration
    @marshal_with(stud_fields)
    def post(self):
       args = student_post_args.parse_args()
       user = studentDetails.query.filter_by(user_id=args["user_id"]).first()
       if user:
          abort(409, message="user id already exists")
       addStudent = studentDetails(user_id = args["user_id"],user_name = args["user_name"],email_id = args["email_id"],password = args["password"])
       db.session.add(addStudent)
       db.session.commit()
       return args, 201
    
    # to update in db for forgot password
    @marshal_with(stud_fields)
    def put(self):
        args = student_put.parse_args()
        student = studentDetails.query.filter_by(user_id=args["user_id"]).first()
        if not student:
            abort(404, message = "student doesn't exist, cannot update")
        if args["password"]:
            student.password = args["password"]
        db.session.commit()
        return student, 201
    
class staffRegistration(Resource):
    @marshal_with(staff_fields)
    def get(self):
        args = staff_get.parse_args()
        staff = staffDetails.query.filter_by(user_id=args["user_id"]).first()
        if not staff:
            abort(404, message="Could not find such staff")
        elif staff and args["password"] != staff.password:
                abort(404, message="Incorrect password")
        args['user_name'] = staff.user_name
        args['email_id'] = staff.email_id
        return args
   
    @marshal_with(staff_fields)
    def post(self):
       args = staff_post.parse_args()
       staff = staffDetails.query.filter_by(user_id = args["user_id"]).first()
       if staff:
          abort(409, message="staff id already exists")
       addStaff = staffDetails(user_id = args["user_id"],user_name = args["user_name"],email_id = args["email_id"],password = args["password"],is_admin = args["is_admin"])
       db.session.add(addStaff)
       db.session.commit()
       return args, 201
    
    @marshal_with(staff_fields)
    def put(self):
        args = staff_put.parse_args()
        staff = staffDetails.query.filter_by(user_id=args["user_id"]).first()
        if not staff:
            abort(404, message = "staff doesn't exist, cannot update")
        if args["password"]:
            staff.password = args["password"]
        db.session.commit()
        return staff, 201

class courseDetails(Resource):
    def get(self):
        args = course_get.parse_args()
        isCourse = course.query.filter_by(course_code=args["course_code"]).first()
        if not isCourse:
            abort(404, message="no such course exist")
        args['course_name'] = isCourse.course_name
        args['course_type'] = isCourse.course_type
        args['total_credits'] = isCourse.total_credits
        args['semester_in'] = isCourse.semester_in
        return args
   
        
    def post(self):
        args = course_post.parse_args()
        isCourse = course.query.filter_by(course_code=args["course_code"]).first()
        if isCourse:
            abort(404, message="course already exist")
        addCourse = course(course_code=args["course_code"],course_name=args["course_name"],course_type=args["course_type"],total_credits=args["total_credits"],semester_in=args["semester_in"])
        db.session.add(addCourse)
        db.session.commit()
        return args, 201

class enroll(Resource):
    def get(self):
        args = enroll_get.parse_args()
        isenroll = studentEnrolled.query.filter_by(user_id=args["user_id"],course_code=args["course_code"]).first()
        if not isenroll:
            abort(404, message="student not enrolled to this subject")
        args['user_id'] = isenroll.user_id
        args['course_code'] = isenroll.course_code
        return args, 201

    def post(self):
        args = enroll_post.parse_args()
        student = studentDetails.query.filter_by(user_id=args["user_id"]).first()
        isCourse = course.query.filter_by(course_code=args["course_code"]).first()
        hasStudentEnrolled = studentEnrolled.query.filter_by(user_id=args["user_id"],course_code=args["course_code"]).first()
        if not student:
            abort(404, message="Could not find such student")
        elif not isCourse:
            abort(404,  message="Could not find such course")
        elif hasStudentEnrolled:
            abort(404, message= "student already enrolled to this subject")
        addEnrollment = studentEnrolled(user_id = args["user_id"],course_code=args["course_code"])
        db.session.add(addEnrollment)
        db.session.commit()
        return args, 201
    

class takeAttendance(Resource):
    # display student list in take attendance page
    def get(self,course_code):
        studentList = db.session.query(studentDetails,studentEnrolled).join(course_code == studentEnrolled.course_code,studentEnrolled.user_id, studentDetails.user_name).all()
        if not studentList:
            abort(404, message = "something went wrong")
        return studentList

api.add_resource(students,'/stud')
api.add_resource(staffRegistration,'/staff')
api.add_resource(courseDetails,'/courseDetails')
api.add_resource(enroll,'/enroll')

api.add_resource(takeAttendance,'/takeAttendance/<str:course_code>')
    
if __name__ == '__main__':
   app.run(debug=True)
