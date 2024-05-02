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
        describe='should change length of firstName and lastName to 150'
    ),
    MockDeployment(
        version=2,
        to={'Customer': 1, 'ShoppingOrder': 1, 'OrderItem': 1, 'Product': 1},
        describe='should change length of firstName and lastName to 150'
    ),
    MockDeployment(
        version=3,
        to={'Customer': 2, 'ShoppingOrder': 2, 'OrderItem': 2, 'Product': 2},
        describe='should change length of firstName and lastName to 150'
    ),
    MockDeployment(
        version=4,
        to={'Customer': 3, 'ShoppingOrder': 3, 'OrderItem': 2, 'Product': 3},
        describe='should change length of firstName and lastName to 150',
        isFreeze=True
    ),
    MockDeployment(
        version=5,
        to={'Customer': 4, 'ShoppingOrder': 4, 'OrderItem': 3, 'Product': 4},
        describe='should change length of firstName and lastName to 150'
    ),
    MockDeployment(
        version=6,
        to={'Customer': 5, 'ShoppingOrder': 5, 'OrderItem': 3, 'Product': 5},
        describe='should change length of firstName and lastName to 150'
    ),
    MockDeployment(
        version=7,
        to={'Customer': 6, 'ShoppingOrder': 6, 'OrderItem': 4, 'Product': 6},
        describe='should change length of firstName and lastName to 150'
    ),
]

if __name__ == '__main__':
    test = TableModificationTestFixture('/etc/xerial/Xerial.json', mockData, mockDeployment, 'Shopping')
    asyncio.run(test.run(4))
    # for deployment in mockDeployment:
    #     if not deployment.version <= 4:
    #         asyncio.run(test.run(deployment.version))
