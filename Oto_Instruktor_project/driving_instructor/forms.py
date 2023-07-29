from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Instructor
from django.contrib.auth.models import User

class RegisterInstructorForm(UserCreationForm):
    """
    Class form for register Instructors.
    """
    is_instructor = forms.BooleanField()
    legitimacy = forms.ImageField(required=False) # in future need to be required=True

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_instructor', 'legitimacy']

class RegisterClientForm(UserCreationForm):
    """
    Class form for register default Client.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']