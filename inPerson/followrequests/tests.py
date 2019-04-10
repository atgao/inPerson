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
        response = self.client.get(reverse("list-follow-requests"))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accept_follow_request(self):
        self.client.login(username='rsedgewick', password='password')
        kwayne = User.objects.get(username="kwayne")

        # accept follow request from kwayne
        response = self.client.post(reverse("accept-follow-requests",
                                   kwargs={"pk":kwayne.pk}))
        # only 1 follow request should exist
        requests = FollowRequest.objects.filter(to_user=self.rsedgewick)
        serializer = FollowRequestsSerializer(requests, many=True)
        response = self.client.get(reverse("list-follow-requests"))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # now test that the followers have been updated
        followers = Follow.objects.filter(followee=self.rsedgewick)
        serializer = FollowsSerializer(followers, many=True)
        response = self.client.get(reverse("followers-list"))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reject_follow_request(self):
        self.client.login(username='rsedgewick', password='password')
        jdoe = User.objects.get(username="jdoe")

        # reject follow request from jdoe
        # this request should be deleted
        response = self.client.delete(reverse("send-delete-follow-request",
                                   kwargs={"pk": jdoe.pk}))

        # check follow requests to verify
        requests = FollowRequest.objects.filter(to_user=self.rsedgewick)
        serializer = FollowRequestsSerializer(requests, many=True)
        response = self.client.get(reverse("list-follow-requests"))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_follow_request(self):
        self.client.login(username='rsedgewick', password='password')
        bwk = User.objects.get(username="bwk")
        response = self.client.put(reverse("send-delete-follow-request",
                                   kwargs={"pk": bwk.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request = FollowRequest.objects.get(from_user=self.rsedgewick,
                                               to_user=bwk)
        # print(FollowRequestsSerializer(request).data)

    def test_cancel_follow_request(self):
        self.client.login(username='kwayne', password="password")
        rsedgewick = User.objects.get(username="rsedgewick")
        response = self.client.post(reverse("cancel-follow-request",
                                    kwargs={"pk": rsedgewick.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        self.client.login(username='rsedgewick', password='password')
        requests = FollowRequest.objects.filter(to_user=self.rsedgewick)
        serializer = FollowRequestsSerializer(requests, many=True)
        response = self.client.get(reverse("list-follow-requests"))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class FolloweringsTest(APITestCase):
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
        Follow.objects.add_follower(follower=self.rsedgewick, followee=bwk)
        Follow.objects.add_follower(follower=self.rsedgewick, followee=aturing)
        Follow.objects.add_follower(follower=self.rsedgewick, followee=al14)

    def test_get_list_of_followings(self):
        self.client.login(username='rsedgewick', password='password')
        followings = Follow.objects.filter(follower=self.rsedgewick)
        serializer = FollowsSerializer(followings, many=True)
        response = self.client.get(reverse("following-list"))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollow_user(self):
        self.client.login(username='rsedgewick', password='password')
        bwk = User.objects.get(username="bwk")
        response = self.client.delete(reverse("unfollow", kwargs={"pk": bwk.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        followings = Follow.objects.filter(follower=self.rsedgewick)
        serializer = FollowsSerializer(followings, many=True)
        response = self.client.get(reverse("following-list"))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BlocksTest(APITestCase):
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

        # block users
        Block.objects.add_block(self.rsedgewick, jdoe)
        Block.objects.add_block(self.rsedgewick, al14)

    def test_get_list_of_blocked_users(self):
        self.client.login(username='rsedgewick', password='password')
        b_users = Block.objects.filter(blocker=self.rsedgewick)
        serializer = BlocksSerializer(b_users, many=True)
        response = self.client.get(reverse("blocked-users-list"))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_block_a_user(self):
        self.client.login(username='rsedgewick', password='password')
        kwayne = User.objects.get(username="kwayne")
        response = self.client.post(reverse("block-check-blocks-unblock",
                                    kwargs={"pk": kwayne.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        b_users = Block.objects.filter(blocker=self.rsedgewick)
        serializer = BlocksSerializer(b_users, many=True)
        response = self.client.get(reverse("blocked-users-list"))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unblock_user(self):
        self.client.login(username='rsedgewick', password='password')
        al14 = User.objects.get(username="al14")
        response = self.client.delete(reverse("block-check-blocks-unblock",
                                    kwargs={"pk": al14.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        b_users = Block.objects.filter(blocker=self.rsedgewick)
        serializer = BlocksSerializer(b_users, many=True)
        response = self.client.get(reverse("blocked-users-list"))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
