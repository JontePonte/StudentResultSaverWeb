from django import forms


class CreateNewGroup(forms.Form):
    name = forms.CharField(max_length=100)
    

class CreateNewStudent(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

class CreateNewExam(forms.Form):
    name = forms.CharField(max_length=100)
