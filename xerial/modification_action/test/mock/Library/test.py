import asyncio
from importlib import import_module
from typing import List

from xerial.modification_action.test.TableModificationTestFixture import TableModificationTestFixture
from xerial.modification_action.test.model.MockDataCollection import MockDataCollection
from xerial.modification_action.test.model.MockDeployment import MockDeployment

mock_names = ['Book', 'Librarian', 'Library']
mocks = {}

for name in mock_names:
    module_path = f"xerial.modification_action.test.mock.Library.{name}.mock"
    mock_module = import_module(module_path)
    mocks[name] = mock_module.mock

mockData: List[MockDataCollection] = [
    mocks['Book'],
    mocks['Librarian'],
    mocks['Library']
]

mockDeployment: List[MockDeployment] = [
    MockDeployment(
        version=1,
        to={'Book': 0, 'Librarian': 0, 'Library': 0},
        describe=''
    ),
    MockDeployment(
        version=2,
        to={'Book': 1, 'Librarian': 1, 'Library': 1},
        describe=''
    ),
    MockDeployment(
        version=3,
        to={'Book': 2, 'Librarian': 2, 'Library': 2},
        describe=''
    ),
    MockDeployment(
        version=4,
        to={'Book': 3, 'Librarian': 3, 'Library': 2},
        describe='should change length of firstName and lastName to 150',
        isFreeze=True
    ),
    MockDeployment(
        version=5,
        to={'Book': 4, 'Librarian': 3, 'Library': 3},
        describe='should change length of firstName and lastName to 150'
    ),
    MockDeployment(
        version=6,
        to={'Book': 5, 'Librarian': 4, 'Library': 3},
        describe='should change length of firstName and lastName to 150'
    ),
    MockDeployment(
        version=7,
        to={'Book': 6, 'Librarian': 5, 'Library': 4},
        describe='should change length of firstName and lastName to 150'
    ),
]

if __name__ == '__main__':
    test = TableModificationTestFixture('/etc/xerial/Xerial.json', mockData, mockDeployment, 'Library')
    # asyncio.run(test.run(deploymentVersion=5))
    for deployment in mockDeployment:
        if not deployment.version <= 4:
            asyncio.run(test.run(deployment.version))
