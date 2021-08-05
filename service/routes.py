  
"""
My Service
Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort


# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Product, DataValidationError
from werkzeug.exceptions import NotFound
from flask_restx import Api, Resource, fields, reqparse, inputs
# Import Flask application
from service import app, status  # HTTP Status Codes
# app.config["APPLICATION_ROOT"] = "/api"
from functools import wraps
import uuid


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return app.send_static_file("index.html")



# ######################################################################
# # Configure Swagger before initializing it
# ######################################################################
api = Api(app,
          version='1.0.0',
          title='Product Demo REST API Service',
          description='This is a sample server Product store server.',
          default='products',
          default_label='Product shop operations',
          doc='/apidocs', # default also could use doc='/apidocs/'
          prefix=''
         )


# Define the model so that the docs reflect what can be sent
create_model = api.model('Product', {
    'name': fields.String(required=True,
                          description='The name of the Product'),
    'description': fields.String(required=True,
                          description='The description of the Product'),
    'price': fields.Float(required=False,
                          description='The price of the Product'),
    'inventory': fields.Integer(required=False,
                          description='The inventory of the Product'),
    'owner': fields.String(required=False,
                          description='The owner of the Product'),
    'category': fields.String(required=False,
                              description='The category of Product')
})

product_model = api.inherit(
    'ProductModel',
    create_model,
    {
        'id': fields.Integer(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)


purchase_model = api.model('Purchase', {
    'id': fields.Integer(required=True,
                        description='The id of the Product'),
    'amount': fields.Integer(required=True,
                             description='The amount of the Product')
})


# query string arguments
product_args = reqparse.RequestParser()
product_args.add_argument('name', type=str, required=False, help='List Pets by name')
product_args.add_argument('category', type=str, required=False, help='List Pets by category')
product_args.add_argument('owner', type=str, required=False, help='List Pets by owner')
product_args.add_argument('low', type=str, required=False, help='List Pets by min price')
product_args.add_argument('high', type=str, required=False, help='List Pets by max price')


# ######################################################################
# #  PATH: /products
# ######################################################################
@api.route('/products', strict_slashes=False)
class ProductCollection(Resource):
    ######################################################################
    # LIST PRODUCT
    ######################################################################
    @api.doc('list_products')
    @api.expect(product_args, validate=True)
    @api.marshal_list_with(product_model)
    def get(self):
        """ Returns all of the products """
        app.logger.info("Request for product list")
        products = []
        name = request.args.get('name')
        price_low = request.args.get("low")
        price_high = request.args.get("high")
        owner = request.args.get("owner")
        category = request.args.get("category")
        if name:
            app.logger.info("Find by name: %s", name)
            products = Product.find_by_name(name).all()
        elif price_low and price_high:
            app.logger.info("Find by price from %s to %s", price_low, price_high)
            products = Product.find_by_price(price_low, price_high).all()
        elif owner:
            app.logger.info("Find by owner: %s", owner)
            products = Product.find_by_owner(owner).all()
        elif category:
            app.logger.info("Find by category: %s", category)
            products = Product.find_by_category(category).all()
        else:
            products = Product.all()
        app.logger.info('[%s] Products returned', len(products))
        results = [Product.serialize() for Product in products]
        return results, status.HTTP_200_OK

    ######################################################################
    # CREATE A PRODUCT
    ######################################################################
    @api.doc('create_products')
    @api.expect(create_model)
    @api.response(400, 'The posted data was not valid')
    @api.response(201, 'Product created successfully')
    @api.marshal_with(product_model, code=201)
    def post(self):
        """
        Creates a Product
        This endpoint will create a Product based the data in the body that is posted
        """
        app.logger.info("Request to create a product")
        check_content_type("application/json")
        product = Product()
        app.logger.debug('Payload = %s', api.payload)
        create_model.validate(api.payload) # validate manually
        product.deserialize(api.payload)
        product.create()
        app.logger.info('Product with new id [%s] created!', product.id)
        location_url = api.url_for(ProductResource, product_id=product.id, _external=True)
        return product.serialize(), status.HTTP_201_CREATED, {'Location': location_url}


######################################################################
#  PATH: /products/{id}
######################################################################
@api.route('/products/<int:product_id>')
@api.param('product_id', 'The Product identifier')
class ProductResource(Resource):
    """
    ProductResource class

    Allows the manipulation of a single Pet
    GET /product{id} - Returns a Product with the id
    PUT /product{id} - Update a Product with the id
    DELETE /product{id} -  Deletes a Product with the id
    """
    ######################################################################
    # RETRIEVE A PRODUCT
    ######################################################################
    @api.doc('get_products')
    @api.response(404, 'Product not found')
    @api.marshal_with(product_model)
    def get(self, product_id):
        """
        Retrieve a single Product

        This endpoint will return a Product based on it's id
        """
        app.logger.info("Request for product with id: %s", product_id)
        product = Product.find(product_id)
        if not product:
            api.abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(product_id))
        # product = Product.find_or_404(product_id)

        return product.serialize(), status.HTTP_200_OK

    ######################################################################
    # UPDATE AN EXISTING PRODUCT
    ######################################################################
    @api.doc('update_products')
    @api.response(404, 'Product not found')
    @api.response(400, 'The posted Product data was not valid')
    @api.expect(product_model, validate=True)
    @api.marshal_with(product_model)
    def put(self, product_id):
        """
        Update a Product
        This endpoint will update a Product based the body that is posted
        """
        app.logger.info("Request to update Product with id %s", product_id)
        check_content_type("application/json")
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(product_id))

        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        product.deserialize(data)
        product.id = product_id
        product.update()
        app.logger.info("Product with id [%d] updated.", product.id)
        return product.serialize(), status.HTTP_200_OK

    ######################################################################
    # DELETE A PRODUCT
    ######################################################################
    @api.doc('delete_products')
    @api.response(204, 'Product deleted')
    # @app.route("/products/<int:product_id>", methods=["DELETE"])
    def delete(self, product_id):
        """
        Delete a Product
        This endpoint will delete a Product based the id specified in the path
        """
        app.logger.info("Request to delete Product with id %s", product_id)
        product = Product.find(product_id)
        if product:
            product.delete()
        app.logger.info("Product with id [%s] delete", product_id)
        return '', status.HTTP_204_NO_CONTENT

######################################################################
#  PATH: /products/{id}/purchase
######################################################################
@api.route('/products/<product_id>/purchase')
@api.param('product_id', 'The Product identifier')
# @api.expect(purchase_model)
class PurchaseResource(Resource):
    # #####################################################################
    # PURCHASE A product
    # #####################################################################
    @api.doc('purchase_products')
    @api.response(404, 'Product not found')
    @api.response(409, 'The Product cannot be purchased now')
    @api.expect(purchase_model, validate=True)
    @api.marshal_with(purchase_model)
    def post(self, product_id):
        """Purchase a product"""
        data = api.payload
        amount = data['amount']
        app.logger.info("Request to purchase %d product with id %s", amount, product_id)
        check_content_type("application/json")
        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND, "product with id '{}' was not found.".format(product_id)
            )
        product.inventory -= amount
        product.update()
        # TODO: Call Shopcarts & Inventory Service APIs to execute the purchase
        # result = other_service.purchase(product)
        # if not result.success:
        #     abort(status.HTTP_409_CONFLICT, 'Product with id [{}] cannot be purchased now.'.format(product_id))
        app.logger.info('Peroduct with id [%s] has been purchased!', product.id)
        return product.serialize(), status.HTTP_200_OK

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
# @app.before_first_request
def initialize_logging(log_level=logging.INFO):
    """Initialized the default logging to STDOUT"""
    if not app.debug:
        print("Setting up logging...")
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.propagate = False
        app.logger.info("Logging handler established")

def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Product.init_db(app)

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
