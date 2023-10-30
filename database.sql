create table studentsEnrolled(
enrollId int primary key,
userId int,
subjectCode varchar(10),
	FOREIGN KEY(userId) 
	  REFERENCES studentsEnrolled(userId)
);