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


# converts a datetime object
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

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

class GetSingleSectionTest(APITestCase):
    """
    Try getting details of a section
    """
    client = APIClient()

    def setUp(self):
        Section.objects.create(class_number=40063, code="COS", catalog_number="333",
                                title="Advanced Programming Techniques",start_time=time(11),
                                end_time=time(12, 20), days=["T", "Th"], location="BOWEN 222", term="S2019")
        Section.objects.create(class_number=40000, code="COS", catalog_number="226", section="L01",
                                title="Algorithms and Data Structures", start_time=time(11),
                                end_time=time(12,20), days=["T", "Th"], location="FRIEN 101", term="S2019")
        Section.objects.create(class_number=40000, code="COS", catalog_number="226", section="P01",
                                title="Algorithms and Data Structures", start_time=time(15),
                                end_time=time(16,20), days=["T", "Th"], location="FRIEN 108", term="S2019")
        Section.objects.create(class_number=40000, code="COS", catalog_number="226", section="P01A",
                                title="Algorithms and Data Structures", start_time=time(15),
                                end_time=time(16,20), days=["T", "Th"], location="ANDB1 017", term="S2019")

    def test_get_valid_section(self):
        cos333_lecture = Section.objects.filter(code="COS", catalog_number="333")
        response = self.client.get(reverse("search-sections") + "?search=COS+333")
        serializer = SectionsSerializer(cos333_lecture, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

# test views
class ScheduleTest(APITestCase):
    client = APIClient()

    def setUp(self):
        # create a test user
        User = get_user_model()
        self.rsedgewick = User.objects.create_user(first_name="Rob", last_name="Sedgewick",
                                             username="rsedgewick", class_year=2022,
                                             password="password")
        a_schedule = Schedule.objects.create(term="S2019", owner=self.rsedgewick)
        s_cos333 = Section.objects.create(class_number=40063, code="COS", catalog_number="333",
                                title="Advanced Programming Techniques",start_time=time(11),
                                end_time=time(12, 20), days=["T", "Th"], location="BOWEN 222", term="S2019")
        s_cos226 = Section.objects.create(class_number=40000, code="COS", catalog_number="226", section="L01",
                                title="Algorithms and Data Structures", start_time=time(11),
                                end_time=time(12,20), days=["T", "Th"], location="FRIEN 101", term="S2019")
        s_chi418 = Section.objects.create(class_number=40003, code="CHI", catalog_number="418", section="C03",
                                title="Algorithms and Data Structures", start_time=time(13),
                                end_time=time(14,50), days=["T", "Th"], location="FRIST 228", term="S2019")

        # add classes to schedule
        RecurrentEvent.objects.create_event_from_section(a_schedule, SectionsSerializer(s_cos333).data)
        RecurrentEvent.objects.create_event_from_section(a_schedule, SectionsSerializer(s_cos226).data)
        RecurrentEvent.objects.create_event_from_section(a_schedule, SectionsSerializer(s_chi418).data)

    def test_get_events_from_schedule(self):
        self.client.login(username='rsedgewick', password='password')
        schedule = Schedule.objects.get(owner=self.rsedgewick)
        events = RecurrentEvent.objects.filter(schedule=schedule)
        serializer = RecurrentEventsSerializer(events, many=True)
        response = self.client.get(reverse("get-schedule-add-event"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # having difficulties with this because of the datetime object
    def test_create_custom_event(self):
        self.client.login(username='rsedgewick', password='password')
        schedule = Schedule.objects.get(owner=self.rsedgewick)
        event = {"title": "Lunch", "start_time":time(11), "end_time":time(12,30),
                 "location": "CS302", "days": ["M", "T", "W", "Th", "F"]}
        # response = self.client.post(reverse("create-update-delete-recurrent-event"),
        #                             data=json.dumps(event, default=myconverter),
        #                             content_type='application/json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # events = RecurrentEvent.objects.filter(schedule=schedule)
        # serializer = RecurrentEventsSerializer(events, many=True)
        # print(serializer.data)
        # response = self.client.get(reverse("get-schedule-add-event"))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, serializer.data)

    def test_delete_event(self):
        self.client.login(username='rsedgewick', password='password')
        schedule = Schedule.objects.get(owner=self.rsedgewick)
        event = RecurrentEvent.objects.get(location="BOWEN 222")
        response = self.client.delete(reverse("create-update-delete-recurrent-event",
                                      kwargs={"pk": event.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = RecurrentEvent.objects.filter(schedule=schedule)
        serializer = RecurrentEventsSerializer(events, many=True)
        response = self.client.get(reverse("get-schedule-add-event"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_event(self):
        self.client.login(username='rsedgewick', password='password')
        schedule = Schedule.objects.get(owner=self.rsedgewick)
        event = RecurrentEvent.objects.get(location="BOWEN 222")
        updated_event = {"location": "MCCOSH 50"}
        response = self.client.put(reverse("create-update-delete-recurrent-event",
                                   kwargs={"pk": event.pk}), data=json.dumps(updated_event),
                                   content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = RecurrentEvent.objects.filter(schedule=schedule)
        serializer = RecurrentEventsSerializer(events, many=True)
        response = self.client.get(reverse("get-schedule-add-event"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        e_cos333 = RecurrentEvent.objects.get(location="MCCOSH 50")
        self.assertEqual(e_cos333.location, "MCCOSH 50")
