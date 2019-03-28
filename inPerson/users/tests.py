from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your tests here.
class UsersTest(APITestCase):
    client = APIClient()

    def setUp(self):
        User = get_user_model()
        user1 = User.objects.create_user(first_name="John", last_name="Doe", username="jdoe", class_year=2021, password="password", email="j@princeton.edu")
        User.objects.create_user(first_name="Rob", last_name="Sedgewick", username="rsedgewick", class_year=2022, password="password")

    def test_create_user(self):
        User = get_user_model()
        user_jdoe = User.objects.get(username="jdoe")
        self.assertEqual(str(user_jdoe), "jdoe")
        self.assertEqual(user_jdoe.get_name(), "John Doe")
