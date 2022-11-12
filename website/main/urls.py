from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name='home'),
    path("home/", views.home, name='home'),
    path("groups/", views.groups, name='groups'),
    path("group/<int:id>", views.group, name='group'),
    path("student/<int:id>", views.student, name='student'),
    path("exam/<int:id>", views.exam, name='exam'),
]
