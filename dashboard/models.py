from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import Course, Lesson


class Profile(AbstractUser):
    def __str__(self):
        return self.username


class Subprofile(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    picture = models.ImageField(
        default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class CourseProgress(models.Model):
    """A model to keep track of a users progress through courses."""
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(
        Lesson, related_name="completed_lessons",)
    last_accessed_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="last_accessed_lesson", null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.last_name} {self.course.name} Progress"
