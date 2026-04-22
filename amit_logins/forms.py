from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,SetPasswordForm
from .models import *
from django.forms import modelformset_factory, inlineformset_factory

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
            'S_NO','DATE','MONTH','YEAR', 'BILL_NUMBER', 'REGISTRATION_NUMBER', 'NAME',
            'CASH_RECEIVED', 'ONLINE_RECEIVED'
        ]
        widgets = {
            'DATE': DATE_WIDGET,
            'MONTH': forms.Select(),
            'YEAR': forms.Select(),
        }

for model in [ NAGERCOILINTERNSHIPBILL, NAGERCOILPRODUCTBILL, TIRUNELVELIINTERNSHIPBILL, TIRUNELVELIPRODUCTBILL, PUDUKOTTAIINTERNSHIPBILL, PUDUKOTTAIPRODUCTBILL,CHENNAIINTERNSHIPBILL, CHENNAIPRODUCTBILL]:
    
    form_class = type(f"{model.__name__}Form", (BaseBillForm,), {'Meta': type('Meta', (), {'model': model, **BaseBillForm.Meta.__dict__})})
    globals()[form_class.__name__] = form_class

from decimal import Decimal, InvalidOperation

class AbstractTaxInvoiceForm(forms.ModelForm):
    TOTAL_AMOUNT = forms.CharField(required=False)
    GST_18 = forms.CharField(required=False)
    TOTAL_AMOUNT_WITH_GST = forms.CharField(required=False)
    ROUND_OFF = forms.CharField(required=False)
    GRAND_TOTAL = forms.CharField(required=False)

    class Meta:
        fields = [
            'INVOICE_NO', 'DATE', 'BILL_TO',
            'TOTAL_AMOUNT', 'GST_18', 'TOTAL_AMOUNT_WITH_GST', 
            'ROUND_OFF', 'GRAND_TOTAL', 'AMOUNT_IN_WORDS'
        ]
        widgets = {
            'DATE': forms.DateInput(attrs={'type': 'date'}),
            'BILL_TO': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter Billing Address'}),
            'AMOUNT_IN_WORDS': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Amount in Words'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        numeric_fields = ['TOTAL_AMOUNT', 'GST_18', 'TOTAL_AMOUNT_WITH_GST', 'ROUND_OFF', 'GRAND_TOTAL']
        for field in numeric_fields:
            val = cleaned_data.get(field)
            if val:
                try:
                    # Handle commas and the '+' prefix from JS
                    cleaned_val = val.replace(',', '').replace('+', '')
                    cleaned_data[field] = Decimal(cleaned_val)
                except (InvalidOperation, ValueError):
                    self.add_error(field, "Invalid number format")
        return cleaned_data

class AbstractTaxInvoiceItemForm(forms.ModelForm):
    S_NO = forms.CharField()
    QTY = forms.CharField()
    UNIT_PRICE = forms.CharField()
    TOTAL_VALUE = forms.CharField()

    class Meta:
        fields = ['S_NO', 'DESCRIPTION', 'QTY', 'UNIT_PRICE', 'TOTAL_VALUE']
        widgets = {
            'DESCRIPTION': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Item Description'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Clean numeric fields
        field_conversions = {
            'S_NO': int,
            'QTY': int,
            'UNIT_PRICE': Decimal,
            'TOTAL_VALUE': Decimal
        }
        for field, target_type in field_conversions.items():
            val = cleaned_data.get(field)
            if val:
                try:
                    raw_val = val.replace(',', '')
                    if '.' in raw_val and target_type == int:
                        # Handle case where user types 1.00 for an integer
                        cleaned_data[field] = int(float(raw_val))
                    else:
                        cleaned_data[field] = target_type(raw_val)
                except (InvalidOperation, ValueError, TypeError):
                    self.add_error(field, f"Invalid {field} format")
        return cleaned_data

class NagercoilTaxInvoiceForm(AbstractTaxInvoiceForm):
    class Meta(AbstractTaxInvoiceForm.Meta):
        model = NAGERCOILTAXINVOICE

NagercoilTaxInvoiceItemFormSet = inlineformset_factory(
    NAGERCOILTAXINVOICE, NagercoilTAXINVOICEITEM, form=AbstractTaxInvoiceItemForm, extra=1, can_delete=True
)

class TirunelveliTaxInvoiceForm(AbstractTaxInvoiceForm):
    class Meta(AbstractTaxInvoiceForm.Meta):
        model = TIRUNELVELITAXINVOICE

TirunelveliTaxInvoiceItemFormSet = inlineformset_factory(
    TIRUNELVELITAXINVOICE, TIRUNELVELITAXINVOICEITEM, form=AbstractTaxInvoiceItemForm, extra=1, can_delete=True
)

class PudukottaiTaxInvoiceForm(AbstractTaxInvoiceForm):
    class Meta(AbstractTaxInvoiceForm.Meta):
        model = PUDUKOTTAITAXINVOICE

PudukottaiTaxInvoiceItemFormSet = inlineformset_factory(
    PUDUKOTTAITAXINVOICE, PUDUKOTTAITAXINVOICEITEM, form=AbstractTaxInvoiceItemForm, extra=1, can_delete=True
)

class ChennaiTaxInvoiceForm(AbstractTaxInvoiceForm):
    class Meta(AbstractTaxInvoiceForm.Meta):
        model = CHENNAITAXINVOICE

ChennaiTaxInvoiceItemFormSet = inlineformset_factory(
    CHENNAITAXINVOICE, CHENNAITAXINVOICEITEM, form=AbstractTaxInvoiceItemForm, extra=1, can_delete=True
)

class AbstractComponentForm(forms.ModelForm):
    class Meta:
        fields = ['COMPONENT_CODE', 'COMPONENT_NAME', 'RANGE', 'AVAILABLE_QUANTITY', 'TOTAL_STOCK']
        widgets = {
            'COMPONENT_CODE': forms.TextInput(attrs={'class': 'form-control'}),
            'COMPONENT_NAME': forms.TextInput(attrs={'class': 'form-control'}),
            'RANGE': forms.TextInput(attrs={'class': 'form-control'}),
            'AVAILABLE_QUANTITY': forms.NumberInput(attrs={'class': 'form-control'}),
            'TOTAL_STOCK': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class NagercoilComponentForm(AbstractComponentForm):
    class Meta(AbstractComponentForm.Meta):
        model = NagercoilComponent

class StockAdjustmentForm(forms.Form):
    COMPONENT = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    QUANTITY = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))

class GlobalComponentForm(forms.Form):
    COMPONENT_CODE = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Component Code'}))
    COMPONENT_NAME = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Component Name'}))
    CATEGORY = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Category (e.g. CAPACITORS)'}))
    RANGE = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Range'}))
