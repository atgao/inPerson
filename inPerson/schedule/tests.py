from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import RecurrentEvent
from .models import Schedule

# Create your tests here.
class RecurrentEventsTest(APITestCase):
    client = APIClient()

    @classmethod
    def setup_test_data():
        #set up a user
        user = User.objects.create()

    def create_recurrentevent(title="", start_time="", end_time="", days="", location=""):
        if title != "" and artist != "":
            Songs.objects.create(title=title, artist=artist)
