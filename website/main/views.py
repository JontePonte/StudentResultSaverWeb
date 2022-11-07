from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from .forms import CreateNewGroup
from .models import Group


def home(response):
    return render(response, "main/home.html", {})


def index(response, id):
    gr = Group.objects.get(id=id)

    # Safety check so user can't access each other groups
    if not gr in response.user.group.all():
        return render(response, "main/groups.html", {})

    if response.method == "POST":
        if response.POST.get("renameSave"):
            txt = response.POST.get("rename")
            gr.name = txt
            gr.save()

    return render(response, "main/group.html", {"gr":gr})


def groups(response):
    return render(response, "main/groups.html", {})


def create(response):
    if response.method == "POST":
        form = CreateNewGroup(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"] # Unencrypts data
            g = Group(name=n)
            g.save()
            response.user.group.add(g)
        
            return HttpResponseRedirect("/groups/")

    else:
        form = CreateNewGroup()
    return render(response, "main/create.html", {"form":form})