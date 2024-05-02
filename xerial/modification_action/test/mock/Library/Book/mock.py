import os

from xerial.modification_action.test.model.MockDataCollection import MockDataCollection, MockData

mock: MockDataCollection = MockDataCollection(
    name='Book',
    basePath=os.path.dirname(__file__),
    data=[
        MockData(
            version=3,
            rows=[
                {
                    "isbn": "9781234567890",
                    "bookTitle": "Book 1",
                    "author": "Author 1",
                    "publishedYear": "2000",
                    "library": 1,
                    "fee": 20.00,
                },
                {
                    "isbn": "9781234567891",
                    "bookTitle": "Book 2",
                    "author": "Author 2",
                    "publishedYear": "2001",
                    "library": 1,
                    "fee": 25.00,
                },
                {
                    "isbn": "9781234567892",
                    "bookTitle": "Book 3",
                    "author": "Author 3",
                    "publishedYear": "2002",
                    "library": 3,
                    "fee": 30.00,
                },
                {
                    "isbn": "9781234567893",
                    "bookTitle": "Book 4",
                    "author": "Author 4",
                    "publishedYear": "2003",
                    "library": 4,
                    "fee": 35.00,
                },
                {
                    "isbn": "9781234567894",
                    "bookTitle": "Book 5",
                    "author": "Author 5",
                    "publishedYear": "2004",
                    "library": 5,
                    "fee": 40.00,
                },
            ]
        ),

        MockData(
            version=4,
            rows=[
                {
                    "isbn": "9781234567890",
                    "bookTitle": "Book 1",
                    "author": "Author 1",
                    "publishedYear": "2000",
                    "library": 1,
                },
                {
                    "isbn": "9781234567891",
                    "bookTitle": "Book 2",
                    "author": "Author 2",
                    "publishedYear": "2001",
                    "library": 1,
                },
                {
                    "isbn": "9781234567892",
                    "bookTitle": "Book 3",
                    "author": "Author 3",
                    "publishedYear": "2002",
                    "library": 3,
                },
                {
                    "isbn": "9781234567893",
                    "bookTitle": "Book 4",
                    "author": "Author 4",
                    "publishedYear": "2003",
                    "library": 4,
                },
                {
                    "isbn": "9781234567894",
                    "bookTitle": "Book 5",
                    "author": "Author 5",
                    "publishedYear": "2004",
                    "library": 5,
                },
            ]
        ),

        MockData(
            version=5,
            rows=[
                {
                    "isbn": "9781234567890",
                    "bookTitle": "Book 1",
                    "author": "Author 1",
                    "publishedYear": "2000",
                    "library": 1,
                    "fee": 20.00,
                    "totalSales": 150.00,
                },
                {
                    "isbn": "9781234567891",
                    "bookTitle": "Book 2",
                    "author": "Author 2",
                    "publishedYear": "2001",
                    "library": 1,
                    "fee": 25.00,
                    "totalSales": 200.00,
                },
                {
                    "isbn": "9781234567892",
                    "bookTitle": "Book 3",
                    "author": "Author 3",
                    "publishedYear": "2002",
                    "library": 3,
                    "fee": 30.00,
                    "totalSales": 250.00,
                },
                {
                    "isbn": "9781234567893",
                    "bookTitle": "Book 4",
                    "author": "Author 4",
                    "publishedYear": "2003",
                    "library": 4,
                    "fee": 35.00,
                    "totalSales": 300.00,
                },
                {
                    "isbn": "9781234567894",
                    "bookTitle": "Book 5",
                    "author": "Author 5",
                    "publishedYear": "2004",
                    "library": 5,
                    "fee": 40.00,
                    "totalSales": 350.00,
                },
            ]
        ),

        MockData(
            version=6,
            rows=[
                {
                    "isbn": "9781234567890",
                    "title": "Book 1",
                    "author": "Author 1",
                    "publishedYear": "2000",
                    "library": 1,
                },
                {
                    "isbn": "9781234567891",
                    "title": "Book 2",
                    "author": "Author 2",
                    "publishedYear": "2001",
                    "library": 1,
                },
                {
                    "isbn": "9781234567892",
                    "title": "Book 3",
                    "author": "Author 3",
                    "publishedYear": "2002",
                    "library": 3,
                },
                {
                    "isbn": "9781234567893",
                    "title": "Book 4",
                    "author": "Author 4",
                    "publishedYear": "2003",
                    "library": 4,
                },
                {
                    "isbn": "9781234567894",
                    "title": "Book 5",
                    "author": "Author 5",
                    "publishedYear": "2004",
                    "library": 5,
                },
            ]
        ),
    ]
)
