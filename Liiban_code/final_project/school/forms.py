from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
class ContactForm(forms.Form):

    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "20", }))

class SignupForm(forms.Form):
    GENDER_CHOICES = (
            ('M', 'Male'),
            ('F', 'Female'),
    )
    #must include data for each of the following fields

    first_name = forms.CharField(label="First name",max_length=30)
    surname = forms.CharField(label="Surname",max_length=30)
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1940, 2018)),label="Date of birth")
    username = forms.CharField(label="Enter username",max_length=16)
    email = forms.EmailField(label="Enter email")
    password = forms.CharField(widget=forms.PasswordInput,label="Enter password",max_length=16)
    password1 = forms.CharField(widget=forms.PasswordInput,label="Re-enter password",max_length=16)
    gender = forms.ChoiceField(widget=forms.RadioSelect,choices =GENDER_CHOICES)

class LoginForm(forms.Form):
    username = forms.CharField(label="Enter username",max_length=16)
    password = forms.CharField(widget=forms.PasswordInput, label="Enter password",max_length=16)


class UserUpdate(forms.ModelForm):
    username = forms.CharField(label="Enter username",max_length=16)
    email = forms.EmailField(label="Enter email")

    class Meta:
        model = User
        fields = ['username', 'email']
