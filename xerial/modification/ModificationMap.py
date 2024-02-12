from typing import List, Type


class ModificationMap:
    def __init__(self):
        self.__modification_dict: dict[str, dict[str, List[tuple]]] = {}

    def add(self, table: str, version: str, modification: List[any]) -> None:
        if table not in self.__modification_dict:
            self.__modification_dict[table] = {}
        self.__modification_dict[table][version] = modification

    def get(self, table: str, version: str) -> List[tuple]:
        return self.__modification_dict.get(table, {}).get(version, [])

    def get_by_table(self, table: str) -> dict[str, List[tuple]]:
        return self.__modification_dict.get(table, {})

    def get_all(self) -> dict[str, dict[str, List[tuple]]]:
        return self.__modification_dict
