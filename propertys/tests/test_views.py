import unittest.mock as mock

from django.contrib.auth import get_user_model
from requests.models import Response
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Property


class PropertyListViewTests(APITestCase):
    """Property List View Tests"""

    def setUp(self):

        # Create Users
        self.shared_password = "testingPa$$w0rd!"

        self.test_seller = get_user_model().objects.create_user(
            username="test_seller",
            password=self.shared_password,
            is_seller=True,
        )

        # Create Property
        Property.objects.create(
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

    def test_anonymous_users_can_list_property(self):
        """Test an anonymous user can get list of properties"""
        response = self.client.get("/property/")
        count = Property.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PropertyCreateViewTests(APITestCase):
    """Property Create View Tests"""

    def setUp(self):

        # Create Users
        self.shared_password = "testingPa$$w0rd!"

        self.test_user = get_user_model().objects.create_user(
            username="test_user",
            password=self.shared_password,
        )

        self.test_seller = get_user_model().objects.create_user(
            username="test_seller",
            password=self.shared_password,
            is_seller=True,
        )

        # Property Object
        self.property_obj = {
            "street_name": "test street name",
            "locality": "test locality",
            "city": "test city",
            "postcode": "w1a 1aa",
            "description": "test description",
            "price": 100000,
            "property_type": "apartment",
            "num_bedrooms": 1,
            "num_bathrooms": 1,
        }

    # CREDIT: Mocking API calls in Python
    # AUTHOR: O'Brian Kimokot
    # URL:    https://auth0.com/blog/mocking-api-calls-in-python/

    # CREDIT: Create a functioning Response object (mocking a response)
    # AUTHOR: jonrsharpe - StackOverflow
    # URL:    https://stackoverflow.com/a/40361593
    @mock.patch("requests.get")
    def test_seller_user_can_create_property(self, mock_get):
        """Test a user (seller) can create a property (mocking postcode API
        response)
        """
        # Mock request to simulate external API call
        the_response = mock.Mock(spec=Response)
        the_response.json.return_value = {
            "status": 200,
            "result": {
                "postcode": "W1A 1AA",
                "longitude": -0.143799,
                "latitude": 51.518561,
            },
        }
        mock_get.return_value = the_response

        initial_count = Property.objects.count()
        self.client.login(
            username="test_seller", password=self.shared_password
        )
        response = self.client.post("/property/create", self.property_obj)
        count = Property.objects.count()
        self.assertEqual(count, initial_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_user_cannot_create_property(self):
        """Test an anonymous user cannot create a property"""
        response = self.client.post("/property/create", self.property_obj)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_seller_user_cannot_create_property(self):
        """Test an anonymous user (non-seller) cannot create a property"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.post("/property/create", self.property_obj)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PropertyDetailViewTests(APITestCase):
    """Property Retrieve, Update and Deletion Tests"""

    def setUp(self):

        # Create Users
        self.shared_password = "testingPa$$w0rd!"

        self.test_user_1 = get_user_model().objects.create_user(
            username="test_user_1",
            password=self.shared_password,
        )

        self.test_seller_1 = get_user_model().objects.create_user(
            username="test_seller_1",
            password=self.shared_password,
            is_seller=True,
        )

        self.test_seller_2 = get_user_model().objects.create_user(
            username="test_seller_2",
            password=self.shared_password,
            is_seller=True,
        )

        # Create Properties, each with a different owner
        self.test_seller_1_property = Property.objects.create(
            owner=self.test_seller_1,
            street_name="test street name 1",
            locality="test locality",
            city="test city",
            postcode="hd59pz",
            description="test description",
            price=100000,
            property_type="apartment",
            num_bedrooms=1,
            num_bathrooms=1,
        )

        self.test_seller_2_property = Property.objects.create(
            owner=self.test_seller_2,
            street_name="test street name 2",
            locality="test locality",
            city="test city",
            postcode="test postcode",
            description="test description",
            price=100000,
            property_type="apartment",
            num_bedrooms=1,
            num_bathrooms=1,
        )

        # Property PUT Object
        self.property_update_obj = {
            "street_name": "test street name, put",
            "locality": "test locality",
            "city": "test city",
            "postcode": "W12 7RU",
            "description": "test description",
            "price": 100000,
            "property_type": "apartment",
            "num_bedrooms": 1,
            "num_bathrooms": 1,
        }

    def test_can_get_property_with_valid_id(self):
        """Test an anonymous user can get property detail"""
        response = self.client.get(
            f"/property/{self.test_seller_1_property.id}"
        )
        self.assertEqual(
            response.data["street_name"],
            self.test_seller_1_property.street_name,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_get_property_using_invalid_id(self):
        """Test an anonymous get request with invalid object id will return a
        404 response
        """
        response = self.client.get("/property/99")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch("requests.get")
    def test_seller_can_update_own_property_with_put(self, mock_get):
        """Test a user (seller) can update a property they own using a PUT
        request (mocking postcode API response which tests postcode details
        change)
        """
        # Mock request to simulate external API call
        the_response = mock.Mock(spec=Response)
        the_response.json.return_value = {
            "status": 200,
            "result": {
                "postcode": "W12 7RU",
                "longitude": -0.223397,
                "latitude": 51.513735,
            },
        }
        mock_get.return_value = the_response

        self.client.login(
            username="test_seller_1", password=self.shared_password
        )
        response = self.client.put(
            f"/property/{self.test_seller_1_property.id}",
            self.property_update_obj,
        )
        property = Property.objects.get(pk=self.test_seller_1_property.id)
        self.assertEqual(property.street_name, "test street name, put")
        self.assertEqual(property.longitude, -0.223397)
        self.assertEqual(property.latitude, 51.513735)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_seller_can_update_own_property_with_patch(self):
        """Test a user (seller) can update a property they own using a PATCH
        request
        """
        self.client.login(
            username="test_seller_1", password=self.shared_password
        )
        response = self.client.patch(
            f"/property/{self.test_seller_1_property.id}",
            {"street_name": "test street name 1, patch"},
        )
        property = Property.objects.get(pk=self.test_seller_1_property.id)
        self.assertEqual(
            property.__str__(),
            f"('test street name 1, patch', '{property.locality}', "
            f"'{property.city}', '{property.postcode}')",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_seller_cannot_update_other_users_property(self):
        """Test a user (seller) cannot update a property they do not own"""
        self.client.login(
            username="test_seller_1", password=self.shared_password
        )
        response = self.client.patch(
            f"/property/{self.test_seller_2_property.id}",
            {"street_name": "test street name 2, updated"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_update_property(self):
        """Test an anonymous user cannot update a property"""
        response = self.client.patch(
            f"/property/{self.test_seller_2_property.id}",
            self.property_update_obj,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_seller_user_cannot_update_property(self):
        """Test an anonymous user (non-seller) cannot update a property"""
        self.client.login(username="test_user", password=self.shared_password)
        response = self.client.patch(
            f"/property/{self.test_seller_2_property.id}",
            self.property_update_obj,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seller_can_delete_own_property(self):
        """Test a user (seller) can delete a property they own"""
        self.client.login(
            username="test_seller_1", password=self.shared_password
        )
        initial_count = Property.objects.count()
        response = self.client.delete(
            f"/property/{self.test_seller_1_property.id}"
        )
        count = Property.objects.count()
        self.assertEqual(count, initial_count - 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_seller_cannot_delete_other_users_property(self):
        """Test a user (seller) cannot delete a property they own don't own"""
        self.client.login(
            username="test_seller_1", password=self.shared_password
        )
        response = self.client.delete(
            f"/property/{self.test_seller_2_property.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cannot_delete_property(self):
        """Test an anonymous user cannot delete a property"""
        response = self.client.delete(
            f"/property/{self.test_seller_1_property.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cannot_delete_property(self):
        """Test a user cannot delete a property"""
        self.client.login(
            username="test_user_1", password=self.shared_password
        )
        response = self.client.delete(
            f"/property/{self.test_seller_1_property.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
