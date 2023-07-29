from django.shortcuts import render
from .models import User
from django.views import View
from django.views.generic import ListView, TemplateView



class mainPage(ListView):
    """
    Class view for home page, with display list of instructors and button for registration.
    """
    model = User
    template_name = 'driving_instructor/mainPageView.html'
    context_object_name = 'instructors'

    def get_queryset(self):
        # get list of instructors 
        return User.objects.filter(instructor=True)


class RegisterInstructor(TemplateView):
    """
    Class view for registration Instructor.
    """

    template_name = 'driving_instructor/registerFormInstructor.html'


class RegisterClient(TemplateView):
    """
    Class view for registration Client.
    """

    template_name = 'driving_instructor/registerFormClient.html'
