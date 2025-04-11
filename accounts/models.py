from django.db import models
from django.contrib.auth.models import AbstractUser

class FitUser(AbstractUser):
    email = models.EmailField(unique = True)
    age = models.PositiveIntegerField(null = True, blank = True)
    height_in = models.PositiveIntegerField(null = True, blank = True)
    weight_lb = models.PositiveIntegerField(null = True, blank = True)
    bio = models.TextField(blank=True)
    totalWorkouts = models.PositiveIntegerField(null = True, blank = True)
    totalCalBurned = models.PositiveIntegerField(null = True, blank = True)
    workoutCountHistory = []
    calBurnedHistory = []

    def heightConvert(self):
        if self.height is None:
            return f"No provided height"
        feet = self.height_in // 12
        inches = self.height_in % 12
        return f"{feet} ft. and {inches} in."

    def __str__(self):
        height = self.heightConvert()
        return f"{self.first_name} has a height of {height} and weight of {self.weight_lb}."