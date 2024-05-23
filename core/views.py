from django.shortcuts import render, redirect
import re
from django.db.models import Count
from .models import Blog, StudentMessage
from dashboard.models import CourseProgress
from courses.models import Category, Course


def home(request):
    blogs = Blog.objects.all()
    messages = StudentMessage.objects.all()
    categories = Category.objects.all()
    # most popular courses logic
    courses = None
    completed_progresses = CourseProgress.objects.filter(completed=True)
    if Course.objects.all().count() <= 3 or len(completed_progresses) <= 0:
        courses = Course.objects.all()
    else:
        popular_courses = completed_progresses.values("course").annotate(
            repetation_times=Count("course")).order_by('-repetation_times')[:3]
        course_ids = []
        for cousre in popular_courses:
            course_ids.append(cousre['course'])
        courses = Course.objects.filter(id__in=course_ids)
    return render(request, 'core/index.html', {
        'blogs': blogs,
        'messages': messages,
        'categories': categories,
        'courses': courses,
    })


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


def testimonial(request):
    # define the profanity filter logic
    bad_words = ["asshole", "bastard", "bitch",
                 "damn", "dickhead", "fuck", "piss off", "shit"]
    bad_words_pattern = re.compile(
        r"\b(" + r"|".join(bad_words) + r")\b", re.IGNORECASE)
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        # Check for profanity in the user's input
        if bad_words_pattern.search(message) or bad_words_pattern.search(subject):
            print("the message contains bad words !")
            return render(request, 'core/contact.html', {
                "error": "Please do not use any bad words",
            })
        user_message = StudentMessage(
            author=request.user, subject=subject, content=message)
        user_message.save()
        return redirect('core:home')
    else:
        messages = StudentMessage.objects.all()
    return render(request, 'core/testimonial.html', {
        'messages': messages
    })
