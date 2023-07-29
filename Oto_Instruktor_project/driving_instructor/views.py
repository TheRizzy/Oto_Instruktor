from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import User, Instructor
from django.views import View
from django.views.generic import ListView, TemplateView, FormView
from .forms import RegisterInstructorForm, RegisterClientForm



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


class RegisterInstructor(FormView):
    """
    Class view for registration Instructor.
    """
    model = Instructor
    form_class = RegisterInstructorForm
    template_name = 'driving_instructor/registerFormInstructor.html'
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        """
        This method is called when valid form data has been POSTed.
        It should return an HttpResponse.
        In my case this function save new user to database and create relation in Instructors with that user
        """
        user = form.save()
        Instructor.objects.create(user=user, is_instructor=True, legitimacy=form.cleaned_data['legitimacy'])
        return super().form_valid(form)



class RegisterClient(FormView):
    """
    Class view for registration Client.
    """
    form_class = RegisterClientForm
    template_name = 'driving_instructor/registerFormClient.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        his method is called when valid form data has been POSTed.
        It should return an HttpResponse.
        In my case this function save new user to database as User 
        """
        form.save()
        return super().form_valid(form)

