import os

from xerial.modification_action.test.model.MockDataCollection import MockDataCollection, MockData

mock: MockDataCollection = MockDataCollection(
    name='Customer',
    basePath=os.path.dirname(__file__),
    data=[
        MockData(
            version=3,
            rows=[
                {
                    "id": 1,
                    "name": "Customer 1",
                    "email": "customer01@gmail.com",
                    "phoneNumber": "0812345678",
                },
                {
                    "id": 2,
                    "name": "Customer 2",
                    "email": "customer02@gmail.com",
                    "phoneNumber": "0812345679",
                },
                {
                    "id": 3,
                    "name": "Customer 3",
                    "email": "customer03@gmail.com",
                    "phoneNumber": "0812345680",
                },
                {
                    "id": 4,
                    "name": "Customer 4",
                    "email": "customer04@gmail.com",
                    "phoneNumber": "0812345681",
                },
                {
                    "id": 5,
                    "name": "Customer 5",
                    "email": "customer05@gmail.com",
                    "phoneNumber": "0812345682",
                },
            ]
        ),

        MockData(
            version=4,
            rows=[
                {
                    "id": 1,
                    "name": "Customer 1",
                    "email": "customer01@gmail.com",
                    "phoneNumber": "0812345678",
                    "address": "Bangkok, Thailand",
                },
                {
                    "id": 2,
                    "name": "Customer 2",
                    "email": "customer02@gmail.com",
                    "phoneNumber": "0812345679",
                    "address": "Bangkok, Thailand",
                },
                {
                    "id": 3,
                    "name": "Customer 3",
                    "email": "customer03@gmail.com",
                    "phoneNumber": "0812345680",
                    "address": "Bangkok, Thailand",
                },
                {
                    "id": 4,
                    "name": "Customer 4",
                    "email": "customer04@gmail.com",
                    "phoneNumber": "0812345681",
                    "address": "Bangkok, Thailand",
                },
                {
                    "id": 5,
                    "name": "Customer 5",
                    "email": "customer05@gmail.com",
                    "phoneNumber": "0812345682",
                    "address": "Bangkok, Thailand",
                },
            ]
        ),

        MockData(
            version=5,
            rows=[
                {
                    "id": 1,
                    "name": "Customer 1",
                    "email": "customer01@gmail.com",
                    "phoneNumber": "0812345678",
                    "salary": 18000/1,
                },
                {
                    "id": 2,
                    "name": "Customer 2",
                    "email": "customer02@gmail.com",
                    "phoneNumber": "0812345679",
                    "salary": 20000/1,
                },
                {
                    "id": 3,
                    "name": "Customer 3",
                    "email": "customer03@gmail.com",
                    "phoneNumber": "0812345680",
                    "salary": 25000/1,
                },
                {
                    "id": 4,
                    "name": "Customer 4",
                    "email": "customer04@gmail.com",
                    "phoneNumber": "0812345681",
                    "salary": 30000/1,
                },
                {
                    "id": 5,
                    "name": "Customer 5",
                    "email": "customer05@gmail.com",
                    "phoneNumber": "0812345682",
                    "salary": 35000/1,
                },
            ]
        ),

        MockData(
            version=6,
            rows=[
                {
                    "id": 1,
                    "name": "Customer 1",
                    "email": "customer01@gmail.com",
                    "salary": 18000/1,
                },
                {
                    "id": 2,
                    "name": "Customer 2",
                    "email": "customer02@gmail.com",
                    "salary": 20000/1,
                },
                {
                    "id": 3,
                    "name": "Customer 3",
                    "email": "customer03@gmail.com",
                    "salary": 25000/1,
                },
                {
                    "id": 4,
                    "name": "Customer 4",
                    "email": "customer04@gmail.com",
                    "salary": 30000/1,
                },
                {
                    "id": 5,
                    "name": "Customer 5",
                    "email": "customer05@gmail.com",
                    "salary": 35000/1,
                },
            ]
        ),
    ]
)
