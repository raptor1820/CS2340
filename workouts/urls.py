from django.urls import path
from . import views

urlpatterns = [
    path('', views.workout_list, name='workout_list'),
    path('create/', views.workout_create, name='workout_create'),
    path('<int:workout_id>/', views.workout_detail, name='workout_detail'),
    path('<int:workout_id>/edit/', views.workout_edit, name='workout_edit'),
    path('<int:workout_id>/delete/', views.workout_delete, name='workout_delete'),
    
    path('<int:workout_id>/add-exercise/', views.add_exercise_to_workout, name='add_exercise_to_workout'),
    path('<int:workout_id>/exercise/<int:exercise_id>/edit/', views.edit_workout_exercise, name='edit_workout_exercise'),
    path('<int:workout_id>/exercise/<int:exercise_id>/delete/', views.delete_workout_exercise, name='delete_workout_exercise'),
]
