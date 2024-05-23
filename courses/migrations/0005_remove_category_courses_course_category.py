# Generated by Django 4.2.10 on 2024-04-26 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_category_courses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='courses',
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.category'),
        ),
    ]
