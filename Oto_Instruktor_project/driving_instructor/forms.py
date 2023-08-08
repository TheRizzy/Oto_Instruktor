from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Instructor, InstructorProfile, Availability, Reservation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone



class RegisterInstructorForm(UserCreationForm):
    """
    Class form for register Instructors.
    """
    is_instructor = forms.BooleanField()
    legitimacy = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class':'form-control-file'})) 

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_instructor', 'legitimacy']
        labels = {
            'username': 'Nazwa uzytkownika',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Email',
            'password1': 'Hasło',
            'password2': 'Powtórz hasło',
            'is_instructor': 'Potwierdzam, ze jestem certyfikowany instuktorem nauk jazdy',
            'legitimacy': 'Prześlij zdjęcie swojej legitymacji',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Wprowadź swoją nazwę uzytkownika'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Wprowadź swoje imię'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Wprowadź swoje nazwisko'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Wprowadź Twój adres@email.com'}),
            'is_instructor': forms.CheckboxInput(attrs={'class':'form-check','placeholder':'Potwierdzam, ze jestem certyfikowany instuktorem nauk jazdy'}),
            'legitimacy': forms.FileInput(attrs={'class':'form-control-file'}),
        }
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Function to override widget to passwords fields
        """
        super(RegisterInstructorForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Wprowadź hasło'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Powtórz hasło'

class RegisterClientForm(UserCreationForm):
    """
    Class form for register default Client.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Login',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Email',
            'password1': 'Hasło',
            'password2': 'Powtórz hasło',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Wprowadź swoją nazwę uzytkownika'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Wprowadź swoje imię'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Wprowadź swoje nazwisko'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Wprowadź Twój adres@email.com'}),
        }


    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Function to override widget to passwords and email fields
        """
        super(RegisterClientForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Wprowadź Twój adres@email.com'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Wprowadź hasło'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Powtórz hasło'

class InstructorProfileForm(forms.ModelForm):
    """
    Class form for data details to profile of instructor.
    """
    class Meta:
        model = InstructorProfile
        fields = ['title', 'description', 'personal_data', 'company_data', 'work_region', 'hourly_rate']
        labels = {
            'title': 'Twoja nazwa ogłoszenia',
            'description': 'Opis',
            'personal_data': 'Dane osobowe',
            'company_data': 'Dane firmy',
            'work_region': 'Region pracy',
            'hourly_rate': 'Stawka za godzinę jazd dodatkowych'
        }

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Wprowadź swój tytuł ogłoszenia'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Wprowadź swoje opis'}),
            'personal_data': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Wprowadź swoje dane personalne'}),
            'company_data': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Wprowadź swoje dane firmy'}),
            'work_region': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Wprowadź swój region pracy'}),
            'hourly_rate': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Wprowadź swoją cenę od 1h/zł'}),
        }    
        

    def clean_hourly_rate(self):
        """
        Function to block hourly rate below zero.
        """
        hourly_rate = self.cleaned_data.get('hourly_rate')
        if hourly_rate < 0:
            raise forms.ValidationError("Stawka godzinowa nie może być ujemna.")
        return hourly_rate


class AvailabilityForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # Check if date and time is from future
        if date and start_time:
            start_datetime = timezone.datetime.combine(date, start_time)
            if start_datetime < timezone.now():
                raise ValidationError(_("Start time must be in the future."))

        # Check if end_time > start_time
        if start_time and end_time and end_time <= start_time:
            raise ValidationError(_("End time must be after start time."))

        return cleaned_data



class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['comment']


class ConfirmationForm(forms.Form):
    CHOICES = [('confirm', 'Potwierdź'), ('reject', 'Odrzuć')]
    action = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    reservation_id = forms.IntegerField(widget=forms.HiddenInput())
