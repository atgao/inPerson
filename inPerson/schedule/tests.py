from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import RecurrentEvent
from .models import Schedule
from users.models import User

# Create your tests here.
# class RecurrentEventsTest(APITestCase):
#     client = APIClient()
#
#     @classmethod
#     def setup_test_data():
#         #set up a user
#         user = User.objects.create(first_name="John", last_name="Doe", class_year="test@example.com")
#
#     def create_recurrentevent(title="", start_time="", end_time="", days="", location=""):
#         if title != "" and artist != "":
#             Songs.objects.create(title=title, artist=artist)
