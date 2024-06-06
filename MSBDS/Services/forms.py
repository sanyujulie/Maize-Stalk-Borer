from django import forms
from Services.models import *
from django.forms import ModelForm
from django.core.validators import FileExtensionValidator
from django.core.validators import EmailValidator, RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from djmoney.forms.fields import MoneyField
from djmoney.money import Money
import re




def validate_not_entirely_numeric(value):
    if value.isdigit():
        raise ValidationError("Package name cannot be entirely numeric.")

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget= forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "username",
                "name": "username",
                "id": "username"
                }
            )
        )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "password",
                "name": "password",
                "id": "password"
            }
        )
    )
    

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(3, message='Username must be at least 3 characters long.'),
            MaxLengthValidator(25, message='Username cannot have more than 25 characters.'),
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='Enter a valid username: Only letters, numbers, and underscores are allowed.'
            ),
        ],
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "Username", 'name': 'username', 'id': 'username'})
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-sm", "placeholder": "Password", 'name': 'password', 'id': 'password'}),
        validators=[
            MinLengthValidator(8, message='Password must be at least 8 characters long.'),
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$',
                message='Password must contain at least one uppercase letter, one lowercase letter, and one number.'
            ),
        ]
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-sm", "placeholder": "Confirm Password", 'name': 'confirm_password', 'id': 'confirm_password'})
    )

    admin_role = forms.ChoiceField(
        choices=CustomUser.ADMIN_ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control form-control-sm", "placeholder": "Admin Role", 'name': 'admin_role', 'id': 'admin_role'}),
        required=True,
        label="Admin Role"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'confirm_password', 'admin_role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user




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
    severity_level = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Severity_level', 'name': 'severity_level', 'id': 'severity_level'})
    )
    class Meta:
        model = Farmer
        fields = ['username','farmSize', 'farmLocation', 'contact','severity_level']


