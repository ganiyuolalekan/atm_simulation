from django import forms
from .models import Customer


class CreateCustomer(forms.ModelForm):
    class Meta:
        model = Customer
        fields = 'full_name', 'account_number', 'amount', 'pin'


class CollectPin(forms.Form):
    pin = forms.CharField(max_length=4)


class CollectNumber(forms.Form):
    number = forms.IntegerField()
