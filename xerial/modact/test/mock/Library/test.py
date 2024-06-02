import asyncio
from importlib import import_module
from typing import List

from xerial.modact.test.TableModificationTestFixture import TableModificationTestFixture
from xerial.modact.test.model.MockDataCollection import MockDataCollection
from xerial.modact.test.model.MockDeployment import MockDeployment

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
		describe='Initial deployment'
	),
	MockDeployment(
		version=2,
		to={'Book': 1, 'Librarian': 1, 'Library': 1},
		describe='Book: Should RENAME title to bookTitle, Librarian: Should ADD phoneNumber and address, Library: Should RENAME name to librarianName'
	),
	MockDeployment(
		version=3,
		to={'Book': 2, 'Librarian': 2, 'Library': 2},
		describe='Book: Should ADD fee and totalSales, Librarian: Should ADD DateOfBirth, Library: Should ADD createDate'
	),
	MockDeployment(
		version=4,
		to={'Book': 3, 'Librarian': 3, 'Library': 2},
		describe='Book: Should DROP totalSales, CHANGE TYPE of fee to float, CHANGE LENGTH of bookTitle to 20, Librarian: Should RENAME DateOfBirth to DOB',
		isFreeze=True
	),
	MockDeployment(
		version=5,
		to={'Book': 4, 'Librarian': 3, 'Library': 3},
		describe='Book: Should DROP fee, Library: Should ADD telephone'
	),
	MockDeployment(
		version=6,
		to={'Book': 5, 'Librarian': 4, 'Library': 3},
		describe='Book: Should CHECKOUT to v2 and SKIP reverse of CHANGE TYPE of fee to float, Librarian: Should ADD startWorkingTime'
	),
	MockDeployment(
		version=7,
		to={'Book': 6, 'Librarian': 5, 'Library': 4},
		describe='Book: Should CHECKOUT to v0, Librarian: Should CHECKOUT to v1, Library: Should CHECKOUT to v1 and SKIP reverse of ADD telephone'
	),
]

if __name__ == '__main__':
	test = TableModificationTestFixture('/etc/xerial/Xerial.json', mockData, mockDeployment, 'Library')
	# asyncio.run(test.run(deploymentVersion=5))
	for deployment in mockDeployment:
		if not deployment.version <= 4:
			asyncio.run(test.run(deployment.version))
