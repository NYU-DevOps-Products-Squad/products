"""
Models for Product
All of the models are stored in this module
"""
import logging
#import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import app

from sqlalchemy import func
from sqlalchemy.exc import InvalidRequestError, DataError

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()
migrate = Migrate(app, db)

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass


class Product(db.Model):
    """
    Class that represents a <your resource model name>
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, db.Sequence('product_id_seq'), primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    price = db.Column(db.FLOAT(8))
    inventory = db.Column(db.Integer)
    owner = db.Column(db.String(63))
    category =  db.Column(db.String(63))


    def __repr__(self):
        return "<<Product> %r id=[%s] %r %f %d %r %r>" % (self.name, self.id, self.description, self.price, self.inventory, self.owner, self.category)

    def create(self):
        """
        Creates a Product to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Product to the database
        """
        logger.info("Updating %s", self.name)

        if not self.id:
            logger.info("empty ID")
            raise DataValidationError("empty ID")
        db.session.commit()

    def delete(self):
        """ Removes a Product from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        try:
            db.session.commit()
        except InvalidRequestError:
            db.session.rollback()

    def serialize(self):
        """ Serializes a Product into a dictionary """
        return {
            "id": self.id, 
            "name": self.name, 
            "description" : self.description,
            "price": self.price,
            "inventory": self.inventory,
            "owner": self.owner,
            "category": self.category

            }

    def deserialize(self, data):
        """
        Deserializes a Product from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.description = data["description"]
            self.price = data["price"]
            self.inventory = data["inventory"]
            self.owner = data["owner"]
            self.category = data["category"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Product: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Product: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Products in the database """
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Product by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Product by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Products with the given name
        Args:
            name (string): the name of the Products you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
    
    @classmethod
    def find_by_price(cls, low, high):
        """Returns all Products with the given price
        Args:
            price (string): the price of the Products you want to match
        """
        logger.info("Processing price query for %s to %s ...", low, high)
        return cls.query.filter(cls.price >= low, cls.price <= high)

    @classmethod
    def find_by_owner(cls, owner):
        """Returns all Products with the given owner
        Args:
            owner (string): the owner of the Products you want to match
        """
        logger.info("Processing owner query for %s ...", owner)
        return cls.query.filter(cls.owner == owner)