from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, FormView, UpdateView, DetailView
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Instructor, InstructorProfile, Availability, Reservation
from .forms import RegisterInstructorForm, RegisterClientForm, InstructorProfileForm, ReservationForm, AvailabilityForm, ReservationForm, ConfirmationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from operator import attrgetter




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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        instructor_profile = InstructorProfile.objects.get(pk=self.kwargs['pk'])

        instructor = Instructor.objects.get(pk=self.kwargs['pk'])
        availabilities = Availability.objects.filter(instructor=instructor, date__gte=timezone.now().date())
        
        context['instructor'] = instructor_profile
        context['availabilities'] = availabilities

        return context


class AddAvailabilityView(LoginRequiredMixin, View):
    template_name = 'driving_instructor/instructorAvailabilityView.html'
    form_class = AvailabilityForm

    def get(self, request):
        form = self.form_class()
        instructor = Instructor.objects.get(user=request.user)

        # Get availabilities assigned to instructor, only from future
        availabilities = Availability.objects.filter(instructor=instructor, date__gte=timezone.now().date())

        # Sorting availabilities from the nearest date
        sorted_availabilities = sorted(availabilities, key=attrgetter('date', 'start_time'))

        return render(request, self.template_name, {'form': form, 'availabilities': sorted_availabilities})

    def post(self, request):
        form = self.form_class(request.POST)
        # Get login instructor 
        instructor = Instructor.objects.get(user=request.user)
        if form.is_valid():
            
            # Get data from form
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            # Create object of Availability and save to database
            availability = Availability(instructor=instructor, date=date, start_time=start_time, end_time=end_time)
            availability.save()
            messages.success(self.request, 'Dostępność została pomyślnie dodana.')
            return redirect('instructor_availability')
        
        availabilities = Availability.objects.filter(instructor=instructor, date__gte=timezone.now().date())
        messages.error(self.request, 'Bład podczas zapisu informacj.')
        return render(request, self.template_name, {'form': form, 'availabilities': availabilities})


class ReserveAvailabilityView(LoginRequiredMixin, View):
    template_name = 'driving_instructor/reserveAvailability.html'
    form_class = ReservationForm

    def get(self, request, availability_id):
        availability = Availability.objects.get(pk=availability_id)
        form = self.form_class(initial={'date': availability.date, 'start_time': availability.start_time, 'end_time': availability.end_time})
        return render(request, self.template_name, {'form': form, 'availability': availability})

    def post(self, request, availability_id):
        availability = Availability.objects.get(pk=availability_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.instructor = availability.instructor
            reservation.save()
            return redirect('home') #change to redirect to some success url
        return render(request, self.template_name, {'form': form, 'availability': availability})


class ReserveAvailabilityView(FormView):
    template_name = 'driving_instructor/reserveAvailability.html'
    form_class = ReservationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        availability_id = self.kwargs['availability_id']
        availability = Availability.objects.get(pk=availability_id)
        context['availability'] = availability
        return context

    def form_valid(self, form):
        availability_id = self.kwargs['availability_id']
        availability = Availability.objects.get(pk=availability_id)
        
        # Getting data from form
        instructor = availability.instructor
        user = self.request.user
        date = availability.date
        start_time = availability.start_time
        end_time = availability.end_time
        comment = form.cleaned_data['comment']

        # Create new object Reservation and save to db
        reservation = Reservation(instructor=instructor, user=user, date=date, start_time=start_time, end_time=end_time, comment=comment)
        reservation.save()
        
        return redirect('confirmation')  # Where redirect after successfully reservation?


class ConfirmationView(TemplateView):
    template_name = 'driving_instructor/confirmationView.html'


class InstructorReservationView(FormView):
    template_name = 'driving_instructor/instructorReservationsView.html'
    form_class = ConfirmationForm  
    success_url = reverse_lazy('instructor_reservations')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = Reservation.objects.filter(
            instructor=self.request.user.instructor,
            is_confirmed=False
        )
        return context

    def form_valid(self, form):
        reservation_id = form.cleaned_data['reservation_id']
        reservation = Reservation.objects.get(pk=reservation_id)
        action = form.cleaned_data['action']

        if action == 'confirm':
            reservation.is_confirmed = True
            reservation.save()
        elif action == 'reject':
            reservation.delete()

        return super().form_valid(form)


class InstructorConfirmReservationView(View):
    
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, instructor=request.user.instructor, is_confirmed=False)
        reservation.is_confirmed = True
        reservation.save()
        return redirect('instructor_reservations')

class InstructorRejectReservationView(View):
    
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, instructor=request.user.instructor, is_confirmed=False)
        reservation.delete()
        return redirect('instructor_reservations')
    

class UserReservationsView(LoginRequiredMixin, ListView):
    """
    Class view for list user reservations.
    """
    template_name = 'driving_instructor/UserReservationsView.html'
    model = Reservation
    context_object_name = 'reservations'

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(user=user)
     