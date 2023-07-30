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

    # Here can add new fields to user models like: license number, photo of license? etc.



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

    def __str__(self):
        return f"{self.user.username} - {self.title}"
