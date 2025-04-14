from django.test import TestCase
from django.contrib.auth import get_user_model

class FitUserModelTest(TestCase):
    def test_user_creation(self):
        # Create a user instance
        user = get_user_model().objects.create_user(
            username="fitguy123",
            email="fitguy@example.com",
            password="testpassword",
            first_name="John",
            last_name="Doe",
            age=28,
            height_in=70,
            weight_lb=160,
            totalWorkouts=10,
            totalCalBurned=2000
        )
        print(user)

        # Ensure the user is saved in the database
        self.assertEqual(user.username, "fitguy123")
        self.assertEqual(user.email, "fitguy@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.age, 28)
        self.assertEqual(user.height_in, 70)
        self.assertEqual(user.weight_lb, 160)
        self.assertEqual(user.totalWorkouts, 10)
        self.assertEqual(user.totalCalBurned, 2000)

    def test_bmi_calculation(self):
        # Create a user with known height and weight
        user = get_user_model().objects.create_user(
            username="fitguy123",
            email="fitguy@example.com",
            password="testpassword",
            height_in=70,
            weight_lb=160
        )

        # BMI formula: 703 * (weight / height^2)
        expected_bmi = round(703 * (160 / (70 ** 2)), 2)

        # Ensure the bmi property calculates correctly
        self.assertEqual(user.bmi(), expected_bmi)

    def test_height_conversion(self):
        # Create a user with a known height
        user = get_user_model().objects.create_user(
            username="fitguy123",
            email="fitguy@example.com",
            password="testpassword",
            height_in=73  # 6 feet 1 inch
        )

        # Check that the height is correctly converted to feet and inches
        self.assertEqual(user.heightConvert(), "6 ft. and 1 in.")

    def test_empty_workout_history(self):
        # Create a user with an empty workout history
        user = get_user_model().objects.create_user(
            username="fitguy123",
            email="fitguy@example.com",
            password="testpassword",
            workoutCountHistory=[]
        )

        # Ensure the workout history is empty
        self.assertEqual(user.workoutCountHistory, [])

    def test_workout_history_append(self):
        # Create a user
        user = get_user_model().objects.create_user(
            username="fitguy123",
            email="fitguy@example.com",
            password="testpassword",
            workoutCountHistory=[]
        )

        # Append a workout count to the history
        user.workoutCountHistory.append(5)
        user.save()

        # Reload from the database and check if the history updated
        user.refresh_from_db()
        self.assertEqual(user.workoutCountHistory, [5])

