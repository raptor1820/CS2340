from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Workout, WorkoutCategory, Exercise, WorkoutExercise
from django import forms

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['title', 'date', 'start_time', 'end_time', 'category', 'notes', 'intensity', 'calories_burned']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'sets', 'reps', 'weight', 'duration', 'distance', 'notes', 'order']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

@login_required
def workout_list(request):
    """Display all workouts for the current user"""
    workouts = Workout.objects.filter(user=request.user).order_by('-date', '-start_time')
    return render(request, 'workouts/workout_list.html', {'workouts': workouts})

@login_required
def workout_detail(request, workout_id):
    """Display details of a specific workout"""
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    exercises = workout.workout_exercises.all().order_by('order')
    return render(request, 'workouts/workout_detail.html', {
        'workout': workout,
        'exercises': exercises
    })

@login_required
def workout_create(request):
    """Create a new workout"""
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            messages.success(request, 'Workout created successfully!')
            return redirect('workout_detail', workout_id=workout.id)
    else:
        form = WorkoutForm(initial={'date': timezone.now().date()})
    
    return render(request, 'workouts/workout_form.html', {
        'form': form,
        'title': 'Create Workout'
    })

@login_required
def workout_edit(request, workout_id):
    """Edit an existing workout"""
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            messages.success(request, 'Workout updated successfully!')
            return redirect('workout_detail', workout_id=workout.id)
    else:
        form = WorkoutForm(instance=workout)
    
    return render(request, 'workouts/workout_form.html', {
        'form': form,
        'workout': workout,
        'title': 'Edit Workout'
    })

@login_required
def workout_delete(request, workout_id):
    """Delete a workout"""
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    
    if request.method == 'POST':
        workout.delete()
        messages.success(request, 'Workout deleted successfully!')
        return redirect('workout_list')
    
    return render(request, 'workouts/workout_confirm_delete.html', {'workout': workout})

@login_required
def add_exercise_to_workout(request, workout_id):
    """Add an exercise to a workout"""
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    
    if request.method == 'POST':
        form = WorkoutExerciseForm(request.POST)
        if form.is_valid():
            workout_exercise = form.save(commit=False)
            workout_exercise.workout = workout
            workout_exercise.save()
            messages.success(request, 'Exercise added to workout!')
            return redirect('workout_detail', workout_id=workout.id)
    else:
        next_order = workout.workout_exercises.count() + 1
        form = WorkoutExerciseForm(initial={'order': next_order})
    
    return render(request, 'workouts/workout_exercise_form.html', {
        'form': form,
        'workout': workout,
        'title': 'Add Exercise to Workout'
    })

@login_required
def edit_workout_exercise(request, workout_id, exercise_id):
    """Edit an exercise in a workout"""
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    workout_exercise = get_object_or_404(WorkoutExercise, id=exercise_id, workout=workout)
    
    if request.method == 'POST':
        form = WorkoutExerciseForm(request.POST, instance=workout_exercise)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exercise updated successfully!')
            return redirect('workout_detail', workout_id=workout.id)
    else:
        form = WorkoutExerciseForm(instance=workout_exercise)
    
    return render(request, 'workouts/workout_exercise_form.html', {
        'form': form,
        'workout': workout,
        'workout_exercise': workout_exercise,
        'title': 'Edit Exercise'
    })

@login_required
def delete_workout_exercise(request, workout_id, exercise_id):
    """Delete an exercise from a workout"""
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    workout_exercise = get_object_or_404(WorkoutExercise, id=exercise_id, workout=workout)
    
    if request.method == 'POST':
        workout_exercise.delete()
        # Reorder remaining exercises
        for i, exercise in enumerate(workout.workout_exercises.all().order_by('order')):
            exercise.order = i + 1
            exercise.save()
        messages.success(request, 'Exercise removed from workout!')
        return redirect('workout_detail', workout_id=workout.id)
    
    return render(request, 'workouts/workout_exercise_confirm_delete.html', {
        'workout': workout,
        'workout_exercise': workout_exercise
    })
