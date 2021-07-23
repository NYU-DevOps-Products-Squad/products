"""
Product Steps
Steps file for Products.feature
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import json
import requests
from behave import given
from compare import expect
        
@given('the following products')
def step_impl(context):
    """ Delete all Products and load new ones """
    headers = {'Content-Type': 'application/json'}
    # list all of the products and delete them one by one
    context.resp = requests.get(context.base_url + '/api/products')
    expect(context.resp.status_code).to_equal(200)
    for product in context.resp.json():
        context.resp = requests.delete(context.base_url + '/api/products/' + str(product["id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)

    # load the database with new products
    create_url = context.base_url + '/api/products'
    for row in context.table:
        data = {
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "inventory": row['inventory'],
            "owner": row['owner'],
            "category": row['category']
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)
