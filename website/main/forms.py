from django import forms


class CreateNewGroup(forms.Form):
    name = forms.CharField(max_length=200)
    
