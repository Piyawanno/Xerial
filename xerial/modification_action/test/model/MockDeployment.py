class MockDeployment:
    def __init__(self, version: int, to: dict[str, int], describe: str, isFreeze: bool = False) -> None:
        self.version = version
        self.to = to
        self.describe = describe
        self.isFreeze = isFreeze

    def getLogName(self) -> str:
        name = f"deployment{self.version}"
        for key, value in self.to.items():
            name += f"_{key}{value}"
        return f"{name}_log.txt"
