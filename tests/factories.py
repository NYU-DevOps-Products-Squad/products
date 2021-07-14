# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger, FuzzyText
from service.models import Product
import uuid

class ProductFactory(factory.Factory):
    """ Creates fake pets that you don't have to feed """

    class Meta:
        model = Product

    name = FuzzyChoice(choices=["apple", "banana", "tomato", "watermelon"])
    description = FuzzyText(length = 10)
    price = FuzzyInteger(0, 42)
    inventory = FuzzyInteger(0, 42)
    owner = FuzzyText(length = 5)
    category = FuzzyChoice(choices=["fruit","vegetable"])
    id = None


if __name__ == '__main__':
    for _ in range(10):
        product = ProductFactory()
        print(product.serialize())