import os
from typing import List

from xerial.modact.test.model.MockDataCollection import MockDataCollection, MockData

mock: MockDataCollection = MockDataCollection(
	name='Librarian',
	basePath=os.path.dirname(__file__),
	data=[
		MockData(
			version=3,
			rows=[
				{
					"id": 1,
					"name": "Librarian 1",
					"email": "librarian01@gmail.com",
					"library": 1,
					"phoneNumber": "0801234567",
					"address": "Address 1",
					"DOB": "2000-01-01",
				},
				{
					"id": 2,
					"name": "Librarian 2",
					"email": "librarian02@gmail.com",
					"library": 2,
					"phoneNumber": "0801234568",
					"address": "Address 2",
					"DOB": "2000-01-02",
				},
				{
					"id": 3,
					"name": "Librarian 3",
					"email": "librarian03gmail.com",
					"library": 3,
					"phoneNumber": "0801234569",
					"address": "Address 3",
					"DOB": "2000-01-03",
				},
				{
					"id": 4,
					"name": "Librarian 4",
					"email": "librarian04@gmail.com",
					"library": 4,
					"phoneNumber": "0801234570",
					"address": "Address 4",
					"DOB": "2000-01-04",
				},
				{
					"id": 5,
					"name": "Librarian 5",
					"email": "librarian05@gmail.com",
					"library": 5,
					"phoneNumber": "0801234571",
					"address": "Address 5",
					"DOB": "2000-01-05",
				},
			]
		),

		MockData(
			version=4,
			rows=[
				{
					"id": 1,
					"name": "Librarian 1",
					"email": "librarian01@gmail.com",
					"library": 1,
					"phoneNumber": "0801234567",
					"address": "Address 1",
					"DOB": "2000-01-01",
					"startWorkingTime": "07:00:00",
				},
				{
					"id": 2,
					"name": "Librarian 2",
					"email": "librarian02@gmail.com",
					"library": 2,
					"phoneNumber": "0801234568",
					"address": "Address 2",
					"DOB": "2000-01-02",
					"startWorkingTime": "07:10:00",
				},
				{
					"id": 3,
					"name": "Librarian 3",
					"email": "librarian03gmail.com",
					"library": 3,
					"phoneNumber": "0801234569",
					"address": "Address 3",
					"DOB": "2000-01-03",
					"startWorkingTime": "07:20:00",
				},
				{
					"id": 4,
					"name": "Librarian 4",
					"email": "librarian04@gmail.com",
					"library": 4,
					"phoneNumber": "0801234570",
					"address": "Address 4",
					"DOB": "2000-01-04",
					"startWorkingTime": "08:00:00",
				},
				{
					"id": 5,
					"name": "Librarian 5",
					"email": "librarian05@gmail.com",
					"library": 5,
					"phoneNumber": "0801234571",
					"address": "Address 5",
					"DOB": "2000-01-05",
					"startWorkingTime": "08:10:00",
				},
			]
		),

		MockData(
			version=5,
			rows=[
				{
					"id": 1,
					"name": "Librarian 1",
					"email": "librarian01@gmail.com",
					"library": 1,
					"phoneNumber": "0801234567",
					"address": "Address 1",
				},
				{
					"id": 2,
					"name": "Librarian 2",
					"email": "librarian02@gmail.com",
					"library": 2,
					"phoneNumber": "0801234568",
					"address": "Address 2",
				},
				{
					"id": 3,
					"name": "Librarian 3",
					"email": "librarian03gmail.com",
					"library": 3,
					"phoneNumber": "0801234569",
					"address": "Address 3",
				},
				{
					"id": 4,
					"name": "Librarian 4",
					"email": "librarian04@gmail.com",
					"library": 4,
					"phoneNumber": "0801234570",
					"address": "Address 4",
				},
				{
					"id": 5,
					"name": "Librarian 5",
					"email": "librarian05@gmail.com",
					"library": 5,
					"phoneNumber": "0801234571",
					"address": "Address 5",
				},
			]
		),
	]
)
