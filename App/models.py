from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    acadimic_year = models.IntegerField()
    section = models.CharField(max_length=1)
    img = models.ImageField(upload_to='student_images/', default='student_images/default.jpg')

    def __str__(self):
        return self.user.username
    
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    img = models.ImageField(upload_to='instructor_images/', default='student_images/default.jpg')

    def __str__(self):
        return self.user.username
    
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=10)
    credit_hours = models.IntegerField()
    img = models.ImageField(upload_to='course_images/', default='student_images/default.jpg')

    def __str__(self):
        return self.course_name
    
class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.user.username + ' ' + self.course.course_name
    
class InstructorCourse(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.instructor.user.username + ' ' + self.course.course_name
    
class Assignment(models.Model):
    assignment_name = models.CharField(max_length=100)
    assignment_file = models.FileField(upload_to='assignments/')
    pupil_sheet = models.FileField(upload_to='pupil_sheets/')
    questions_count = models.IntegerField()
    date = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.assignment_name
    
class AssignmentQuestion(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    question_number = models.IntegerField()
    question_answer = models.CharField(max_length=1)

    def __str__(self):
        return self.assignment.assignment_name + ' ' + str(self.question_number)

class StudentAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student_assignment_file = models.FileField(upload_to='student_assignments/')
    student_assignment_date = models.DateTimeField()
    grade = models.IntegerField()

    def __str__(self):
        return self.student.user.username + ' ' + self.assignment.assignment_name
    
class StudentAssignmentAnswer(models.Model):
    student_assignment = models.ForeignKey(StudentAssignment, on_delete=models.CASCADE)
    question_number = models.IntegerField()
    question_answer = models.IntegerField()

    def __str__(self):
        return self.question
    