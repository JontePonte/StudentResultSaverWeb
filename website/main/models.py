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
