from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import SignupSerializer
from django.core.exceptions import ValidationError
from .validators import CustomPasswordValidator


class SignupViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup_view(self):
        # Define test data
        data = {
            "username": "testuser",
            "password": "Testpassword123!",
        }

        # Make a POST request to the SignupView
        response = self.client.post("/accounts/api/signup", data, format="json")

        # Check if the response status code is 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if a user with the given username exists in the database
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_invalid_signup_view(self):
        # Define invalid test data (missing required field)
        data = {
            "password": "testpassword",
        }

        # Make a POST request to the SignupView with invalid data
        response = self.client.post("/accounts/api/signup", data, format="json")

        # Check if the response status code is 400 (bad request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if a user with the given username does not exist in the database
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_password_validation(self):
        # Test valid password
        valid_password = "Testpassword123!"
        validator = CustomPasswordValidator()
        try:
            validator.validate(valid_password)
        except ValidationError:
            self.fail(f"Validation for a valid password failed: {valid_password}")

        # Test invalid password (too short)
        invalid_password_short = "Short1"
        with self.assertRaises(ValidationError):
            validator.validate(invalid_password_short)

        # Test invalid password (missing digit)
        invalid_password_no_digit = "NoDigitUpperCase"
        with self.assertRaises(ValidationError):
            validator.validate(invalid_password_no_digit)

        # Test invalid password (missing special character)
        invalid_password_no_special = "NoSpecial123"
        with self.assertRaises(ValidationError):
            validator.validate(invalid_password_no_special)
