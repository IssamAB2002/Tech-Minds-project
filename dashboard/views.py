from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ProfileCreation, LoginForm
from .models import CourseProgress


def dashboard(request):
    user = request.user
    all_progress = CourseProgress.objects.filter(user=user)
    progress_data = []
    for progress in all_progress:
        all_lessons = progress.course.lesson_set.count()
        compl_lessons = progress.completed_lessons.count()
        percentage = (compl_lessons / float(all_lessons)) * \
            100 if all_lessons > 0 else 0
        prog_obj = dict(course_name=progress.course.name,
                        all_lessons=all_lessons,
                        completed_lessons=compl_lessons, prog_percenage=percentage)
        progress_data.append(prog_obj)
    return render(request, 'dashboard/dashboard.html', {
        'progress_data': progress_data,
    })


def user_signup(request):
    if request.method == 'POST':
        form = ProfileCreation(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:login')
    else:
        form = ProfileCreation()
    return render(request, 'dashboard/signup.html', {
        'form': form
    })


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                print("User Logged in")
                return redirect('core:home')
            else:
                print("Invalid Credenials")
    else:
        form = LoginForm()
    return render(request, 'dashboard/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('dashboard:login')
