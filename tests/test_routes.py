"""
TestYourResourceModel API Service Test Suite
Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase, mock
from unittest.mock import patch
from unittest.mock import MagicMock, patch
from service import app, status  # HTTP Status Codes
from service.models import db, Product
from service.routes import app, initialize_logging, init_db
from .factories import ProductFactory
from service.error_handlers import internal_server_error
from sqlalchemy.exc import InvalidRequestError



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
        initialize_logging(logging.CRITICAL)

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    def _create_products(self, count):
        """ Factory method to create products in bulk """
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            # test_product_name = test_product.name
            # test_product_description = test_product.description
            # test_product_price = test_product.price
            resp = self.app.post(
                "/products", json=test_product.serialize(), content_type="application/json")
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
            new_product = resp.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"],"Product Demo REST API Service")
    
    @mock.patch('service.routes.init_db', side_effect=Exception())
    def test_init_exception(self, service_init_mock):
        import service
        import importlib
        with self.assertRaises(SystemExit) as cm:
            importlib.import_module("service")
            self.assertRaises(Exception, importlib.reload, service)
        self.assertEqual(cm.exception.code, 4)
        # self.assertRaises(Exception, importlib.reload, "service")

    def test_get_product_list(self):
        """ Get a list of products """
        self._create_products(5)
        resp = self.app.get("/products")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_product(self):
        """ Get a single product """
        # get the id of a product
        test_product = self._create_products(1)[0]
        resp = self.app.get(
            "/products/{}".format(test_product.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_product.name)
        
        # print the repr of a product
        rep = "%s" % test_product


    def test_update_product(self):
        """ Update an existing Product """
        # create a product to update
        test_product = ProductFactory()
        test_product_name = test_product.name
        test_product_description = test_product.description
        test_product_price = test_product.price
        resp = self.app.post(
            "/products", json=test_product.serialize(), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = resp.get_json()
        new_product["category"] = "Education"
        resp = self.app.put(
            "/products/{}".format(new_product["id"]),
            json=new_product,
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["category"], "Education")


    def test_update_product_not_found(self):
        """ Update a product that's not found """
        test_product = ProductFactory()
        resp = self.app.put(
            "/products/0",
            json=test_product.serialize(),
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_product(self):
        """ Delete a Product """
        test_product = self._create_products(1)[0]
        resp = self.app.delete("/products/{}".format(test_product.id))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get("/products/{}".format(test_product.id), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_product_commit_error(self):
        """ Delete a Product """
        product = Product(name="iPhone X", description="Black iPhone", category="Technology", price=999.99)
        product.create()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        with patch('service.models.db.session.commit') as commit:
            commit.side_effect = InvalidRequestError
            product.delete()
            self.assertEqual(len(Product.all()), 1)


    def test_purchase_a_product(self):
        """Purchase a product"""
        self._create_products(2)
        resp = self.app.put("/products/2/purchase", content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.app.get("/products/2", content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_purchase_not_available(self):
        """Purchase a product that is not available"""
        resp = self.app.put("/products/2/purchase", content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        resp = self.app.get("/products/2", content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_data_validation_error(self):
        '''Data Validation Error '''
        test_product = ProductFactory()
        data = test_product.serialize()
        data.pop('name', None)
        resp = self.app.post(
            "/products", json=data, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Bad Request', resp.data)

    def test_404_not_found_error(self):
        '''Resources Not Found Error '''
        resp = self.app.get("/products/{}")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(b'Not Found', resp.data)

    def test_method_not_allowed_error(self):
        '''Test Method Not Allowed Error '''
        resp = self.app.post("/")
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIn(b'Method not Allowed', resp.data)

    def test_unsupported_media_type_error(self):
        '''Unsupported Media Requests '''
        test_product = ProductFactory()
        data = test_product.serialize()
        resp = self.app.post(
            "/products", json=data, content_type="text/javascript"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertIn(b'Content-Type must be application/json', resp.data)

    def test_internal_server_error(self):
        '''Internal Server Error '''
        resp = internal_server_error("internal serval error")
        self.assertEqual(resp[1], status.HTTP_500_INTERNAL_SERVER_ERROR)
