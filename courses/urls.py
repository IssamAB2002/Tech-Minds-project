from django.urls import path
from . import views
app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('cat_course/<int:id>/', views.cat_courses, name='cat_courses'),
    path('cat_course/<int:id>/lesson/<int:lsn_id>',
         views.lesson_view, name="lesson"),
    path('cat_course/<int:id>/lesson/<int:lsn_id>/completed', views.lesson_complet_view, name="lesson_complet")
]
