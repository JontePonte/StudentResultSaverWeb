from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name='home'),
    path("home/", views.home, name='home'),
    path("groups/", views.groups, name='groups'),
    path("create/", views.create, name='create'),
    path("<int:id>", views.index, name='index')
]
