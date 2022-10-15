from django.contrib.auth import get_user_model
from propertys.models import Property
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Bookmark


class BookmarkListViewTests(APITestCase):
    """Bookmark List / Create View Tests"""

    def setUp(self):

        # Create Users
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

        # Create Properties
        self.property = Property.objects.create(
            owner=self.test_seller,
            street_name="test street name",
            locality="test locality",
            city="test city",
            postcode="test postcode",
            description="test description",
            price=100000,
            property_type="apartment",
            num_bedrooms=1,
            num_bathrooms=1,
        )

        self.property_for_creation_test = Property.objects.create(
            owner=self.test_seller,
            street_name="test street name",
            locality="test locality",
            city="test city",
            postcode="test postcode",
            description="test description",
            price=100000,
            property_type="apartment",
            num_bedrooms=1,
            num_bathrooms=1,
        )

        # Create Bookmark
        self.test_user_bookmark = Bookmark.objects.create(
            owner=self.test_user,
            property=self.property,
        )

    def test_anonymous_users_cannot_see_bookmarks(self):
        """Test an anonymous user cannot see any bookmarks"""
        response = self.client.get("/bookmarks/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_see_bookmarks_they_own(self):
        """Test an authenticated user can get list of bookmarks they own"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.get("/bookmarks/")
        response_obj_count = response.data["count"]
        self.assertEqual(response_obj_count, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_cannot_see_bookmarks_they_do_not_own(self):
        """Test an authenticated user cannot see bookmarks they don't own"""
        self.client.login(
            username="test_seller",
            password=self.shared_password,
        )
        response = self.client.get("/bookmarks/")
        response_obj_count = response.data["count"]
        self.assertEqual(response_obj_count, 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_create_bookmark(self):
        """Test an authenticated user can create a bookmark"""
        initial_count = Bookmark.objects.count()
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.post(
            "/bookmarks/",
            {
                "property": self.property_for_creation_test.id,
            },
        )
        count = Bookmark.objects.count()
        self.assertEqual(count, initial_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_bookmarks_should_not_be_allowed(self):
        """Test a duplicate bookmark cannot be created"""

        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.post(
            "/bookmarks/",
            {
                "property": self.property.id,
            },
        )
        self.assertEqual(response.data["detail"], "possible duplicate")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookmarkDetailViewTests(APITestCase):
    """Bookmark Retrieve, Update and Deletion Tests"""

    def setUp(self):

        # Create users
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

        # Create property
        self.property = Property.objects.create(
            owner=self.test_seller,
            street_name="test street name",
            locality="test locality",
            city="test city",
            postcode="test postcode",
            description="test description",
            price=100000,
            property_type="apartment",
            num_bedrooms=1,
            num_bathrooms=1,
        )

        # Create Bookmark
        self.test_user_bookmark = Bookmark.objects.create(
            owner=self.test_user,
            property=self.property,
        )

    def test_anonymous_users_cannot_see_individual_bookmarks(self):
        """Test an anonymous user cannot see any bookmarks"""
        response = self.client.get(f"/bookmarks/{self.test_user_bookmark.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_see_individual_bookmarks_they_own(self):
        """Test an authenticated user can get individual bookmarks they own"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.get(f"/bookmarks/{self.test_user_bookmark.id}/")
        self.assertEqual(response.data["id"], self.test_user_bookmark.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_see_individual_bookmarks_they_do_not_own(self):
        """Test an authenticated user cannot get individual bookmarks they do
        not own
        """
        self.client.login(
            username="test_seller", password=self.shared_password
        )
        response = self.client.get(f"/bookmarks/{self.test_user_bookmark.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_delete_bookmarks(self):
        """Test owner of a bookmark can delete it"""
        initial_count = Bookmark.objects.count()
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.delete(
            f"/bookmarks/{self.test_user_bookmark.id}/"
        )
        count = Bookmark.objects.count()
        self.assertEqual(count, initial_count - 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
