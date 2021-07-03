"""
My Service

Describe what your service does here
"""

from models import Product
import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import import Product, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )

######################################################################
# UPDATE AN EXISTING PRODUCT
######################################################################
@app.route("/products/<string:product_id>", methods=["PUT"])
@requires_content_type("application/json")
def update_pets(pet_id):
    """
    Update a Product
    This endpoint will update a Product based the body that is posted
    """
    app.logger.info("Request to update Product with id %s", product_id)
    product = Product.find(product_id)
    if not product:
        app.logger.info("Product with id [%s] was not found.", product_id)
        api.abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(product_id))

    product.deserialize(request.get_json())
    product.update()
    app.logger.info("Product with id [%s] updated.", product.id)
    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<string:product_id>", methods=["DELETE"])
def delete_pets(pet_id):
    """
    Delete a Product
    This endpoint will delete a Product based the id specified in the path
    """
    app.logger.info("Request to delete Product with id %s", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()
    app.logger.info("Product with id [%s] delete", product_id)
    return make_response(jsonify(message = ''), status.HTTP_204_NO_CONTENT)
######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    YourResourceModel.init_db(app)
