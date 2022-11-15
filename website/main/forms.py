from django import forms


class CreateNewGroup(forms.Form):
    name = forms.CharField(max_length=100)
    

class CreateNewStudent(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

class CreateNewExam(forms.Form):
    name = forms.CharField(max_length=100)

class CreateNewAssignment(forms.Form):
    name = forms.CharField(max_length=100)

class AddExamResult(forms.Form):
    points_e = forms.FloatField()
    points_c = forms.FloatField()
    points_a = forms.FloatField()

class AddAssignmentResult(forms.Form):
    result = forms.CharField(max_length=20)
