# forms.py
from django import forms

class TransferForm(forms.Form):
    receiver_account_number = forms.CharField(label='Receiver Account Number', max_length=10)
    amount = forms.DecimalField(label='Amount', min_value=0.01)
