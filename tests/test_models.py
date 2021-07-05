"""
Test cases for YourResourceModel Model

"""
import logging
import unittest
import os
from service import app
from service.models import Product, DataValidationError, db
from .factories import ProductFactory

######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
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