from django.db import models
from dashboard.models import Profile
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    blog_image = models.ImageField(upload_to='blogs_pic/')
    small_content = models.CharField(max_length=150, null=True)
    def __str__(self):          
        return self.title

class StudentMessage(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    content = models.TextField()
