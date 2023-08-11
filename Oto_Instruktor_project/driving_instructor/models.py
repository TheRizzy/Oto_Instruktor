from django.db import models
from django.contrib.auth.models import User

class Instructor(models.Model):
    """
    Class model instructor in relation OneToOne to build-in User to define if user is instructor. On default False
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_instructor = models.BooleanField(default=False)
    legitimacy = models.ImageField(upload_to='legitimacy/', null=True, blank=True)


    def __str__(self):
        """
        Magic method to override and show username instructor for example in admin panel
        """
        return self.user.username


class InstructorProfile(models.Model):
    """
    Class model for profile data of instructor.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    personal_data = models.TextField()
    company_data = models.TextField()
    work_region = models.TextField()
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    availability = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Availability(models.Model):
    """
    Class model for adding availability time for instructors to make a lesson.
    """
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.instructor} - {self.date} - {self.start_time} - {self.end_time}"


class Reservation(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    comment = models.TextField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.instructor} & {self.user} - {self.date} - {self.start_time} - {self.end_time}"

 