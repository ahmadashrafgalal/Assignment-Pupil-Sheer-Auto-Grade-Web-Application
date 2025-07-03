from django.shortcuts import render, redirect
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
from django.contrib.auth import authenticate, login
import datetime
from .model_functions import process_exam_sheet, process_exam_answer
import os
from django.contrib.auth import logout


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return check_user_type(user)
        
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("login")

def check_user_type(user):
    if hasattr(user, 'student'):
        return redirect("student")
    elif hasattr(user, 'instructor'):
        return redirect("instructor")
    else:
        return redirect("login")

# ------------------------------------------------------------------------------------
# -----------------------------------< Instructor >-----------------------------------
def instructor_page(request):
    instructor = Instructor.objects.get(user=request.user)
    courses = InstructorCourse.objects.filter(instructor=instructor)
    print(courses)
    return render(request, "instructor/new_instructor.html", {"courses": courses,
                                               "instructor": instructor})
    

def course_page(request, course_id):
    course = Course.objects.get(id=course_id)
    assignments = Assignment.objects.filter(course=course)
    instructor = Instructor.objects.get(user=request.user)
    for assignment in assignments:
        assignment.uploads = StudentAssignment.objects.filter(assignment=assignment).count()
        assignment.answers = AssignmentQuestion.objects.filter(assignment=assignment)
        # for answer in assignment.answers:
        #     print(answer.question_number)
        #     print(answer.question_answer)

    if request.method == "POST":
        if 'answer_form_submit' in request.POST:
            assignment_id = request.POST.get('assignment_id')

            assignment = Assignment.objects.get(id=assignment_id)

            assignment.answers = AssignmentQuestion.objects.filter(assignment=assignment)

            for answer in assignment.answers:
                answer.question_answer = request.POST.get(str(answer.question_number))
                answer.save()
        else:
            assignment = Assignment()
            assignment.assignment_name = request.POST.get('assignment_name')
            assignment.assignment_file = request.FILES.get('assignment_file')
            assignment.pupil_sheet = request.FILES.get('assignment_pupil')
            assignment.questions_count = request.POST.get('question_count')
            assignment.date = datetime.datetime.now()
            assignment.course = course
            assignment.save()

            for i in range(1, int(assignment.questions_count) + 1):
                question = AssignmentQuestion()
                question.assignment = assignment
                question.question_number = i
                question.question_answer = 0
                question.save()

            tf_results, abcd_results ,path = process_exam_sheet(str(os.path.abspath(assignment.pupil_sheet.path)) , int(assignment.questions_count), assignment.id)

            for i, result in abcd_results:
                print(f"Updating question {i} with answer {result}")  # Debugging line
                question = AssignmentQuestion.objects.get(assignment=assignment, question_number=i)
                question.question_answer = result
                question.save()

            assignment.pupil_sheet = path
            assignment.save()


    return render(request, "instructor/new_course.html", {"course": course,
                                                      "assignments": assignments,
                                                      "instructor": instructor,
                                                      })


def Instructor_assignment_page(request, assignment_id):
    instructor = Instructor.objects.get(user=request.user)

    assignment = Assignment.objects.get(id=assignment_id)
    student_assignments = StudentAssignment.objects.filter(assignment=assignment)
    answers = AssignmentQuestion.objects.filter(assignment=assignment)
    course = Course.objects.get(id=assignment.course_id)

    assignment.count = student_assignments.count()

    for student_assignment in student_assignments:
        student_assignment.answers = StudentAssignmentAnswer.objects.filter(student_assignment=student_assignment)

    return render(request, "instructor/new_assignment.html", {"assignment": assignment,
                                                         "student_assignments": student_assignments,
                                                         "answers": answers,
                                                         "course": course,
                                                         "instructor": instructor
                                                         })
# -----------------------------------------------------------------------------------
# ------------------------------------< Student >------------------------------------
def student_page(request):
    student = Student.objects.get(user=request.user)

    done_assignments = StudentAssignment.objects.filter(student=student).values_list('assignment_id', flat=True)

    assignments = Assignment.objects.all()

    for assignment in assignments:
        assignment.status = "Completed" if assignment.id in done_assignments else "Not Completed"

    return render(request, 'student/new_student.html', {
        'student': student,
        'assignments': assignments
    })


def assignment_page(request, assignment_id):
    student = Student.objects.get(user=request.user)
    assignment = Assignment.objects.get(id=assignment_id)
    
    done_assignments = StudentAssignment.objects.filter(student=student).values_list('assignment_id', flat=True)
    instructor = InstructorCourse.objects.get(course=assignment.course).instructor

    if assignment.id in done_assignments:
        assignment.status = "Completed"
    else:
        assignment.status = "NotCompleted"

    if request.method == "POST" :
        student_assignment = StudentAssignment()
        student_assignment.student = student
        student_assignment.assignment = assignment
        student_assignment.student_assignment_file = request.FILES.get('file_input')
        student_assignment.student_assignment_date = datetime.datetime.now()
        student_assignment.grade = 0

        student_assignment.save()



        true_count  = 0 

        tf_results, abcd_results, path = process_exam_answer(str(os.path.abspath(student_assignment.student_assignment_file.path)) , int(assignment.questions_count), assignment.id, student.id)

        for i, result in abcd_results:
            question = AssignmentQuestion.objects.get(assignment=assignment, question_number=i)
            if question.question_answer == result:
                true_count += 1

        student_assignment.grade = true_count
        student_assignment.student_assignment_file = path
        student_assignment.save()

    
    return render(request, 'student/new_assign.html', {'assignment':assignment,
                                                       'student': student,
                                                         'instructor': instructor
                                                       })

from django.http import FileResponse
import os
from django.conf import settings

def download_pupil_sheet(request):
    file_path = os.path.join(settings.BASE_DIR, 'App/static/IMG/pupil.jpg')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename="Pupil_Sheet.jpg")