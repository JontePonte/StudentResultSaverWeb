from django.shortcuts import render
from django.http import HttpResponse


def home(response):
    return render(response, "main/home.html", {})


def groups(response):
    return render(response, "main/groups.html", {})
