import importlib.util
import sys
from typing import List

from xerial.modification_action.test.model.MockData import MockData


class MockDataCollection:
    name: str = ''
    basePath: str = ''
    data: List[MockData] = []

    def __init__(self, name: str, basePath: str, data: List[MockData]) -> None:
        self.name = name
        self.basePath = basePath
        self.data: dict[int, MockData] = {
            mockData.version: mockData
            for mockData in data
        }

    def get(self, version: int) -> MockData | None:
        return self.data.get(version)

    def freezeVersion(self) -> MockData:
        return self.data.get(sorted(self.data.keys())[0])

    def isValidVersion(self, version: int) -> bool:
        return version in self.data.keys()

    def allVersions(self) -> List[int]:
        return list(self.data.keys())

    def getModel(self, version: int) -> type:
        # Append the directory to sys.path
        originalSysPath = sys.path.copy()
        sys.path.append(self.basePath)

        try:
            # Construct the path to the file
            modelPath = f'{self.basePath}/{version}.py'

            # Construct a valid module name by replacing illegal characters
            moduleName = f'{self.name}_{version}'

            # Load the module from the given file path
            spec = importlib.util.spec_from_file_location(moduleName, modelPath)
            if spec is None:
                raise ImportError(f"Can't find the module '{version}'")
            module = importlib.util.module_from_spec(spec)
            sys.modules[moduleName] = module
            spec.loader.exec_module(module)

            # Retrieve the class from the loaded module
            target = getattr(module, self.name, None)
            if target is None:
                raise AttributeError(f"The class '{self.name}' was not found for '{version}'")

            return target

        finally:
            # Restore the original sys.path
            sys.path = originalSysPath
