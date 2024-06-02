import os

from xerial.modact.test.model.MockDataCollection import MockDataCollection, MockData

mock: MockDataCollection = MockDataCollection(
	name='Product',
	basePath=os.path.dirname(__file__),
	data=[
		MockData(
			version=3,
			rows=[
				{
					"id": 1,
					"name": "Product 1",
					"price": 20,
					"quantity": 100,
				},
				{
					"id": 2,
					"name": "Product 2",
					"price": 50,
					"quantity": 50,
				},
				{
					"id": 3,
					"name": "Product 3",
					"price": 80,
					"quantity": 250,
				},
				{
					"id": 4,
					"name": "Product 4",
					"price": 100,
					"quantity": 100,
				},
				{
					"id": 5,
					"name": "Product 5",
					"price": 200,
					"quantity": 500,
				},
			]
		),

		MockData(
			version=4,
			rows=[
				{
					"id": 1,
					"name": "Product 1",
					"price": 20.00,
					"quantity": 100,
					"discountRate": 0.10,
				},
				{
					"id": 2,
					"name": "Product 2",
					"price": 50.00,
					"quantity": 50,
					"discountRate": 0.10,
				},
				{
					"id": 3,
					"name": "Product 3",
					"price": 80.00,
					"quantity": 250,
					"discountRate": 0.10,
				},
				{
					"id": 4,
					"name": "Product 4",
					"price": 100.00,
					"quantity": 100,
					"discountRate": 0.10,
				},
				{
					"id": 5,
					"name": "Product 5",
					"price": 200.00,
					"quantity": 500,
					"discountRate": 0.10,
				},
			]
		),

		MockData(
			version=5,
			rows=[
				{
					"id": 1,
					"name": "Product 1",
					"price": 20,
					"quantity": 100,
					"description": "Product 1 description",
				},
				{
					"id": 2,
					"name": "Product 2",
					"price": 50,
					"quantity": 50,
					"description": "Product 2 description",
				},
				{
					"id": 3,
					"name": "Product 3",
					"price": 80,
					"quantity": 250,
					"description": "Product 3 description",
				},
				{
					"id": 4,
					"name": "Product 4",
					"price": 100,
					"quantity": 100,
					"description": "Product 4 description",
				},
				{
					"id": 5,
					"name": "Product 5",
					"price": 200,
					"quantity": 500,
					"description": "Product 5 description",
				},
			]
		),

		MockData(
			version=6,
			rows=[
				{
					"id": 1,
					"name": "Product 1",
					"price": 20,
					"description": "Product 1 description",
				},
				{
					"id": 2,
					"name": "Product 2",
					"price": 50,
					"description": "Product 2 description",
				},
				{
					"id": 3,
					"name": "Product 3",
					"price": 80,
					"description": "Product 3 description",
				},
				{
					"id": 4,
					"name": "Product 4",
					"price": 100,
					"description": "Product 4 description",
				},
				{
					"id": 5,
					"name": "Product 5",
					"price": 200,
					"description": "Product 5 description",
				},
			]
		),
	]
)
