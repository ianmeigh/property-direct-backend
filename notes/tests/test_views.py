from django.contrib.auth import get_user_model
from propertys.models import Property
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Note


class NoteListViewTests(APITestCase):
    """Note List / Create View Tests"""

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

        # Create Property
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

        # Create Note
        self.test_user_note = Note.objects.create(
            owner=self.test_user,
            property=self.property,
            content="Test Note",
        )

    def test_anonymous_users_cannot_see_notes(self):
        """Test an anonymous user cannot see any notes"""
        response = self.client.get("/notes/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_see_notes_they_own(self):
        """Test an authenticated user can get list of notes they own"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.get("/notes/")
        response_obj_count = response.data["count"]
        self.assertEqual(response_obj_count, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_cannot_see_notes_they_do_not_own(self):
        """Test an authenticated user cannot see notes they don't own"""
        self.client.login(
            username="test_seller",
            password=self.shared_password,
        )
        response = self.client.get("/notes/")
        response_obj_count = response.data["count"]
        self.assertEqual(response_obj_count, 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_create_note(self):
        """Test an authenticated user can create a note"""
        initial_count = Note.objects.count()
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.post(
            "/notes/",
            {
                "property": self.property.id,
                "content": "new test note",
            },
        )
        count = Note.objects.count()
        self.assertEqual(count, initial_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class NoteDetailViewTests(APITestCase):
    """Note Retrieve, Update and Deletion Tests"""

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

        # Create Note
        self.test_user_note = Note.objects.create(
            owner=self.test_user,
            property=self.property,
            content="Test Note",
        )

    def test_anonymous_users_cannot_see_individual_notes(self):
        """Test an anonymous user cannot see any notes"""
        response = self.client.get(f"/notes/{self.test_user_note.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_see_individual_notes_they_own(self):
        """Test an authenticated user can get individual notes they own"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.get(f"/notes/{self.test_user_note.id}/")
        self.assertEqual(response.data["id"], self.test_user_note.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_see_individual_notes_they_do_not_own(self):
        """Test an authenticated user cannot get individual notes they do not
        own
        """
        self.client.login(
            username="test_seller", password=self.shared_password
        )
        response = self.client.get(f"/notes/{self.test_user_note.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_edit_notes(self):
        """Test owner of a note can update it"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.put(
            f"/notes/{self.test_user_note.id}/",
            {
                "property": self.property.id,
                "content": "updated test note",
            },
        )
        self.assertEqual(response.data["content"], "updated test note")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_delete_notes(self):
        """Test owner of a note can delete it"""
        initial_count = Note.objects.count()
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.delete(f"/notes/{self.test_user_note.id}/")
        count = Note.objects.count()
        self.assertEqual(count, initial_count - 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
