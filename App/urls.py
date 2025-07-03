from django.urls import path
from .views import (
    login_page,
    instructor_page,
    student_page,
    assignment_page,
    download_pupil_sheet,
    course_page,
    Instructor_assignment_page,
    logout_user
)
urlpatterns = [
    path('', login_page, name='login'),
    path('instructor', instructor_page, name='instructor'),
    path('student', student_page, name="student"),
    path('student/assignment/<int:assignment_id>', assignment_page, name="assignment_page"),
    path('download_pupil_sheet', download_pupil_sheet, name="download_pupil_sheet"),
    path('course/<int:course_id>', course_page, name="course_page"),
    path('assignment/<int:assignment_id>', Instructor_assignment_page, name="Instructor_assignment_page"),
    path('logout', logout_user, name="logout")

]
