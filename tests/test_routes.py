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
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
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


    def _create_products(self, count):
        """ Factory method to create pets in bulk """
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            resp = self.app.post(
                "/products", json=test_product.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test pet"
            )
            new_product = resp.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products
    

    def test_get_product_list(self):
        """ Get a list of Products """
        self._create_products(5)
        resp = self.app.get("/products")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)


    def test_create_product(self):
            """ Create a new Product """
            test_product = ProductFactory()
            logging.debug(test_product)
            resp = self.app.post(
                "/products", json=test_product.serialize(), content_type="application/json"
            )
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
            # Make sure location header is set
            location = resp.headers.get("Location", None)
            self.assertIsNotNone(location)
            # Check the data is correct
            new_product = resp.get_json()
            self.assertEqual(new_product["name"], test_product.name, "Names do not match")
            self.assertEqual(
                new_product["category"], test_product.category, "Categories do not match"
            )
            self.assertEqual(
                new_product["description"], test_product.description, "Description does not match"
            )
            self.assertEqual(
                new_product["price"], test_product.price, "Price does not match"
            )
            self.assertEqual(
                new_product["inventory"], test_product.inventory, "Inventory does not match"
            )
            # Check that the location header was correct
            resp = self.app.get(location, content_type="application/json")
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            new_product = resp.get_json()
            self.assertEqual(new_product["name"], test_product.name, "Names do not match")
            self.assertEqual(
                new_product["category"], test_product.category, "Categories do not match"
            )
            self.assertEqual(
                new_product["description"], test_product.description, "Availability does not match"
            )
            self.assertEqual(
                new_product["price"], test_product.price, "Price does not match"
            )
            self.assertEqual(
                new_product["inventory"], test_product.inventory, "Inventory does not match"
            )


    def test_get_product(self):
        """ Get a single Product """
        # get the id of a pet
        test_product = self._create_products(1)[0]
        resp = self.app.get(
            "/products/{}".format(test_product.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_product.name)


