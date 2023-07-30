from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView, FormView, UpdateView
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Instructor, InstructorProfile
from .forms import RegisterInstructorForm, RegisterClientForm, InstructorProfileForm



class mainPage(TemplateView):
    """
    Class view for home page and display of login user.
    """
    template_name = 'driving_instructor/mainPageView.html'
    
    def get_context_data(self, **kwargs):
        """
        Method who allows to add additional data to the template context.
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class instructorListView(ListView):
    """
    Class view for display list of instructors.
    """
    model = User
    template_name = 'driving_instructor/listInstructorsView.html'
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
        This method is called when valid form data has been POSTed.
        It should return an HttpResponse.
        In my case this function save new user to database as User 
        """
        form.save()
        return super().form_valid(form)


class loginView(LoginView):
    """
    Class view for login 
    """
    template_name = 'driving_instructor/login.html'
    redirect_authenticated_user = True # Redirect login users to home page
    
    def get_success_url(self):
        """
        Redirect login user to home page
        """
        return reverse_lazy('home') 
    
class logoutView(LogoutView):
    """
    Class view for logout. After logout user will be redirect to home view.
    """
    next_page = 'home'


class InstructorProfileView(LoginRequiredMixin, UpdateView):
    """
    Class view for view and edit profile of instructor.
    """

    form_class = InstructorProfileForm
    template_name = 'driving_instructor/instructorProfileView.html'


    def get_success_url(self) -> str:
        """
        Function to dynamic build url with login user primary key
        """
        return reverse('instructor_profile', args=[self.request.user.pk])
    
    
    def get_object(self, queryset=None):
        """
        Function to find instructor base on login user primary key
        """
        try:
            profile = self.request.user.instructorprofile
        except InstructorProfile.DoesNotExist:
            # If profile not exist, create new one
            profile = InstructorProfile(user=self.request.user)
            profile.save()

        return profile
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request, 'Informacje zostały pomyślnie zapisane.')
        return response
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        messages.error(self.request, 'Wystąpił bład podczas zapisu informacj.')
        return response