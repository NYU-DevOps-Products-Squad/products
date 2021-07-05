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
from factory.fuzzy import FuzzyChoice
from service.models import Product


class ProductFactory(factory.Factory):
    """ Creates fake products that you don't have to feed """

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    description = FuzzyChoice(choices=["des1", "des2", "des3", "des4"])
    price = FuzzyChoice(choices=[10.5, 20, 80, 100, 150, 200])
    inventory = FuzzyChoice(choices=[120, 150, 80, 20, 2, 0])
    owner = FuzzyChoice(choices=["owner1", "owner2", "owner3", "owner4"])
    category = FuzzyChoice(choices=["A", "B", "C", "D"])
