from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from datetime import datetime

from .models import FollowRequest
from friendship.models import Follow, Block
from . serializers import FollowsSerializer, FollowRequestsSerializer, BlocksSerializer


from users.models import User
from django.contrib.auth import get_user_model

class FollowersTest(APITestCase):
    client = APIClient()

    def setUp(self):
        # create users
        User = get_user_model()
        self.rsedgewick = User.objects.create_user(first_name="Rob", last_name="Sedgewick",
                                             username="rsedgewick", class_year=2022,
                                             password="password")
        bwk = User.objects.create_user(first_name="Brian", last_name="Kernighan",
                                       username="bwk", class_year=2021, password="password")
        aturing = User.objects.create_user(first_name="Alan", last_name="Turing",
                                 username="aturing", class_year=2019, password="password")
        al14 = User.objects.create_user(first_name="Ada", last_name="Lovelace",
                                 username="al14", class_year=2020, password="password")
        jdoe = User.objects.create_user(first_name="John", last_name="Doe", username="jdoe",
                                  class_year=2022, password="password")
        kwayne = User.objects.create_user(first_name="Kevin", last_name="Wayne", username="kwayne",
                                  class_year=2019, password="password")

        # make followers
        Follow.objects.add_follower(follower=bwk, followee=self.rsedgewick)
        Follow.objects.add_follower(follower=aturing, followee=self.rsedgewick)
        Follow.objects.add_follower(follower=al14, followee=self.rsedgewick)

        # make follow requests
        FollowRequest.objects.create(from_user=kwayne, to_user=self.rsedgewick,
                                    created=datetime.now())
        FollowRequest.objects.create(from_user=jdoe, to_user=self.rsedgewick,
                                    created=datetime.now())

    def test_get_list_of_followers(self):
        self.client.login(username='rsedgewick', password='password')
        followers = Follow.objects.filter(followee=self.rsedgewick)
        serializer = FollowsSerializer(followers, many=True)
        response = self.client.get(reverse("followers-list"))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_a_follower(self):
        self.client.login(username='rsedgewick', password='password')
        bwk = User.objects.get(username="bwk")
        response = self.client.delete(reverse("remove-follower", kwargs={"pk":bwk.pk}))

        # check that bwk has been removed as a follower
        followers = Follow.objects.filter(followee=self.rsedgewick)
        serializer = FollowsSerializer(followers, many=True)
        response = self.client.get(reverse("followers-list"))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_incoming_follow_requests(self):
        self.client.login(username='rsedgewick', password='password')
        requests = FollowRequest.objects.filter(to_user=self.rsedgewick)
        serializer = FollowRequestsSerializer(requests, many=True)
        response = self.client.get(reverse("accept-list-follow-requests",
                                    kwargs={"pk": self.rsedgewick.pk}))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
