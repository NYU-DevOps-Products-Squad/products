"""
Global Configuration for Application
"""
import os
import json

# Get configuration from environment
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://cldzutkk:3pYtMMg3zo0ToM4vnp1XoJXA6lbYxRWz@kashin.db.elephantsql.com:5432/cldzutkk"
)

# override if we are running in Cloud Foundry
if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.environ['VCAP_SERVICES'])
    DATABASE_URI = vcap['user-provided'][0]['credentials']['url']

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

