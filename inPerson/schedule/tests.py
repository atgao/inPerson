from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import RecurrentEvent
from .models import Schedule

from users.models import User
from django.contrib.auth import get_user_model



class ScheduleTest(APITestCase):
    """
    Test that a schedule belongs to the correct user
    """

    def setUp(self):
        # create a temporary user
        User = get_user_model()
        User.objects.create_user(first_name="Rob", last_name="Sedgewick", username="rsedgewick", class_year=2022, password="password")
        user1 = User.objects.get(username="rsedgewick")
        Schedule.objects.create(semester="S19", owner=user1)

    def test_schedule_to_a_user(self):
        user1 = User.objects.get(username="rsedgewick")
        a_schedule = Schedule.objects.get(owner=user1)
        self.assertEqual(a_schedule.semester, "S19")
        self.assertEqual(a_schedule.owner.username, "rsedgewick")
