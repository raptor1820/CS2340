from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class WorkoutCategory(models.Model):
    """Category for different types of workouts (e.g., Cardio, Strength, Flexibility)"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Workout Categories"
    
    def __str__(self):
        return self.name

class Exercise(models.Model):
    """TODO add exerciseDB gif integration"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(WorkoutCategory, on_delete=models.CASCADE, related_name='exercises')
    muscle_group = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name

class Workout(models.Model):
    """A complete workout session"""
    INTENSITY_CHOICES = [
        ('L', 'Light'),
        ('M', 'Moderate'),
        ('H', 'High'),
        ('V', 'Very High')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    title = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(null=True, blank=True)
    category = models.ForeignKey(WorkoutCategory, on_delete=models.SET_NULL, null=True, related_name='workouts')
    notes = models.TextField(blank=True)
    intensity = models.CharField(max_length=1, choices=INTENSITY_CHOICES, default='M')
    calories_burned = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date', '-start_time']
    
    def __str__(self):
        return f"{self.title} - {self.date}"
    
    @property
    def duration(self):
        """Calculate workout duration in minutes"""
        if not self.end_time:
            return None
        
        start_datetime = timezone.datetime.combine(timezone.now().date(), self.start_time)
        end_datetime = timezone.datetime.combine(timezone.now().date(), self.end_time)
        
        if end_datetime < start_datetime:  # If workout spans midnight
            end_datetime = end_datetime + timezone.timedelta(days=1)
            
        duration = end_datetime - start_datetime
        return duration.total_seconds() // 60  # Duration in minutes

class WorkoutExercise(models.Model):
    """Junction model connecting exercises to workouts with specific metrics"""
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='workout_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='workout_exercises')
    sets = models.PositiveIntegerField(default=1)
    reps = models.PositiveIntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # in kg/lbs
    duration = models.PositiveIntegerField(null=True, blank=True)  # in seconds
    distance = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # in km/miles
    notes = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)  # To maintain exercise order
    
    class Meta:
        ordering = ['order']
        unique_together = ['workout', 'exercise', 'order']
    
    def __str__(self):
        return f"{self.exercise.name} ({self.sets} sets)"

class UserMetrics(models.Model):
    """User metrics to track progress"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metrics')
    date = models.DateField(default=timezone.now)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in kg/lbs
    body_fat = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)  # percentage
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "User Metrics"
        ordering = ['-date']
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
