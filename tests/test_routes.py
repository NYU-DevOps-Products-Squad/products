"""
TestYourResourceModel API Service Test Suite
Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from service.models import db
from service.routes import app, init_db
from .factories import ProductFactory


######################################################################
#  T E S T   C A S E S
######################################################################
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

class TestProductServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"],"Product Demo REST API Service")
    
    @mock.path('service.__init__', side_effect=ValueError())
    def test_init_exception(self):
        import service

    def test_update_product(self):
        """ Update an existing Product """
        # create a product to update
        test_product = ProductFactory()
        test_product_name = test_product.name
        test_product_description = test_product.description
        test_product_price = test_product.price
        resp = self.app.post(
            "/api/products", json=test_product.serialize(), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = resp.get_json()
        new_product["category"] = "Education"
        resp = self.app.put(
            "/api/products/{}".format(new_product["id"]),
            json=new_product,
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["category"], "Education")

        # create an update request with partial information
        part_product = resp.get_json()
        part_product["category"] = ""
        resp = self.app.put(
            "/api/products/{}".format(part_product["id"]),
            json=part_product,
            content_type="application/json")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["category"], "Education")

        part_product = resp.get_json()
        part_product["name"] = ""
        resp = self.app.put(
            "/api/products/{}".format(part_product["id"]),
            json=part_product,
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["name"], test_product_name)

        part_product = resp.get_json()
        part_product["description"] = ""
        resp = self.app.put(
            "/api/products/{}".format(part_product["id"]),
            json=part_product,
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["description"], test_product_description)

        part_product = resp.get_json()
        part_product["price"] = ""
        resp = self.app.put(
            "/api/products/{}".format(part_product["id"]),
            json=part_product,
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["price"], test_product_price)

    def test_update_product_not_found(self):
        """ Update a product that's not found """
        test_product = ProductFactory()
        resp = self.app.put(
            "/api/products/0",
            json=test_product.serialize(),
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product_bad_request(self):
        """ Update a product with bad request body """
        # create a product to update
        test_product = ProductFactory()
        resp = self.app.post(
            "/api/products", json=test_product.serialize(), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # create an update request with bad request body
        new_product = resp.get_json()
        resp = self.app.put(
            "/api/products/a",
            json=new_product,
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        resp = self.app.put(
            "/api/products/3.3",
            json=new_product,
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        test_product = ProductFactory()
        test_product_name = test_product.name
        test_product_description = test_product.description
        test_product_price = test_product.price
        resp = self.app.post(
            "/api/products", json=test_product.serialize(), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = resp.get_json()
        new_product["price"] = "a"
        resp = self.app.put(
            "/api/products/{}".format(new_product["id"]),
            json=new_product,
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        """ Delete a Product """
        test_product = self._create_products(1)[0]
        resp = self.app.delete("/api/products/{}".format(test_product.id))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get("/api/products/{}".format(test_product.id))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
