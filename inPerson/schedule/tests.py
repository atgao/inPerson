from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from datetime import time

from .models import Section
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


class SectionToEvent(APITestCase):
    """
    Test that a section can become a recurrent event
    """
    def setUp(self):
        #create a temporary user and schedule
        User = get_user_model()
        User.objects.create_user(first_name="Rob", last_name="Sedgewick", username="rsedgewick", class_year=2022, password="password")
        user1 = User.objects.get(username="rsedgewick")
        Schedule.objects.create(semester="S19", owner=user1)
        days = ["T", "Th"]
        start_time = time(11)
        end_time = time(12, 20)
        Section.objects.create(class_number=40063, code="COS", catalog_number="333",
                                title="Advanced Programming Techniques",start_time=start_time,
                                end_time=end_time, days=days, location="BOWEN 222")

    def test_convert_section_to_event(self):
        a_class = Section.objects.get(class_number="40063")
        #e = RecurrentEvent()
        # e.objects.create_event_from_section(a_class)
        RecurrentEvent.objects.create_event_from_section(a_class)
