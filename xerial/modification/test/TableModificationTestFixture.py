import json

from xerial.DBSessionBase import DBSessionBase
from xerial.DBSessionPool import DBSessionPool
from xerial.Record import Record


class TableModificationTestFixture:
    def __init__(self, config: str, name: str, raw: str, expected: dict, record: Record):
        """
        The test for a single table modification
        :param name: the name of the table
        :param raw: the path to the raw data, all versions
        :param record: Injected as latest version with a modify method
        """
        self.config = config
        self.name = name
        self.raw = raw
        """
        Data format:
        {version, data (follows the record format)}
        """
        self.expected = expected
        self.record = record

        # Session
        self.pool: DBSessionPool | None = None
        self.session: DBSessionBase | None = None

        # Data
        self.latest = None

    def prepareSession(self) -> None:
        # Load the configuration
        with open(self.config) as fd:
            config = json.load(fd)

        # Create session
        self.pool = DBSessionPool(config)
        self.pool.createConnection()
        self.session = self.pool.getSession()

        # Register the model
        self.session.appendModel(self.record.__class__)
        self.session.createTable()

        # Modify the table
        self.record.modify()

    def closeSession(self) -> None:
        self.session.closeConnection()
        self.pool.close()

    def prepareData(self, destination: str) -> dict:
        return {}

    def prepareLatest(self) -> None:
        latest = self.record.getLatestModification().version.__str__()
        self.latest = self.prepareData(latest)

    def dumpLatest(self) -> None:
        self.session.insertMultiple(list(self.latest.values()))

    def action(self):
        # expect latest data to be modified
        self.session.checkModification(self.record, "idk")

    def assertData(self) -> None:
        assert self.latest == self.expected, \
            f"Expected {self.expected}, got {self.latest}"

    def start(self) -> None:
        self.prepareSession()
        self.prepareLatest()
        self.dumpLatest()
        self.action()
        self.assertData()
        self.closeSession()
