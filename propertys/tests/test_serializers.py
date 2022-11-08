import tempfile
import unittest.mock as mock

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from requests.models import Response
from rest_framework.serializers import ValidationError
from rest_framework.test import APITestCase


class PropertySerializersTests(APITestCase):
    def setUp(self):

        # Create users
        self.shared_password = "testingPa$$w0rd!"

        self.test_seller = get_user_model().objects.create_user(
            username="test_seller",
            password=self.shared_password,
            is_seller=True,
        )

        # CREDIT: Mock image raising error; invalid image or corrupt
        # AUTHOR: marcorichetta - forum.djangoproject.com
        # URL: https://forum.djangoproject.com/t/mock-image-raising-error-inval
        # id-image-or-corrupt/4513/2

        # Create image of invalid proportions
        file = tempfile.TemporaryFile()
        image = Image.new(mode="RGB", size=(4097, 4097))
        image.save(file, "png", optimize=True, quality=50)
        file.seek(0)
        self.test_image = SimpleUploadedFile(
            "image.png",
            file.read(),
        )
        file.close()

        # CREDIT: Adapted from Python Docs
        # URL:    https://docs.python.org/3/library/tempfile.html

        # Create a text file
        fp = tempfile.TemporaryFile()
        fp.write(b"Hello world!")
        fp.seek(0)
        self.test_file = SimpleUploadedFile(
            "file.txt",
            fp.read(),
        )
        fp.close()

        # Property Object With Invalid Image and File
        self.property_obj_with_invalid_image_and_file = {
            "street_name": "test street name",
            "locality": "test locality",
            "city": "test city",
            "postcode": "w1a 1aa",
            "description": "test description",
            "price": 100000,
            "property_type": "apartment",
            "num_bedrooms": 1,
            "num_bathrooms": 1,
            "image_hero": self.test_image,
            "floorplan": self.test_file,
        }

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

    @mock.patch("requests.get")
    def test_postcode_validation_failure_response(self, mock_get):
        """Test Postcode Validation Failure Response Raises Validation Error"""
        # Mock request to simulate external API call
        the_response = mock.Mock(spec=Response)
        the_response.json.return_value = {
            "status": 404,
            "error": "Invalid postcode",
        }
        mock_get.return_value = the_response

        self.client.login(
            username="test_seller", password=self.shared_password
        )
        response = self.client.post("/property/create/", self.property_obj)
        self.assertRaises(ValidationError)
        self.assertEqual(
            "Please enter a valid UK postcode",
            response.data["postcode"][0],
        )

    @mock.patch("requests.get")
    def test_postcode_validation_api_unavailable_response(self, mock_get):
        """Test Postcode Validation Service Unavaliable Response Raises
        Validation Error
        """
        # Mock request to simulate external API call
        the_response = mock.Mock(spec=Response)
        the_response.json.return_value = {
            "status": 404,
            "error": "Resource not found",
        }
        mock_get.return_value = the_response

        self.client.login(
            username="test_seller", password=self.shared_password
        )
        response = self.client.post("/property/create/", self.property_obj)
        self.assertRaises(ValidationError)
        self.assertEqual(
            (
                "Postcode verification service temporarily unavailable, "
                "please report this and try again later."
            ),
            response.data["postcode"][0],
        )

    @mock.patch("requests.get")
    def test_image_validation_failure_response(self, mock_get):
        """Test oversized images and non-image files produce Validation Failure
        Response
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

        self.client.login(
            username="test_seller", password=self.shared_password
        )
        response = self.client.post(
            "/property/create/", self.property_obj_with_invalid_image_and_file
        )
        self.assertRaises(ValidationError)
        self.assertIn(
            "Image width should be less than",
            response.data["image_hero"][0],
        )
        self.assertEqual(
            (
                "Upload a valid image. The file you uploaded was either not "
                "an image or a corrupted image."
            ),
            response.data["floorplan"][0],
        )
