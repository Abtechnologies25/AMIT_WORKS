from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,SetPasswordForm
from .models import *
from django.forms import modelformset_factory

class UserRegisterForm(UserCreationForm):
    department = forms.ChoiceField(choices=User.DEPARTMENT_CHOICES, label="Department")
    branch = forms.ChoiceField(choices=User.BRANCH_CHOICES, label="Branch")

    class Meta:
        model = User
        fields = ['username','employee_name', 'email', 'password1', 'password2', 'department', 'branch']

    # def __init__(self, *args, **kwargs):
    #     super(UserRegisterForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.widget.attrs['placeholder'] = field.label  # Set label as placeholder
    #         field.label = ""  
    def __init__(self, *args, **kwargs):
            super(UserRegisterForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'
                visible.field.label = ''  # 🔒 Completely hide label
                if visible.name == 'username':
                    visible.field.widget.attrs['placeholder'] = 'Employee ID'  # custom placeholder
                else:
                    visible.field.widget.attrs['placeholder'] = visible.field.label or visible.name.capitalize()

class UserLoginForm(AuthenticationForm):
    # def __init__(self, *args, **kwargs):
    #     super(UserLoginForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'
    #         visible.field.widget.attrs['placeholder'] = visible.field.label
    #         visible.label = ''
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.label = ''  
            if visible.name == 'username':
                visible.field.widget.attrs['placeholder'] = 'Employee ID' 
            else:
                visible.field.widget.attrs['placeholder'] = visible.field.label or visible.name.capitalize()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','employee_name', 'email', 'department', 'branch']

class UserPasswordEditForm(SetPasswordForm):
    class Meta:
        model = User

class WorkStatusGroupForm(forms.ModelForm):
    class Meta:
        model = WorkStatusGroup
        fields = ['S_NO', 'DATE']
        widgets = {
             'DATE': forms.DateInput(attrs={'type': 'date'}),
        }

class WorkStatusForm(forms.ModelForm):
    class Meta:
        model = WorkStatus
        fields = ['WORK_CODE', 'WORK_DETAILS', 'STARTING_DATE', 'ENDING_DATE', 'WORK_STATUS']
        widgets = {
             'STARTING_DATE': forms.DateInput(attrs={'type': 'date'}),
             'ENDING_DATE': forms.DateInput(attrs={'type': 'date'}),
         }