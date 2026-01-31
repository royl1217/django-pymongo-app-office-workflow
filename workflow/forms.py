from django import forms
from .models import WorkflowRequest, Employee, AppUser


class RegisterForm(forms.Form):
  username = forms.CharField(max_length=100)
  password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
  username = forms.CharField(max_length=100)
  password = forms.CharField(widget=forms.PasswordInput)


class WorkflowRequestForm(forms.ModelForm):
  class Meta:
    model = WorkflowRequest
    fields = ["title", "description", "due_date", "approver"]
    widgets = {
      "description": forms.Textarea(attrs={"rows": 3}),
      "due_date": forms.DateInput(attrs={"type": "date"}),
    }