from typing import List


class MockData:
	version: int = 0
	rows: List[dict] = []

	def __init__(self, version: int, rows: List[dict]) -> None:
		self.version = version
		self.rows = rows
