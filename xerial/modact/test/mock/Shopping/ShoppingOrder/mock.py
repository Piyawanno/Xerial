import os

from xerial.modact.test.model.MockDataCollection import MockDataCollection, MockData
from xerial.Record import Record

mock: MockDataCollection = MockDataCollection(
		name='ShoppingOrder',
		basePath=os.path.dirname(__file__),
		data=[
			MockData(
				version=3,
				rows=[
					{
						"id": 1,
						"date": "2021-01-01 09:05:20",
						"customer": 1,
						"discountRate": 0.10,
						"totalPrice": 20.00,
					},
					{
						"id": 2,
						"date": "2021-01-02 09:23:50",
						"customer": 2,
						"discountRate": 0.10,
						"totalPrice": 100.00,
					},
					{
						"id": 3,
						"date": "2021-01-03 09:48:09",
						"customer": 3,
						"discountRate": 0.10,
						"totalPrice": 20.00,
					},
					{
						"id": 4,
						"date": "2021-01-04 10:29:04",
						"customer": 4,
						"discountRate": 0.10,
						"totalPrice": 600.00,
					},
					{
						"id": 5,
						"date": "2021-01-05 10:30:45",
						"customer": 5,
						"discountRate": 0.10,
						"totalPrice": 40.00,
					},
				]
			),

			MockData(
				version=4,
				rows=[
					{
						"id": 1,
						"date": "2021-01-01 09:05:20",
						"customer": 1,
						"totalPrice": 20.00,
					},
					{
						"id": 2,
						"date": "2021-01-02 09:23:50",
						"customer": 2,
						"totalPrice": 100.00,
					},
					{
						"id": 3,
						"date": "2021-01-03 09:48:09",
						"customer": 3,
						"totalPrice": 20.00,
					},
					{
						"id": 4,
						"date": "2021-01-04 10:29:04",
						"customer": 4,
						"totalPrice": 600.00,
					},
					{
						"id": 5,
						"date": "2021-01-05 10:30:45",
						"customer": 5,
						"totalPrice": 40.00,
					},
				]
			),

			MockData(
				version=5,
				rows=[
					{
						"id": 1,
						"date": "2021-01-01 09:05:20",
						"customer": 1,
						"discountRate": 0.10,
						"totalPrice": 20,
					},
					{
						"id": 2,
						"date": "2021-01-02 09:23:50",
						"customer": 2,
						"discountRate": 0.10,
						"totalPrice": 100,
					},
					{
						"id": 3,
						"date": "2021-01-03 09:48:09",
						"customer": 3,
						"discountRate": 0.10,
						"totalPrice": 20,
					},
					{
						"id": 4,
						"date": "2021-01-04 10:29:04",
						"customer": 4,
						"discountRate": 0.10,
						"totalPrice": 600,
					},
					{
						"id": 5,
						"date": "2021-01-05 10:30:45",
						"customer": 5,
						"discountRate": 0.10,
						"totalPrice": 40,
					},
				]
			),

			MockData(
				version=6,
				rows=[
					{
						"id": 1,
						"date": "2021-01-01 09:05:20",
						"customer": 1,
						"discount": 0.10,
						"totalPrice": 20,
					},
					{
						"id": 2,
						"date": "2021-01-02 09:23:50",
						"customer": 2,
						"discount": 0.10,
						"totalPrice": 100,
					},
					{
						"id": 3,
						"date": "2021-01-03 09:48:09",
						"customer": 3,
						"discount": 0.10,
						"totalPrice": 20,
					},
					{
						"id": 4,
						"date": "2021-01-04 10:29:04",
						"customer": 4,
						"discount": 0.10,
						"totalPrice": 600,
					},
					{
						"id": 5,
						"date": "2021-01-05 10:30:45",
						"customer": 5,
						"discount": 0.10,
						"totalPrice": 40,
					},
				]
			),
		]
	)

if __name__ == '__main__':
	m = mock[0]
	instance: Record = m.getModel(4)()
	instance.modify()
	scope = instance.getScopedModification("1")
	analyzed = instance.analyzeModifications(scope)
	for key, value in analyzed.items():
		print(f"version: {key}", [ex.message for ex in value])

	debug = []
	for mod in getattr(instance.__class__, '__modification__'):
		debug.append({
			'version': mod.version.__str__(),
			'action': [action.verbose() for action in mod.column],
			'skipped': [
				{
					'skipper': skipper,
					'actions': [action.verbose() for action in actions]
				}
				for skipper, actions
				in mod.skipped.items()
			]
		})
	print(debug)
