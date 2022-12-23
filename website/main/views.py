from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.template.defaulttags import register

from .forms import CreateNewGroup, CreateNewStudent, CreateNewExam, CreateNewAssignment, AddExamResult, AddAssignmentResult
from .models import Group, Student, Exam, ExamResult, Assignment, AssignmentResult


def home(response):
    return render(response, "main/home.html", {})


def group(response, id):
    gr = Group.objects.get(id=id)

    # Safety check so user can't access each other groups
    if not gr in response.user.group.all():
        return render(response, "main/groups.html", {})


    if response.method == "POST":
        # Edit, delete group
        if response.POST.get("save_rename"):
            txt = response.POST.get("rename")
            gr.name = txt
            gr.save()
        elif response.POST.get("delete_group"):
            gr.delete()
            return HttpResponseRedirect("/groups/")
        # ADd student
        elif response.POST.get("save_student"):
            form_new_student = CreateNewStudent(response.POST)
            if form_new_student.is_valid():
                first_name = form_new_student.cleaned_data["first_name"]
                last_name = form_new_student.cleaned_data["last_name"]
                st = Student(first_name=first_name, last_name=last_name)
                st.save()
                gr.student.add(st)
        # Add exam
        elif response.POST.get("save_exam"):
            form_new_exam = CreateNewExam(response.POST)
            if form_new_exam.is_valid():
                name = form_new_exam.cleaned_data["name"]
                ex = Exam(name=name)
                ex.save()
                gr.exam.add(ex)
        # Add assignment
        elif response.POST.get("save_assignment"):
            form_new_assignment = CreateNewAssignment(response.POST)
            if form_new_assignment.is_valid():
                name = form_new_assignment.cleaned_data["name"]
                assignment = Assignment(name=name)
                assignment.save()
                gr.assignment.add(assignment)
        # Save exam and assignment results
        elif response.POST.get("save_all_results"):
            pass
    
    # Empty form info
    form_new_student = CreateNewStudent()
    form_new_exam = CreateNewExam()
    form_new_assignment = CreateNewAssignment()
    form_add_exam_result = AddExamResult()
    form_add_assignment_result = AddAssignmentResult()


    return render(response, "main/group.html", 
    {
        "gr":gr, 
        "form_new_student":form_new_student, 
        "form_new_exam":form_new_exam, 
        "form_new_assignment":form_new_assignment,
        "form_add_exam_result": form_add_exam_result,
        "form_add_assignment_result":form_add_assignment_result,
        })


def student(response, id):
    st = Student.objects.get(id=id)
    gr = st.group

    # Create dict with all student exam results
    exams = {}
    for exam in gr.exam.all():
        student_result = {}
        exams[exam.id] = student_result
        for exam_result in exam.exam_result.all():
            if exam_result in st.exam_result.all():
                student_result["exam_id"] = exam.id
                student_result["points_e"] = exam_result.points_e
                student_result["points_c"] = exam_result.points_c
                student_result["points_a"] = exam_result.points_a

    # Safety check so user can't access each other groups
    if not gr in response.user.group.all():
        return render(response, "main/groups.html", {})

    if response.method == "POST":
        if response.POST.get("save_rename"):
            print("save rename")
            first_new = response.POST.get("rename_first")
            last_new = response.POST.get("rename_last")
            # First and last name is not changed if input is empty
            if not first_new:
                first_new = st.first_name
            if not last_new:
                last_new = st.last_name
            st.first_name = first_new
            st.last_name = last_new
            st.save()
        # Delete student
        elif response.POST.get("delete_student"):
            st.delete()
            return HttpResponseRedirect(f"/group/{gr.id}")
        # Save student results
        elif response.POST.get("save_exam_results"):
            print("save result")
            for exam in gr.exam.all():
                # Create new result if it doesn't exist. Else select right result
                if not st.exam_result.filter(exam=exam):
                    er = ExamResult(exam=exam, student=st)
                else:
                    er = st.exam_result.filter(exam=exam).first()
                
                er.points_e = response.POST.get(f"points_e_{exam.id}")
                er.points_c = response.POST.get(f"points_c_{exam.id}")
                er.points_a = response.POST.get(f"points_a_{exam.id}")

                er.save()
    
    
    form_add_exam_result = AddExamResult() # probably unnecessary

    # Extract student exam results
    exam_results = {}
    for exam in gr.exam.all():
        exam_results[exam.id] = {
            "points_e": ExamResult.objects.filter(student=st).filter(exam=exam).first().points_e,
            "points_c": ExamResult.objects.filter(student=st).filter(exam=exam).first().points_c,
            "points_a": ExamResult.objects.filter(student=st).filter(exam=exam).first().points_a,
            "exam.id": exam.id,
        }
    
    # Add function to allow filtering of dicts
    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    return render(response, "main/student.html", 
    {
        "st":st,
        "form_add_exam_result": form_add_exam_result,
        "exams": exams,
        "exam_results": exam_results,
        })


def exam(response, id):
    exam = Exam.objects.get(id=id)
    gr = exam.group

    # Safety check so user can't access each other groups
    if not gr in response.user.group.all():
        return render(response, "main/groups/.html", {})

    if response.method == "POST":
        # Edit, delete exam
        if response.POST.get("save_rename"):
            txt = response.POST.get("rename")
            exam.name = txt
            exam.save()
        elif response.POST.get("delete_exam"):
            exam.delete()
            return HttpResponseRedirect(f"/group/{gr.id}")

    return render(response, "main/exam.html", {"exam":exam})


def assignment(response, id):
    assignment = Assignment.objects.get(id=id)
    gr = assignment.group

    # Safety check so user can't access each other groups
    if not gr in response.user.group.all():
        return render(response, "main/groups/.html", {})

    if response.method == "POST":
        # Edit, delete assignment
        if response.POST.get("save_rename"):
            txt = response.POST.get("rename")
            assignment.name = txt
            assignment.save()
        elif response.POST.get("delete_assignment"):
            assignment.delete()
            return HttpResponseRedirect(f"/group/{gr.id}")

    return render(response, "main/assignment.html", {"assignment":assignment})



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

