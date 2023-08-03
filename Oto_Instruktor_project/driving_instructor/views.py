from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, FormView, UpdateView, DetailView
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Instructor, InstructorProfile, Availability, Reservation
from .forms import RegisterInstructorForm, RegisterClientForm, InstructorProfileForm, ReservationForm, AvailabilityForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone



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
    model = InstructorProfile
    template_name = 'driving_instructor/instructorsListView.html'
    context_object_name = 'instructors'


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


class InstructorDetailView(DetailView):
    model = InstructorProfile
    template_name = 'driving_instructor/instructorDetail.html'
    context_object_name = 'instructor'




class AddAvailabilityView(LoginRequiredMixin, View):
    template_name = 'driving_instructor/instructorAddAvailabilityView.html'
    form_class = AvailabilityForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Get login instructor 
            instructor = Instructor.objects.get(user=request.user)

            # Get data from form
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            # Create object of Availability and save to database
            availability = Availability(instructor=instructor, date=date, start_time=start_time, end_time=end_time)
            availability.save()
            messages.success(self.request, 'Dostępność została pomyślnie dodana.')
            return redirect('instructor_add_availability')
        return render(request, self.template_name, {'form': form})


class InstructorAvailabilityView(LoginRequiredMixin, View):
    template_name = 'driving_instructor/instructorAvailabilityView.html'

    def get(self, request):
        # Get login
        instructor = Instructor.objects.get(user=request.user)

        # Get availabilities assigned to instructor
        availabilities = Availability.objects.filter(instructor=instructor, date__gte=timezone.now().date())
        return render(request, self.template_name, {'availabilities': availabilities})

# @login_required
# def instructor_detail(request, instructor_id):
#     # Wyświetlenie szczegółów instruktora, wraz z wolnymi terminami zajęć



# @login_required
# def make_reservation(request, instructor_id, date, start_time, end_time):
#     if request.method == 'POST':
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             # Obsługa zapisu rezerwacji
#     else:
#         # Wyświetlenie formularza do rezerwacji zajęć

# @login_required
# def instructor_reservations(request, instructor_id):
#     # Wyświetlenie listy rezerwacji dla danego instruktora

# @login_required
# def confirm_reservation(request, reservation_id):
#     # Obsługa potwierdzenia rezerwacji przez instruktora

# @login_required
# def reject_reservation(request, reservation_id):
#     # Obsługa odrzucenia rezerwacji przez instruktora
