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
    legitimacy = forms.ImageField(required=False) # in future need to be required=True

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

class RegisterClientForm(UserCreationForm):
    """
    Class form for register default Client.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nazwa uzytkownika',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Email',
            'password1': 'Hasło',
            'password2': 'Powtórz hasło',
        }

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
