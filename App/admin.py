from django.contrib import admin
from .models import (
    Student,
    Instructor,
    Course,
    StudentCourse,
    InstructorCourse,
    Assignment,
    AssignmentQuestion,
    StudentAssignment,
    StudentAssignmentAnswer
)
# Register your models here.

admin.site.register((Student, Instructor, Course, StudentCourse, InstructorCourse, Assignment, AssignmentQuestion, StudentAssignment, StudentAssignmentAnswer))