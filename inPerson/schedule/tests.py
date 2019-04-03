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
        Schedule.objects.create(term="S19", owner=user1)

    def test_schedule_to_a_user(self):
        user1 = User.objects.get(username="rsedgewick")
        a_schedule = Schedule.objects.get(owner=user1)
        self.assertEqual(a_schedule.term, "S19")
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
        Schedule.objects.create(term="S19", owner=user1)
        days = ["T", "Th"]
        start_time = time(11)
        end_time = time(12, 20)
        Section.objects.create(class_number=40063, code="COS", catalog_number="333",
                                title="Advanced Programming Techniques",start_time=start_time,
                                end_time=end_time, days=days, location="BOWEN 222")

    def test_convert_section_to_event(self):
        a_class = Section.objects.get(class_number="40063")
        user1 = User.objects.get(username="rsedgewick")
        a_schedule = Schedule.objects.get(owner=user1)
        e = RecurrentEvent.objects.create_event_from_section(a_schedule, SectionsSerializer(a_class).data)
        self.assertEqual(e.schedule.owner.username, "rsedgewick")
        self.assertEqual(e.schedule.term, "S19")

class GetSingleSectionTest(APITestCase):
    """
    Try getting details of a section
    """
    client = APIClient()
    
    def setUp(self):
        Section.objects.create(class_number=40063, code="COS", catalog_number="333",
                                title="Advanced Programming Techniques",start_time=time(11),
                                end_time=time(12, 20), days=["T", "Th"], location="BOWEN 222")
        Section.objects.create(class_number=40000, code="COS", catalog_number="226", section="L01",
                                title="Algorithms and Data Structures", start_time=time(11),
                                end_time=time(12,20), days=["T", "Th"], location="FRIEN 101")
        Section.objects.create(class_number=40000, code="COS", catalog_number="226", section="P01",
                                title="Algorithms and Data Structures", start_time=time(15),
                                end_time=time(16,20), days=["T", "Th"], location="FRIEN 108")
        Section.objects.create(class_number=40000, code="COS", catalog_number="226", section="P01A",
                                title="Algorithms and Data Structures", start_time=time(15),
                                end_time=time(16,20), days=["T", "Th"], location="ANDB1 017")

    def test_get_valid_section(self):
        cos333_lecture = Section.objects.get(code="COS", catalog_number="333")
        # must test reverse url
        response = self.client.get("search-sections", kwargs={"code": "COS"})
        print(response)


    # test views
    class BaseViewTest(APITestCase):
        client = APIClient()

        @staticmethod
        def create_recurrevent_from_class(schedule, class_number="", code="", catalog_number="", title="",
                        start_time="", end_time="", days="", location=""):
            """
            Create a section of a class in the db
            :param class_number:
            :param code:
            :param catalog_number:
            :param title:
            :param start_time:
            :param end_time:
            :param end_time:
            :param days:
            :param: location:
            :return:
            """
            a_section = Section.objects.create(class_number=class_number, code=code, catalog_number=catalog_number,
                                    title=title,start_time=start_time, end_time=end_time, days=days, location=location)
            RecurrentEvent.objects.create_event_from_section(schedule, SectionsSerializer(a_section).data)

        def fetch_all_recurrevents_from_schedule(self, pk=0):
            return self.client.get(
                reverse("search-sections", kwargs={"pk": pk})
            )

        def setUp(self):
            # create a test user
            User = get_user_model()
            User.objects.create_user(first_name="Rob", last_name="Sedgewick", username="rsedgewick", class_year=2022, password="password")
            a_schedule = Schedule.objects.create(term="S19", owner=user1)
            self.create_recurrevent_from_class(a_schedule, 40063, "COS", "333", "Advanced Programming Techniques", time(11),
                                time(12, 20), ["T", "Th"], "BOWEN 222")
            self.create_recurrevent_from_class(a_schedule, 40001, "CHI", "418", "C03", "Advanced Chinese Contemporary Literature and Film", time(13,30), time(14,50),
                                ["T", "Th"], "FRIST 228")

    class GetAllRecurrentEventsFromSchedule(BaseViewTest):
        def test_get_all_events_from_schedule(self):
            """
            This method ensures that we're able to retrieve all events from a user's
            schedule.
            """
            expected = RecurrentEvent.objects.all()
            serialized = RecurrentEventsSerializer(expected)
