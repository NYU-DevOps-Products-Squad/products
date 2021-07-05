"""
Test cases for YourResourceModel Model
"""
import logging
import unittest
import os
from service import app
from service.models import Product, DataValidationError, db
from .factories import ProductFactory
from unittest.mock import patch
from sqlalchemy.exc import InvalidRequestError
######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

class TestProduct(unittest.TestCase):
    """ Test Cases for YourResourceModel Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()


    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_update_a_product(self):
        """ Update a Product """
        product = Product(name="iPhone 12 Pro Max", description="iPhone 12 Pro Max purple", price=1099, inventory=100, owner='Alice', category="Technology")
        product.create()
        self.assertEqual(product.id, 1)
        # Change it and update it
        product.price = 999.99
        product.description = "iPhone 12 Pro Max Black"
        product.update()
        self.assertEqual(product.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].price, 999.99)
        self.assertEqual(products[0].description, "iPhone 12 Pro Max Black")


    def test_update_a_product_empty_id(self):
        """ Update a Product with empty id """
        product = Product(name="iPhone 12 Pro Max", description="iPhone 12 Pro Max purple", price=1099, inventory=100, owner='Alice', category="Technology")
        product.create()
        self.assertEqual(product.id, 1)
        # Change it and update it
        product.id = None
        self.assertRaises(DataValidationError, product.update)

    def test_delete_a_product(self):
        """Delete a Product"""
        product = Product(name="iPhone 12 Pro Max", description="iPhone 12 Pro Max purple", price=1099, inventory=100, owner='Alice', category="Technology")
        product.create()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_delete_a_product_commit_error(self):
        """ Delete a Product Commit Error"""
        product = Product(name="iPhone 12 Pro Max", description="iPhone 12 Pro Max purple", price=1099, inventory=100, owner='Alice', category="Technology")
        product.create()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        with patch('service.models.db.session.commit') as commit:
            commit.side_effect = InvalidRequestError
            product.delete()
            self.assertEqual(len(Product.all()), 1)

