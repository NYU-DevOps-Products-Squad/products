"""
Test cases for Product Model
"""
import logging
import unittest
import os
from service import app
from service.models import Product, DataValidationError, db
from .factories import ProductFactory
from unittest.mock import patch
from sqlalchemy.exc import InvalidRequestError
from werkzeug.exceptions import NotFound

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
#####################################################################
class TestProduct(unittest.TestCase):
    """ Test Cases for Product Model """

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
            
    def test_find_or_404_found(self):
        """Find or return 404 found"""
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()

        product = Product.find_or_404(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, Product.find_or_404, 0)

    def test_find_by_name(self):
        """ Find products by Name """
        Product(name = "test1", description = "test des1", price = 105, inventory = 100, owner = "test person1", category = "A").create()
        Product(name = "test2", description = "test des2", price = 85, inventory = 300, owner = "test person2", category = "A").create()
        products = Product.find_by_name("test2")
        self.assertEqual(products[0].name, "test2")
        self.assertEqual(products[0].description, "test des2")
        self.assertEqual(products[0].price, 85)
        self.assertEqual(products[0].inventory, 300)
        self.assertEqual(products[0].owner, "test person2")
        self.assertEqual(products[0].category, "A")
  
    def test_find_by_price(self):
        """ Find products by Price """
        Product(name = "test1", description = "test des1", price = 105, inventory = 100, owner = "test person1", category = "A").create()
        Product(name = "test2", description = "test des2", price = 85, inventory = 300, owner = "test person2", category = "A").create()
        products = Product.find_by_price(80, 90)
        self.assertEqual(products[0].name, "test2")
        self.assertEqual(products[0].description, "test des2")
        self.assertEqual(products[0].price, 85)
        self.assertEqual(products[0].inventory, 300)
        self.assertEqual(products[0].owner, "test person2")
        self.assertEqual(products[0].category, "A")

    def test_find_by_owner(self):
        """ Find products by Owner """
        Product(name = "test1", description = "test des1", price = 105, inventory = 100, owner = "test person1", category = "A").create()
        Product(name = "test2", description = "test des2", price = 85, inventory = 300, owner = "test person2", category = "A").create()
        products = Product.find_by_owner("test person2")
        self.assertEqual(products[0].name, "test2")
        self.assertEqual(products[0].description, "test des2")
        self.assertEqual(products[0].price, 85)
        self.assertEqual(products[0].inventory, 300)
        self.assertEqual(products[0].owner, "test person2")
        self.assertEqual(products[0].category, "A")

    def test_create_a_product(self):
        """ Test a product and assert that it exists """
        product = Product(name="apple", description = "good", price = 1.5, inventory = 100, owner = "sun123", category="fruit" )
        self.assertTrue(product != None)
        self.assertTrue(product.name,"apple")
        self.assertTrue(product.description,"good")
        self.assertTrue(product.price,1.5)
        self.assertTrue(product.inventory,100)
        self.assertTrue(product.owner,"sun123")
        self.assertTrue(product.category,"fruit")
    

    def test_add_a_product(self):
        """ Create a product and add it to the database """
        products = Product.all()
        self.assertEqual(products, [])
        product = Product(name="apple", description = "good", price = 1.5, inventory = 100, owner = "sun123", category="fruit" )
        self.assertTrue(product != None)
        product.create()
        # Asert that it was assigned an id and shows up in the database
        products = Product.all()
        self.assertEqual(len(products), 1)
    

    def test_serialize_a_product(self):
        """ Test serialization of a Products """
        product = ProductFactory()
        data = product.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], product.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], product.name)
        self.assertIn("category", data)
        self.assertEqual(data["category"], product.category)
        self.assertIn("description", data)
        self.assertEqual(data["description"], product.description)
        self.assertIn("inventory", data)
        self.assertEqual(data["inventory"], product.inventory)
        self.assertIn("owner", data)
        self.assertEqual(data["owner"], product.owner)



    def test_deserialize_a_product(self):
        """ Test deserialization of a Product """
        data = {
            "name": "apple", 
            "description" : "good",
            "price": 1.5,
            "inventory": 100,
            "owner": "sun123",
            "category": "fruit"
        }
        product = Product()
        product.deserialize(data)
        self.assertNotEqual(product, None)
        self.assertEqual(product.name, "apple")
        self.assertEqual(product.category, "fruit")
        self.assertEqual(product.description, "good")
        self.assertEqual(product.price,1.5)
        self.assertEqual(product.inventory,100)
        self.assertEqual(product.owner,"sun123")


    def test_deserialize_missing_data(self):
        """ Test deserialization of a Product with missing data """
        data = {
            "description" : "good",
            "price": 1.5,
            "inventory": 100,
            "owner": "sun123",
            "category": "fruit"}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)
