from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from .forms import CreateNewGroup, CreateNewStudent
from .models import Group, Student


def home(response):
    return render(response, "main/home.html", {})


def index(response, id):
    gr = Group.objects.get(id=id)

    # Safety check so user can't access each other groups
    if not gr in response.user.group.all():
        return render(response, "main/groups.html", {})


    if response.method == "POST":
        if response.POST.get("save_rename"):
            txt = response.POST.get("rename")
            gr.name = txt
            gr.save()
        elif response.POST.get("delete_group"):
            gr.delete()
            return HttpResponseRedirect("/groups/")
        elif response.POST.get("save_student"):
            form_new_student = CreateNewStudent(response.POST)
            if form_new_student.is_valid():
                first_name = form_new_student.cleaned_data["first_name"]
                last_name = form_new_student.cleaned_data["last_name"]
                st = Student(first_name=first_name, last_name=last_name)
                st.save()
                gr.student.add(st)
        
    form_new_student = CreateNewStudent()

    return render(response, "main/group.html", {"gr":gr, "form_new_student":form_new_student})


def groups(response):
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
    return render(response, "main/groups.html", {"form":form})

