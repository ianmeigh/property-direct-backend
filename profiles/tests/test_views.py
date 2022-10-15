from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Profile


class ProfileListViewTests(APITestCase):
    """Profile List View Tests"""

    def setUp(self):

        # Create Users / Profiles
        self.shared_password = "testingPa$$w0rd!"

        self.test_seller = get_user_model().objects.create_user(
            username="test_seller",
            password=self.shared_password,
            is_seller=True,
        )

        self.test_user = get_user_model().objects.create_user(
            username="test_user",
            password=self.shared_password,
        )

    def test_anonymous_users_can_list_only_seller_profiles(self):
        """Test an anonymous user can get list of seller profiles"""
        response = self.client.get("/profiles/")
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_users_can_list_only_seller_profiles(self):
        """Test an authenticated user can get list of seller profiles"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.get("/profiles/")
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileDetailViewTests(APITestCase):
    """Profile Retrieve and Update Tests"""

    def setUp(self):

        # Create Users / Profiles
        self.shared_password = "testingPa$$w0rd!"

        self.test_seller = get_user_model().objects.create_user(
            username="test_seller",
            password=self.shared_password,
            is_seller=True,
        )

        self.test_user = get_user_model().objects.create_user(
            username="test_user",
            password=self.shared_password,
        )

    def test_anonymous_users_cannot_see_non_seller_profiles(self):
        """Test an anonymous user cannot see any profiles owned by users who
        are not sellers
        """
        response = self.client.get(f"/profiles/{self.test_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_view_their_own_profile(self):
        """Test a user (non-seller) can view their profile"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.get(f"/profiles/{self.test_user.id}/")
        self.assertEqual(response.data["id"], self.test_user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_see_individual_profiles_they_do_not_own(self):
        """Test an authenticated user cannot see individual profiles they do
        not own
        """
        self.client.login(
            username="test_seller", password=self.shared_password
        )
        response = self.client.get(f"/profiles/{self.test_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_edit_profile(self):
        """Test owner of a profile can update it"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.put(
            f"/profiles/{self.test_user.id}/",
            {"email": "test@test.com", "telephone_mobile": "07123456789"},
        )
        self.assertEqual(response.data["email"], "test@test.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_delete_profile_and_user_account(self):
        """Test owner of a profile can delete it and that their user account is
        deleted too
        """
        initial_profile_count = Profile.objects.count()
        initial_user_count = get_user_model().objects.count()
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.delete(f"/profiles/{self.test_user.id}/delete/")
        profile_count = Profile.objects.count()
        user_count = get_user_model().objects.count()
        self.assertEqual(profile_count, initial_profile_count - 1)
        self.assertEqual(user_count, initial_user_count - 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
