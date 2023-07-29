from django.db import models
from django.contrib.auth.models import User

class Instructor(models.Model):
    """
    Class model instructor in relation OneToOne to build-in User to define if user is instructor. On default False
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_instructor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    # Here can add new fields to user models like: license number, photo of license? etc.
