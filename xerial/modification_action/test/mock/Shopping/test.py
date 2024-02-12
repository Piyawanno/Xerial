import asyncio
from importlib import import_module
from typing import List

from xerial.modification_action.test.model.MockDataCollection import MockDataCollection
from xerial.modification_action.test.model.MockDeployment import MockDeployment
from xerial.modification_action.test.TableModificationTestFixture import TableModificationTestFixture

mock_names = ['Customer', 'ShoppingOrder', 'OrderItem', 'Product']
mocks = {}

for name in mock_names:
    module_path = f"xerial.modification_action.test.mock.Shopping.{name}.mock"
    mock_module = import_module(module_path)
    mocks[name] = mock_module.mock

mockData: List[MockDataCollection] = [
    mocks['ShoppingOrder'],
    mocks['Product'],
    mocks['Customer'],
    mocks['OrderItem'],
]

mockDeployment: List[MockDeployment] = [
    MockDeployment(
        version=1,
        to={'Customer': 0, 'ShoppingOrder': 0, 'OrderItem': 0, 'Product': 0},
        describe='Initial deployment'
    ),
    MockDeployment(
        version=2,
        to={'Customer': 1, 'ShoppingOrder': 1, 'OrderItem': 1, 'Product': 1},
        describe='Customer: Should ADD salary and totalProductBought, OrderItem: Should ADD totalPrice, Product: Should ADD description, ShoppingOrder: Should ADD discount and totalPrice'
    ),
    MockDeployment(
        version=3,
        to={'Customer': 2, 'ShoppingOrder': 2, 'OrderItem': 2, 'Product': 2},
        describe='Customer: Should ADD phoneNumber and DROP totalProductBought, OrderItem: Should CHANGE TYPE of totalPrice to fraction, Product: Should ADD quantity and CHANGE LENGTH of description to 30, ShoppingOrder: Should RENAME discount to discountRate'
    ),
    MockDeployment(
        version=4,
        to={'Customer': 3, 'ShoppingOrder': 3, 'OrderItem': 2, 'Product': 3},
        describe='Customer: Should DROP salary, Product: Should DROP description, ShoppingOrder: Should CHANGE TYPE of totalPrice to float',
        isFreeze=True
    ),
    MockDeployment(
        version=5,
        to={'Customer': 4, 'ShoppingOrder': 4, 'OrderItem': 3, 'Product': 4},
        describe='Customer: Should ADD address, ShoppingOrder: Should DROP totalPrice, Product: Should ADD discountRate and CHANGE TYPE of discountRate to float, OrderItem: Should DROP discountRate'
    ),
    MockDeployment(
        version=6,
        to={'Customer': 5, 'ShoppingOrder': 5, 'OrderItem': 3, 'Product': 5},
        describe='Customer: Should CHECKOUT to v2, Product: Should CHECKOUT to v2, OrderItem: Should CHECKOUT to v2'
    ),
    MockDeployment(
        version=7,
        to={'Customer': 6, 'ShoppingOrder': 6, 'OrderItem': 4, 'Product': 6},
        describe='Customer: Should CHECKOUT to v1 and SKIP reverse of DROP totalProductBought, ShoppingOrder: Should CHECKOUT to v0, Product: Should CHECKOUT to v1, OrderItem: Should CHECKOUT to v1'
    ),
]

if __name__ == '__main__':
    test = TableModificationTestFixture('/etc/xerial/Xerial.json', mockData, mockDeployment, 'Shopping')
    asyncio.run(test.run(5))
    # for deployment in mockDeployment:
    #     if not deployment.version <= 4:
    #         asyncio.run(test.run(deployment.version))
