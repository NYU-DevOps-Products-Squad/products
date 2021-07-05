  
"""
My Service
Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Product, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
         jsonify(
            name="Product Demo REST API Service",
            version="1.0",
        ),
        status.HTTP_200_OK,
    )

@app.route("/products", methods=["GET"])
def list_product():
    """ Returns all of the products """
    app.logger.info("Request for product list")
    products = []
    name = request.args.get('name')
    price_low = request.args.get("low")
    price_high = request.args.get("high")
    owner = request.args.get("owner")
    if name:
        products = Product.find_by_name(name).all()
    elif price_low and price_high:
        products = Product.find_by_price(price_low, price_high).all()
    elif owner:
        products = Product.find_by_owner(owner).all()
    else:
        products = Product.all()

    results = [Product.serialize() for Product in products]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE A Product
######################################################################
@app.route("/products/<string:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Retrieve a single Product
    This endpoint will return a Product based on it's id
    """
    app.logger.info("Request for Product with id: %s", product_id)
    product = Product.find(product_id)
    
    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)

######################################################################
# ADD A NEW Product
######################################################################
@app.route("/products", methods=["POST"])
def create_product():
    """
    Creates a Product
    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info("Request to create a product")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    location_url = url_for("get_product", product_id=product.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Product.init_db(app)