from django.contrib import admin
from .models import Instructor,InstructorProfile, Availability, Reservation

# Register your models here.

admin.site.register(Instructor)
admin.site.register(InstructorProfile)
admin.site.register(Availability)
admin.site.register(Reservation)



