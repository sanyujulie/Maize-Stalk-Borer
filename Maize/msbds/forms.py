from django import forms
from Services.models import *
from django.forms import ModelForm
from django.core.validators import FileExtensionValidator
from django.core.validators import EmailValidator, RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError

import re



class FarmerForm(ModelForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'name': 'name', 'id': 'name'})
    )
    
   
    farmSize= forms.IntegerField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Farm_size', 'name': 'farmSize', 'id': 'farmSize'})
    )
    
    farmLocation = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location', 'name': 'farmLocation', 'id': 'farmLocation'})
    )
    
    contact = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact', 'name': 'contact', 'id': 'contact'})
    )
    severity = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Severity', 'name': 'severity', 'id': 'severity'})
    )
    class Meta:
        model = Farmer
        fields = ['username','farmSize', 'farmLocation', 'contact','severity']