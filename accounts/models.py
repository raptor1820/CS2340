from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class FitUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

class FitUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    height_in = models.PositiveIntegerField(null=True, blank=True)
    weight_lb = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    totalWorkouts = models.PositiveIntegerField(null=True, blank=True)
    totalCalBurned = models.PositiveIntegerField(null=True, blank=True)
    workoutCountHistory = models.JSONField(default=list, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = FitUserManager()

    USERNAME_FIELD = 'username'  # Default username field used for authentication
    REQUIRED_FIELDS = ['email']  # These fields are required when creating a superuser

    def bmi(self):
        if self.weight_lb and self.height_in:
            return round(703 * (self.weight_lb / (self.height_in ** 2)),2)
        return None

    def heightConvert(self):
        if not self.height_in:
            return "No provided height"
        feet = self.height_in // 12
        inches = self.height_in % 12
        return f"{feet} ft. and {inches} in."

    def __str__(self):
        return f"{self.username}, {self.email}, {self.bmi()}"