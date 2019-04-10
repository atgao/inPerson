from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from datetime import time

from .models import Section, RecurrentEvent, Schedule
from .serializers import SectionsSerializer, RecurrentEventsSerializer, SchedulesSerializer

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
        Schedule.objects.create(term="S2019", owner=user1)

    def test_schedule_to_a_user(self):
        user1 = User.objects.get(username="rsedgewick")
        a_schedule = Schedule.objects.get(owner=user1)
        self.assertEqual(a_schedule.term, "S2019")
        self.assertEqual(a_schedule.owner.username, "rsedgewick")

class MostRecentSchedule(APITestCase):
    """
    Test that we are getting the most recent schedule
    """
    def setUp(self):
        # create a temporary user
        User = get_user_model()
        User.objects.create_user(first_name="Rob", last_name="Sedgewick", username="rsedgewick", class_year=2022, password="password")
        user1 = User.objects.get(username="rsedgewick")
        Schedule.objects.create(term="S2019", owner=user1)
        Schedule.objects.create(term="F2018", owner=user1)
        Schedule.objects.create(term="F2019", owner=user1)

    def test_get_most_recent_schedule(self):
        user1 = User.objects.get(username="rsedgewick")
        schedule = Schedule.objects.get_current_schedule_for_user(user1)
        self.assertEqual(schedule.term, "S2019")
