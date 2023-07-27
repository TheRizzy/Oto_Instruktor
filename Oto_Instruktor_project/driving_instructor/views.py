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


class RegisterView(TemplateView):
    """
    Class view for registration form view.
    """

    template_name = 'driving_instructor/registerFormView.html'
