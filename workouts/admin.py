from django.contrib import admin
from .models import WorkoutCategory, Exercise, Workout, WorkoutExercise, UserMetrics

@admin.register(WorkoutCategory)
class WorkoutCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'muscle_group')
    list_filter = ('category', 'muscle_group')
    search_fields = ('name', 'description')

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'start_time', 'end_time', 'category', 'intensity')
    list_filter = ('date', 'category', 'intensity', 'user')
    search_fields = ('title', 'notes')
    inlines = [WorkoutExerciseInline]

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'workout', 'sets', 'reps', 'weight', 'duration', 'distance')
    list_filter = ('workout__date', 'exercise__category')

@admin.register(UserMetrics)
class UserMetricsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'weight', 'body_fat')
    list_filter = ('date', 'user')
