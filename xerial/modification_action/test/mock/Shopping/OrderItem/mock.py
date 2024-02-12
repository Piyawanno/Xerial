import os

from xerial.modification_action.test.model.MockDataCollection import MockDataCollection, MockData

mock: MockDataCollection = MockDataCollection(
    name='OrderItem',
    basePath=os.path.dirname(__file__),
    data=[
        MockData(
            version=2,
            rows=[
                {
                    "id": 1,
                    "date": "2021-01-01 09:05:20",
                    "quantity": 1,
                    "product": 2,
                    "shoppingOrder": 1,
                    "totalPrice": '20/1',
                },
                {
                    "id": 2,
                    "date": "2021-01-02 09:23:50",
                    "quantity": 2,
                    "product": 3,
                    "shoppingOrder": 2,
                    "totalPrice": '100/1',
                },
                {
                    "id": 3,
                    "date": "2021-01-03 09:48:09",
                    "quantity": 1,
                    "product": 1,
                    "shoppingOrder": 3,
                    "totalPrice": '20/1',
                },
                {
                    "id": 4,
                    "date": "2021-01-04 10:29:04",
                    "quantity": 3,
                    "product": 5,
                    "shoppingOrder": 4,
                    "totalPrice": '600/1',
                },
                {
                    "id": 5,
                    "date": "2021-01-05 10:30:45",
                    "quantity": 2,
                    "product": 2,
                    "shoppingOrder": 5,
                    "totalPrice": '40/1',
                },
            ]
        ),

        MockData(
            version=3,
            rows=[
                {
                    "id": 1,
                    "date": "2021-01-01 09:05:20",
                    "quantity": 1,
                    "product": 2,
                    "shoppingOrder": 1,
                },
                {
                    "id": 2,
                    "date": "2021-01-02 09:23:50",
                    "quantity": 2,
                    "product": 3,
                    "shoppingOrder": 2,
                },
                {
                    "id": 3,
                    "date": "2021-01-03 09:48:09",
                    "quantity": 1,
                    "product": 1,
                    "shoppingOrder": 3,
                },
                {
                    "id": 4,
                    "date": "2021-01-04 10:29:04",
                    "quantity": 3,
                    "product": 5,
                    "shoppingOrder": 4,
                },
                {
                    "id": 5,
                    "date": "2021-01-05 10:30:45",
                    "quantity": 2,
                    "product": 2,
                    "shoppingOrder": 5,
                },
            ]
        ),

        MockData(
            version=4,
            rows=[
                {
                    "id": 1,
                    "date": "2021-01-01 09:05:20",
                    "quantity": 1,
                    "product": 2,
                    "shoppingOrder": 1,
                },
                {
                    "id": 2,
                    "date": "2021-01-02 09:23:50",
                    "quantity": 2,
                    "product": 3,
                    "shoppingOrder": 2,
                },
                {
                    "id": 3,
                    "date": "2021-01-03 09:48:09",
                    "quantity": 1,
                    "product": 1,
                    "shoppingOrder": 3,
                },
                {
                    "id": 4,
                    "date": "2021-01-04 10:29:04",
                    "quantity": 3,
                    "product": 5,
                    "shoppingOrder": 4,
                },
                {
                    "id": 5,
                    "date": "2021-01-05 10:30:45",
                    "quantity": 2,
                    "product": 2,
                    "shoppingOrder": 5,
                },
            ]
        ),
    ]
)
