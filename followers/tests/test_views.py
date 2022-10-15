from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Follower


class FollowerListViewTests(APITestCase):
    """Follower List / Create View Tests"""

    def setUp(self):

        # Create Users
        self.shared_password = "testingPa$$w0rd!"

        self.test_seller = get_user_model().objects.create_user(
            username="test_seller",
            password=self.shared_password,
            is_seller=True,
        )

        self.test_seller_for_creation_test = (
            get_user_model().objects.create_user(
                username="test_seller_for_creation_test",
                password=self.shared_password,
                is_seller=True,
            )
        )

        self.test_user = get_user_model().objects.create_user(
            username="test_user",
            password=self.shared_password,
        )

        self.test_user_2 = get_user_model().objects.create_user(
            username="test_user_2",
            password=self.shared_password,
        )

        # Create Follower Record
        self.test_user_follow = Follower.objects.create(
            owner=self.test_user,
            followed=self.test_seller,
        )

    def test_anonymous_users_cannot_see_followers(self):
        """Test an anonymous user cannot see any follower information"""
        response = self.client.get("/followers/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_can_see_follower_records_they_own(self):
        """Test an authenticated user can get list of their follower records"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.get("/followers/")
        response_obj_count = response.data["count"]
        self.assertEqual(response_obj_count, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_cannot_see_follower_records_they_do_not_own(self):
        """Test an authenticated user cannot see follower records they don't
        own
        """
        self.client.login(
            username="test_seller",
            password=self.shared_password,
        )
        response = self.client.get("/followers/")
        response_obj_count = response.data["count"]
        self.assertEqual(response_obj_count, 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_users_can_follow_sellers(self):
        """Test an authenticated user can follower a seller"""
        initial_count = Follower.objects.count()
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.post(
            "/followers/",
            {
                "followed": self.test_seller_for_creation_test.id,
            },
        )
        count = Follower.objects.count()
        self.assertEqual(count, initial_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_users_cannot_follow_themselves(self):
        """Test users cannot follow themselves"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.post(
            "/followers/",
            {
                "followed": self.test_user.id,
            },
        )
        self.assertEqual(response.data["detail"], "can't follow yourself")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_users_cannot_follow_non_seller_users(self):
        """Test users can only follow sellers"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.post(
            "/followers/",
            {
                "followed": self.test_user_2.id,
            },
        )
        self.assertEqual(
            response.data["detail"], "can't follow a user that isn't a seller"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_follower_records_should_not_be_allowed(self):
        """Test a duplicate follower record cannot be created"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.post(
            "/followers/",
            {
                "followed": self.test_seller.id,
            },
        )
        self.assertEqual(response.data["detail"], "possible duplicate")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FollowerDetailViewTests(APITestCase):
    """Follower Retrieve, Update and Deletion Tests"""

    def setUp(self):

        # Create Users
        self.shared_password = "testingPa$$w0rd!"

        self.test_seller = get_user_model().objects.create_user(
            username="test_seller",
            password=self.shared_password,
            is_seller=True,
        )

        self.test_seller_for_creation_test = (
            get_user_model().objects.create_user(
                username="test_seller_for_creation_test",
                password=self.shared_password,
                is_seller=True,
            )
        )

        self.test_user = get_user_model().objects.create_user(
            username="test_user",
            password=self.shared_password,
        )

        self.test_user_2 = get_user_model().objects.create_user(
            username="test_user_2",
            password=self.shared_password,
        )

        # Create Follower Record
        self.test_user_follow = Follower.objects.create(
            owner=self.test_user,
            followed=self.test_seller,
        )

    def test_anonymous_users_cannot_see_individual_followers(self):
        """Test an anonymous user cannot see any followers"""
        response = self.client.get(f"/followers/{self.test_user_follow.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_see_individual_followers_they_own(self):
        """Test an authenticated user can get individual followers they own"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.get(f"/followers/{self.test_user_follow.id}/")
        self.assertEqual(response.data["id"], self.test_user_follow.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_see_individual_followers_they_do_not_own(self):
        """Test an authenticated user cannot get individual followers they do
        not own
        """
        self.client.login(
            username="test_seller", password=self.shared_password
        )
        response = self.client.get(f"/followers/{self.test_user_follow.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_delete_followers(self):
        """Test owner of a follower can delete it"""
        initial_count = Follower.objects.count()
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.delete(
            f"/followers/{self.test_user_follow.id}/"
        )
        count = Follower.objects.count()
        self.assertEqual(count, initial_count - 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
