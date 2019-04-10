from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from datetime import time
import json

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
        self.assertEqual(schedule.term, "F2019")

class SectionToEvent(APITestCase):
    """
    Test that a section can become a recurrent event
    """
    def setUp(self):
        #create a temporary user and schedule
        User = get_user_model()
        User.objects.create_user(first_name="Rob", last_name="Sedgewick", username="rsedgewick", class_year=2022, password="password")
        user1 = User.objects.get(username="rsedgewick")
        Schedule.objects.create(term="S2019", owner=user1)
        days = ["T", "Th"]
        start_time = time(11)
        end_time = time(12, 20)
        Section.objects.create(class_number=40063, code="COS", catalog_number="333",
                                title="Advanced Programming Techniques",start_time=start_time,
                                end_time=end_time, days=days, location="BOWEN 222", term="S2019")

    def test_convert_section_to_event(self):
        a_class = Section.objects.get(class_number="40063")
        user1 = User.objects.get(username="rsedgewick")
        a_schedule = Schedule.objects.get(owner=user1)
        e = RecurrentEvent.objects.create_event_from_section(a_schedule, SectionsSerializer(a_class).data)
        self.assertEqual(e.schedule.owner.username, "rsedgewick")
        self.assertEqual(e.schedule.term, "S2019")

class AddSectionToSchedule(APITestCase):
    client = APIClient()

    def setUp(self):
        # create users
        User = get_user_model()
        self.rsedgewick = User.objects.create_user(first_name="Rob", last_name="Sedgewick",
                                             username="rsedgewick", class_year=2022,
                                             password="password")
        Schedule.objects.create(term="S2019", owner=self.rsedgewick)
        days = ["T", "Th"]
        start_time = time(11)
        end_time = time(12, 20)
        Section.objects.create(class_number=40063, code="COS", catalog_number="333",
                                title="Advanced Programming Techniques",start_time=start_time,
                                end_time=end_time, days=days, location="BOWEN 222", term="S2019")

    def test_add_section_to_schedule(self):
        self.client.login(username='rsedgewick', password='password')
        a_section = Section.objects.get(class_number=40063)
        serializer = SectionsSerializer(a_section)
        response = self.client.post(reverse("add-class-to-schedule"),
                                    data=json.dumps(serializer.data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        e = RecurrentEvent.objects.get(location="BOWEN 222")
        # print(e.title)
        # self.assertEqual()
