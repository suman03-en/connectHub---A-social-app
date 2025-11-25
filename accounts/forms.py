from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from .mixins import UsernameEmailUniqueCheckMixin
from .models import CustomUser


class CustomRegistrationForm(UsernameEmailUniqueCheckMixin,UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email','username','profile_pic')

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label = 'Email/Username')

class PasswordResetForm(forms.Form):
    password1 = forms.CharField(label="New password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="New password confirm",widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1!=password2:
            raise ValidationError("Two password didn't match.")

class ProfileForm(forms.ModelForm,UsernameEmailUniqueCheckMixin):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email','bio','profile_pic']
    

        