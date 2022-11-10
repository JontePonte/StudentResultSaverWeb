from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group", null=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, default="My favorite class")

    def __str__(self):
        return str(self.name)
    

class Student(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="student", null=True)
    first_name = models.CharField(max_length=300, default="Anna")
    last_name = models.CharField(max_length=300, default="Andersson")

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class Exam(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="exam", null=True)


class ExamResult(models.Model):
    exam = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name="exam_result", null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name="exam_result", null=True)


class Assignment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="assignment", null=True)


class AssignmentResult(models.Model):
    assignment = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name="assignment_result", null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name="assignment_result", null=True)

