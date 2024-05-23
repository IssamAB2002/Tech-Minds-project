from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category_imgs')
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='course_icons', default='course_default.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.FileField(upload_to='lessons/')
    def __str__(self):
        return f'{self.course.name} {self.title}'
