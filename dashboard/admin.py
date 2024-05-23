from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Profile, Subprofile, CourseProgress
from .forms import ProfileCreation
 
class CustomUserAdmin(UserAdmin):
    add_form = ProfileCreation
    model = Profile
    list_display = ['username', 'email', 'is_staff']

admin.site.register(Profile, CustomUserAdmin)
admin.site.register(Subprofile)
admin.site.register(CourseProgress)