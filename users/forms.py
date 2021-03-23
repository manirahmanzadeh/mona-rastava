# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from users.models import Company
from users.models import TeamModel
from hrm.models import Project
from hrm.models import Team
from hrm.models import Position
from hrm.models import Candidate




class CreateTeamForm(forms.Form):
    teamName = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "TeamName",
                "class" : "form-control"
            }
        )
    )

    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        empty_label="Select Company"
    )

    teamModel = forms.ModelChoiceField(
        queryset=TeamModel.objects.all(),
        empty_label="Select TeamModel"
    )

    teamLead = forms.ModelChoiceField(
        queryset=Candidate.objects.all(),
        empty_label="Select TeamLead"
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        empty_label="Select Project"
    )


    # file = forms.FileField()


class CompanyFirstStepForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        empty_label="Select Company"
    )

    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        empty_label="Team Name"
    )

    openPosition = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        empty_label="Open Positions",
        # widget=AutoCompleteWidget(
        #     url='/custom-json-query',
        #     initial_display='John Smith'
        # )
    )



class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))


'''
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('custom_field',)
'''


class SignUpForm(UserCreationForm):
    '''username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))'''
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


'''class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(validators=[validate_password],
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control",
                "id":"myInput"
            }
        ))
        
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))

    class Meta(UserCreationForm):
        model = User
        fields = ('email','password')'''