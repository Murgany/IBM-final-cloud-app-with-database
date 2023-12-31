from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Course, Enrollment, Submission, Choice, Question
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


""" Registration view """
def registration_request(request):
    """ Represents a user registration operation """
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        
        # check if user exists
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
            
        #check if user doesn't already exist,create a new user
        if not user_exist:
            user = User.objects.create_user(username=username, 
                                            first_name=first_name, 
                                            last_name=last_name, 
                                            password=password
                                            )
            login(request, user)
            return redirect("onlinecourse:index")
        else: # if user exists
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)

""" Login view """
def login_request(request):
    """ Represents a login operation """
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


""" Logout """
def logout_request(request):
""" Represents a logout operation """
    logout(request)
    return redirect('onlinecourse:index')


def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled


""" Course List View """
class CourseListView(generic.ListView):
    """ Lists all available courses"""
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses


"""Course Details View """
class CourseDetailView(generic.DetailView):
    """ Displays details of a particular course """
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'


""" Enrollment view """
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


""" Submit choices view """
def submit(request, course_id):
    # Get the courses by id
    course = get_object_or_404(Course, pk=course_id)
    # Get the user
    user = request.user
    # Filter the enrollment by user and course
    enrollment = Enrollment.objects.filter(user=user, course=course).get()
    # Create a submission id
    submission = Submission.objects.create(enrollment_id=enrollment.id)

    choices = extract_answers(request)
    for a in choices:
        temp_c = Choice.objects.filter(id=int(a)).get()
        submission.choices.add(temp_c)

    submission.save()
    return HttpResponseRedirect(reverse(viewname='onlinecourse:show_exam_result', args=(course.id, submission.id)))


def extract_answers(request):
    submitted_choices = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_choices.append(choice_id)
    return submitted_choices


""" Exam results view """
def show_exam_result(request, course_id, submission_id):
    # Get course and submission based on ids
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    # Get the selected choice ids from the submission record
    choices = submission.choices.all()
    questions = course.question_set.all()

    # Calculate total score
    total = sum([q.question_grade for q in questions])
    achieved_score = 0

    # Get the list selected choices
    selected_choice_ids = choices.values_list("id", flat=True)

    for question in questions:
        if question.is_get_score(choices):
            achieved_score += question.question_grade

    grade = round(achieved_score/total*100)

    context = {'course': course,
               'submission': submission,
               'grade': grade,
               'total': total,
               'choices': choices,
               'selected_choice_ids': selected_choice_ids
               }

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
