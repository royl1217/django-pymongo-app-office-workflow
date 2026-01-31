# from django import forms
# from .models import WorkflowRequest, Employee, AppUser


# class RegisterForm(forms.Form):
#   username = forms.CharField(max_length=100)
#   password = forms.CharField(widget=forms.PasswordInput)


# class LoginForm(forms.Form):
#   username = forms.CharField(max_length=100)
#   password = forms.CharField(widget=forms.PasswordInput)


# class WorkflowRequestForm(forms.ModelForm):
#   class Meta:
#     model = WorkflowRequest
#     fields = ["title", "description", "due_date", "approver"]
#     widgets = {
#       "description": forms.Textarea(attrs={"rows": 3}),
#       "due_date": forms.DateInput(attrs={"type": "date"}),
#     }

from django import forms
from .models import Employee

class WorkflowRequestForm(forms.Form):
  title = forms.CharField(max_length=200)
  description = forms.CharField(widget=forms.Textarea, required=False)
  due_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)

  approver = forms.ChoiceField(choices=[], required=True, label="Select Approver")

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # Load all employees for dropdown
    employees = Employee.objects.all()

    self.fields["approver"].choices = [
      (str(emp.id), emp.name) for emp in employees
    ]


class RegisterForm(forms.Form):
  username = forms.CharField(max_length=100)
  password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
  username = forms.CharField(max_length=100)
  password = forms.CharField(widget=forms.PasswordInput)