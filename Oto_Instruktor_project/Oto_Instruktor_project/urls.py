"""
URL configuration for Oto_Instruktor_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from driving_instructor import views as ex_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ex_views.mainPage.as_view(), name='home'),
    path('register_client/', ex_views.RegisterClient.as_view(), name='register_client'),
    path('register_instructor/', ex_views.RegisterInstructor.as_view(), name='register_instructor'),
    path('login/', ex_views.loginView.as_view(), name='login'),
    path('logout/', ex_views.logoutView.as_view(), name='logout'),
    path('instructors_list/', ex_views.instructorListView.as_view(), name='instructors_list'),
    path('instructor_profile/<int:pk>/', ex_views.InstructorProfileView.as_view(), name='instructor_profile'),
    path('instructor_detail/<int:pk>', ex_views.InstructorDetailView.as_view(), name='instructor_detail'),
    path('instructor_availability/', ex_views.AddAvailabilityView.as_view(), name='instructor_availability'),
    path('reserve_availability/<int:availability_id>/', ex_views.ReserveAvailabilityView.as_view(), name='reserve_availability'),
    path('confirmation/', ex_views.ConfirmationView.as_view(), name='confirmation'),
    path('instructor_reservations/', ex_views.InstructorReservationView.as_view(), name='instructor_reservations'),
    path('instructor_confirm_reservation/<int:pk>', ex_views.InstructorConfirmReservationView.as_view(), name='instructor_confirm_reservation'),
    path('instructor_reject_reservation/<int:pk>', ex_views.InstructorRejectReservationView.as_view(), name='instructor_reject_reservation'),
    path('user_reservations/', ex_views.UserReservationsView.as_view(), name='user_reservations'),
    path('delete_availability/<int:pk>/', ex_views.DeleteAvailabilityView.as_view(), name='delete_availability'),


]
