from django import forms


class CreateNewGroup(forms.Form):
    name = forms.CharField(max_length=200)
    

class CreateNewStudent(forms.Form):
    first_name= forms.CharField(max_length=200)
    last_name= forms.CharField(max_length=200)
