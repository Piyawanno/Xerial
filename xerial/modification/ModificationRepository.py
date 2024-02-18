from typing import List

from xerial.DBSessionBase import DBSessionBase
from xerial.Modification import Modification
from xerial.modification.ModificationMap import ModificationMap


class ModificationRepository:
    def __init__(self, session: DBSessionBase):
        self.session = session
        self.mapped_modifications: ModificationMap = ModificationMap()
        self.reverse_modifications: List[tuple] = []

    def get_from_session(self):
        return self.mapping(self.session.getAllModification())

    def mapping(self, modifications: List[Modification]) -> None:
        for modification in modifications:
            self.mapped_modifications.add(
                modification.table,
                modification.version.__str__(),
                modification.column
            )

    def get(self, table: str, version: str = None) -> dict[str, list[tuple]] | list[tuple]:
        if version is None:
            return self.mapped_modifications.get_by_table(table)
        return self.mapped_modifications.get(table, version)

    def sort_by_version(self, modifications: dict[str, list[tuple]], order: str = 'desc') -> List[tuple]:
        versions = list(modifications.keys())
        if order == 'desc':
            versions.sort(reverse=True)
        elif order == 'asc':
            versions.sort()
        return [(version, modifications[version]) for version in versions]

    def generate_reverse(self, table: str, destination: str) -> None:
        modifications = self.get(table)
        reverse = []
