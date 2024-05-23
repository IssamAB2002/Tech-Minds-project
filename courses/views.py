from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.db.models import Count, Sum, F, Value
from django.template import Context, Template
from .models import Category, Course, Lesson
from dashboard.models import CourseProgress
import os


def index(request):
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
    return render(request, 'courses/courses.html', {
        'categories': categories,
        'courses': courses
    })


def cat_courses(request, id):
    category = Category.objects.get(id=id)
    courses = Course.objects.all().filter(category=category)
    return render(request, 'courses/cat-courses.html', {
        'category': category,
        'courses': courses,
    })


def lesson_view(request, id, lsn_id):
    course = Course.objects.get(id=id)
    course_lessons = Lesson.objects.filter(course=course)
    user = request.user
    progress = None
    if user.is_authenticated:
        progress, created = CourseProgress.objects.get_or_create(
            user=user, course=course)
        if progress:
            progress.save()
            if created:
                progress.completed_lessons.clear()
    if lsn_id != 0:
        lesson = Lesson.objects.get(id=lsn_id)
    else:
        lesson = Lesson.objects.first()

    content_path = lesson.content.path
    with open(content_path, 'r') as file:
        content = file.read()
    user_all_progress = CourseProgress.objects.filter(user=user)
    return render(request, 'courses/lesson.html', {
        'course': course,
        'lesson': lesson,
        'course_lessons': course_lessons,
        'content': content,
        'progress': progress,
    })


def lesson_complet_view(request, id, lsn_id):
    course = Course.objects.get(id=id)
    lesson = Lesson.objects.get(id=lsn_id)
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            user = request.user
            try:
                course_progress, created = CourseProgress.objects.get_or_create(
                    user=user, course=course)
                if lesson not in course_progress.completed_lessons.all():
                    course_progress.completed_lessons.add(lesson)
                all_lessons = course_progress.course.lesson_set.count()
                if all_lessons >= course_progress.completed_lessons.count():
                    course_progress.completed = True
                course_progress.save()
                return JsonResponse({'message': 'Lesson marked completed successfully!'})
            except (Lesson.DoesNotExist, CourseProgress.DoesNotExist):
                return JsonResponse({'error': 'Invalid lesson or course.'}, status=400)
            except Exception as e:
                print(f"Error marking lesson completed: {e}")
                return JsonResponse({'error': 'An error occurred.'}, status=500)
        else:
            return JsonResponse({'error': "You must be logged in to track you learn progress."}, status=403)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
