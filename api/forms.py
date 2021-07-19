from django import forms
from django.forms import TextInput, CharField, DateField

class DateInput(forms.DateInput):
    input_type = 'date'

class BBForm(forms.Form):
    ticker = CharField(widget=TextInput(attrs={'class': 'form-control'}))
    variable = CharField(widget=TextInput(attrs={'class': 'form-control'}))
    start_date = DateField(widget=DateInput(attrs={'class': 'form-control'}))
    end_date = DateField(widget=DateInput(attrs={'class': 'form-control'}))