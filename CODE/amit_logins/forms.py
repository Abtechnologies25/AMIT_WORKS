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

class AbstractPaymentVoucherForm(forms.ModelForm):
    class Meta:
        fields = ['S_NO','DATE', 'VC_NO', 'PURPOSE', 'ONLINE_PAYMENT', 'CASH_PAYMENT']
        widgets = {
            'DATE': forms.DateInput(attrs={'type': 'date'}),
            'PURPOSE': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter purpose'}),
            'ONLINE_PAYMENT': forms.NumberInput(attrs={'placeholder': 'Enter Online Payment'}),
            'CASH_PAYMENT': forms.NumberInput(attrs={'placeholder': 'Enter Cash Payment'}),
        }


class NagercoilPaymentVoucherForm(AbstractPaymentVoucherForm):
    class Meta(AbstractPaymentVoucherForm.Meta):
        model = NagercoilPaymentVoucher

class TirunelveliPaymentVoucherForm(AbstractPaymentVoucherForm):
    class Meta(AbstractPaymentVoucherForm.Meta):
        model = TirunelveliPaymentVoucher

class PudukottaiPaymentVoucherForm(AbstractPaymentVoucherForm):
    class Meta(AbstractPaymentVoucherForm.Meta):
        model = PudukottaiPaymentVoucher

class ChennaiPaymentVoucherForm(AbstractPaymentVoucherForm):
    class Meta(AbstractPaymentVoucherForm.Meta):
        model = ChennaiPaymentVoucher

class AbstractProductRegistrationForm(forms.ModelForm):
    class Meta:
        fields = ['S_NO','DATE', 'REG_CODE', 'NAME', 'DEPARTMENT', 'TYPE', 
                  'COLLEGE_UNIVERSITY', 'MOBILE_NO', 'EMAIL_ID','TOTAL_AMOUNT', 
                  'AMOUNT_PAID', 'STATUS']
        widgets = {
            'DATE': forms.DateInput(attrs={'type': 'date'}),
            'MOBILE_NO': forms.TextInput(attrs={'placeholder': 'Enter mobile number'}),
            'EMAIL_ID': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
        }


class NagercoilProductRegistrationForm(AbstractProductRegistrationForm):
    class Meta(AbstractProductRegistrationForm.Meta):
        model = NagercoilProductRegistration

class TirunelveliProductRegistrationForm(AbstractProductRegistrationForm):
    class Meta(AbstractProductRegistrationForm.Meta):
        model = TirunelveliProductRegistration

class PudukottaiProductRegistrationForm(AbstractProductRegistrationForm):
    class Meta(AbstractProductRegistrationForm.Meta):
        model = PudukottaiProductRegistration

class ChennaiProductRegistrationForm(AbstractProductRegistrationForm):
    class Meta(AbstractProductRegistrationForm.Meta):
        model = ChennaiProductRegistration

class AbstractInternshipRegistrationForm(forms.ModelForm):
    class Meta:
        fields = ['S_NO','DATE', 'REG_CODE', 'NAME', 'DEPARTMENT', 'INTERNSHIP_TYPE', 
                  'COLLEGE_UNIVERSITY', 'MOBILE_NO', 'EMAIL_ID','TOTAL_AMOUNT', 
                  'AMOUNT_PAID', 'STATUS']
        widgets = {
            'DATE': forms.DateInput(attrs={'type': 'date'}),
            'MOBILE_NO': forms.TextInput(attrs={'placeholder': 'Enter mobile number'}),
            'EMAIL_ID': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
           
        }

class NagercoilInternshipRegistrationForm(AbstractInternshipRegistrationForm):
    class Meta(AbstractInternshipRegistrationForm.Meta):
        model = NagercoilInternshipRegistration

class TirunelveliInternshipRegistrationForm(AbstractInternshipRegistrationForm):
    class Meta(AbstractInternshipRegistrationForm.Meta):
        model = TirunelveliInternshipRegistration

class PudukottaiInternshipRegistrationForm(AbstractInternshipRegistrationForm):
    class Meta(AbstractInternshipRegistrationForm.Meta):
        model = PudukottaiInternshipRegistration

class ChennaiInternshipRegistrationForm(AbstractInternshipRegistrationForm):
    class Meta(AbstractInternshipRegistrationForm.Meta):
        model = ChennaiInternshipRegistration

DATE_WIDGET = forms.DateInput(attrs={'type': 'date'})

class BaseBillForm(forms.ModelForm):
    class Meta:
        fields = [
            'S_NO','DATE','MONTH','YEAR', 'BILL_NUMBER', 'REGISTRATION_NUMBER', 'NAME', 'TOTAL_AMOUNT',
            'CASH_RECEIVED', 'ONLINE_RECEIVED','TOTAL_PAID_AMOUNT_TILL_NOW','PAYMENT_STATUS'
        ]
        widgets = {
            'DATE': DATE_WIDGET,
            'MONTH': forms.Select(),
            'YEAR': forms.Select(),
        }

for model in [ NAGERCOILINTERNSHIPBILL, NAGERCOILPRODUCTBILL, TIRUNELVELIINTERNSHIPBILL, TIRUNELVELIPRODUCTBILL, PUDUKOTTAIINTERNSHIPBILL, PUDUKOTTAIPRODUCTBILL,CHENNAIINTERNSHIPBILL, CHENNAIPRODUCTBILL]:
    
    form_class = type(f"{model.__name__}Form", (BaseBillForm,), {'Meta': type('Meta', (), {'model': model, **BaseBillForm.Meta.__dict__})})
    globals()[form_class.__name__] = form_class