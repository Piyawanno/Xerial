import os

from xerial.modification_action.test.model.MockDataCollection import MockDataCollection, MockData

mock: MockDataCollection = MockDataCollection(
    name='Library',
    basePath=os.path.dirname(__file__),
    data=[
        MockData(
            version=2,
            rows=[
                {
                    "id": 1,
                    "libraryName": "Library 1",
                    "location": "Location 1",
                    "createDate": "2021-01-01"
                },
                {
                    "id": 2,
                    "libraryName": "Library 2",
                    "location": "Location 2",
                    "createDate": "2021-01-02"
                },
                {
                    "id": 3,
                    "libraryName": "Library 3",
                    "location": "Location 3",
                    "createDate": "2021-01-03"
                },
                {
                    "id": 4,
                    "libraryName": "Library 4",
                    "location": "Location 4",
                    "createDate": "2021-01-04"
                },
                {
                    "id": 5,
                    "libraryName": "Library 5",
                    "location": "Location 5",
                    "createDate": "2021-01-05"
                },
            ]
        ),

        MockData(
            version=3,
            rows=[
                {
                    "id": 1,
                    "libraryName": "Library 1",
                    "location": "Location 1",
                    "createDate": "2021-01-01",
                    "telephone": "0201234567",
                },
                {
                    "id": 2,
                    "libraryName": "Library 2",
                    "location": "Location 2",
                    "createDate": "2021-01-02",
                    "telephone": "0201234568",
                },
                {
                    "id": 3,
                    "libraryName": "Library 3",
                    "location": "Location 3",
                    "createDate": "2021-01-03",
                    "telephone": "0201234569",
                },
                {
                    "id": 4,
                    "libraryName": "Library 4",
                    "location": "Location 4",
                    "createDate": "2021-01-04",
                    "telephone": "0201234570",
                },
                {
                    "id": 5,
                    "libraryName": "Library 5",
                    "location": "Location 5",
                    "createDate": "2021-01-05",
                    "telephone": "0201234571",
                },
            ]
        ),

        MockData(
            version=4,
            rows=[
                {
                    "id": 1,
                    "libraryName": "Library 1",
                    "location": "Location 1",
                    "telephone": "0201234567",
                },
                {
                    "id": 2,
                    "libraryName": "Library 2",
                    "location": "Location 2",
                    "telephone": "0201234568",
                },
                {
                    "id": 3,
                    "libraryName": "Library 3",
                    "location": "Location 3",
                    "telephone": "0201234569",
                },
                {
                    "id": 4,
                    "libraryName": "Library 4",
                    "location": "Location 4",
                    "telephone": "0201234570",
                },
                {
                    "id": 5,
                    "libraryName": "Library 5",
                    "location": "Location 5",
                    "telephone": "0201234571",
                },
            ]
        ),
    ]
)
