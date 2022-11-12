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
    name = models.CharField(max_length=200)
    comment = models.CharField(max_length=500, default="")
    points_max_e = models.FloatField(default=0)
    points_max_a = models.FloatField(default=0)
    points_max_c = models.FloatField(default=0)
    # User can choose to set limits in the system or fix manually
    set_limit = models.BooleanField(default=False)
    points_grade_e_e = models.FloatField(default=0) # E requires only E-points
    points_grade_d_e = models.FloatField(default=0) # D requires E and C points
    points_grade_d_c = models.FloatField(default=0) # ...
    points_grade_c_e = models.FloatField(default=0)
    points_grade_c_C = models.FloatField(default=0)
    points_grade_b_e = models.FloatField(default=0)
    points_grade_b_c = models.FloatField(default=0)
    points_grade_b_a = models.FloatField(default=0)
    points_grade_a_e = models.FloatField(default=0)
    points_grade_a_c = models.FloatField(default=0)
    points_grade_a_a = models.FloatField(default=0)


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, related_name="exam_result", null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name="exam_result", null=True)
    comment = models.CharField(max_length=500, default="")
    points_e = models.FloatField()
    points_c = models.FloatField()
    points_a = models.FloatField()
    # Users can set custom max points if other exam version is used
    points_diff_max_e = models.FloatField(default=0)
    points_diff_max_c = models.FloatField(default=0)
    points_diff_max_a = models.FloatField(default=0)
    # result is set either by user or with exam set limits
    result = models.CharField(max_length=20)


class Assignment(models.Model):
    # Assignments are simpler than exams. No points or limits, just result
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="assignment", null=True)
    name = models.CharField(max_length=200)
    comment = models.CharField(max_length=500, default="")


class AssignmentResult(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, related_name="assignment_result", null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name="assignment_result", null=True)
    # This is only set by user, no automatic function
    result = models.CharField(max_length=100)

