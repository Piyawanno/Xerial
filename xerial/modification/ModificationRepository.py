from typing import List

from xerial.DBSessionBase import DBSessionBase
from xerial.Modification import Modification
from xerial.modification.ModificationMap import ModificationMap


class ModificationRepository:
    def __init__(self, session: DBSessionBase):
        self.session = session
        self.mapped_modifications: ModificationMap = ModificationMap()

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
