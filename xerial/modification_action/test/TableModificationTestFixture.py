import json
import os
import traceback
from typing import List

from xerial.AsyncDBSessionBase import AsyncDBSessionBase
from xerial.AsyncDBSessionPool import AsyncDBSessionPool
from xerial.modification_action.test.model.MockDataCollection import MockDataCollection
from xerial.modification_action.test.model.MockDeployment import MockDeployment


class TableModificationTestFixture:
    config: str = ""
    mocks: List[MockDataCollection] = []
    logPath: str = ''
    deploymentVersion: int = 0

    def __init__(
            self,
            config: str,
            mocks: List[MockDataCollection],
            deployments: List[MockDeployment],
            environment: str = ''
    ) -> None:
        self.config = config
        self.mocks = mocks
        self.deployments = deployments
        self.freeze = {}
        self.environment = environment

        # Session
        self.pool: AsyncDBSessionPool | None = None
        self.session: AsyncDBSessionBase | None = None
        self.setFreezeFromMock()

        # Transient
        self.models: dict[str, type] = {}
        self.possibleToNone: dict[str, set] = {}

    async def prepareSession(self) -> None:
        # Load the configuration
        self.log('Preparing session')
        self.log(f"Loading configuration from: {self.config}")
        with open(self.config) as conf:
            config = json.load(conf)

        # Create session
        self.log('Creating session')
        self.pool = AsyncDBSessionPool(config)
        await self.pool.createConnection()
        self.session = await self.pool.getSession()

        # Register first version model
        await self.onModelChange(self.deployments[0].to)

    async def closeSession(self) -> None:
        self.log('Closing session')
        await self.session.closeConnection()
        await self.pool.close()

    async def onModelChange(self, to: dict[str, int]) -> None:
        self.log(f'Destination version change to {to}')
        self.destinationVersion = to
        self.log('On model change')
        for mock in self.mocks:
            model = mock.getModel(to.get(mock.name))
            self.log(f"\tModel: {mock.name} is pointing to version: {to.get(mock.name)}")

            oldMeta = [key[0] for key in getattr(mock.getModel(self.freeze.get(mock.name))(), 'meta', [])]
            newMeta = [key[0] for key in getattr(mock.getModel(to.get(mock.name))(), 'meta', [])]
            for key in newMeta:
                if key not in oldMeta:
                    self.log(f"\t\tPossible to None: {key}")
                    self.possibleToNone[mock.name] = self.possibleToNone.get(mock.name, set())
                    self.possibleToNone[mock.name].add(key)

            # Update to models
            self.models[mock.name] = model

            # Register the model
            self.session.appendModel(model)
            self.session.checkModelLinking()
            await self.session.createTable()
            self.log(f"\tModel: {mock.name} is created in session")

    async def arrange(self) -> None:
        self.log('Arranging')
        await self.prepareSession()
        await self.climb()

        if self.destinationVersion != self.freeze:
            self.log(f"Destination version is not freeze")
            self.log(f"Freeze: {self.freeze}")
            raise ValueError("Destination version is not freeze")
        
        self.log(f"destination version is valid")

        for mock in self.mocks:
            model: type = self.models.get(mock.name)
            self.log(f"\tInserting data for {mock.name}")
            rows = mock.get(self.destinationVersion.get(mock.name)).rows
            self.log(f"\tData to insert: {rows}")
            await self.session.insertMultiple([model().fromDict(row) for row in rows])

    async def act(self, to: dict[str, int]) -> None:
        self.log('Act')
        await self.onModelChange(to)
        self.log(f"Freeze Destination version: {to}")

        for mock in self.mocks:
            self.log(f"\tModifying {mock.name}")
            model: type = self.models.get(mock.name)
            await self.session.checkModelModification(model, str(self.freeze.get(mock.name)))

    async def assert_(self) -> bool:
        self.log('Assert')
        if self.session is None:
            raise ValueError("Session is not initialized.")
        
        failed = False

        for mock in self.mocks:
            self.log(f"\tAsserting {mock.name}")
            destination = mock.get(self.destinationVersion.get(mock.name))
            self.log(f"\tDestination: {destination.version}")
            actual = await self.session.selectRaw(self.models.get(mock.name), '')
            expected = destination.rows
            self.log(f"\t\t(Length) Actual: {len(actual)}, Expected: {len(expected)}")

            if len(actual) != len(expected):
                self.log(f"\t\tAssertion failed for {mock.name}: Length mismatch")
                failed = True
                continue

            for i, (act, exp) in enumerate(zip(actual, expected)):
                if act.keys() != exp.keys():
                    self.log(f"\t\tAssertion failed for {mock.name}, keys mismatch")
                    self.log(f"\t\t\tactual: {act.keys()}")
                    self.log(f"\t\t\texpected: {exp.keys()}")
                    failed = True
                    continue

                mismatched_keys = {key for key in act if act[key] != exp[key]}
                possibleToNone = self.possibleToNone.get(mock.name) or set()
                for key in mismatched_keys:
                    self.log(f"\t\tpossibleToNone: assertion {i} skipped for {key}")
                    if key in possibleToNone and act[key] is None:
                        continue
                    self.log(f"\t\tAssertion failed for {mock.name}, key: {key}")
                    self.log(f"\t\t\tactual: {act[key]}")
                    self.log(f"\t\t\texpected: {exp[key]}")
                    failed = True

                if not mismatched_keys:
                    self.log(f"\t\tAssertion {i} passed")

        if not failed:
            self.log('All assertions passed')

        return not failed

    async def validateVersions(self, to: dict[str, int]) -> None:
        valid: bool = True
        for mock in self.mocks:
            self.log(f'Validating {mock.name} version {to.get(mock.name)}')
            version = to.get(mock.name)
            if not mock.isValidVersion(version):
                self.log(f"\t{mock.name} version {version} is not valid, Try: {mock.allVersions()}")
                valid = False

        if not valid:
            raise ValueError("Test terminated due to invalid version.")

    async def printModifications(self) -> None:
        self.log('Print modifications')
        for mock in self.mocks:
            model = self.models.get(mock.name)
            self.log(f"\tModel: {mock.name} with version: {self.destinationVersion.get(mock.name)}")
            modifications = getattr(model, '__modification__', [])
            if not modifications:
                self.log(f"\t\tNo modifications")
            for modification in modifications:
                self.log(f"\t\tModification: {modification.version}")
                for action in modification.column:
                    self.log(f"\t\t\t{action.__str__()}")
                self.log(f"\t\t\tException: {modification.analyze()}")

    async def tearDown(self, drop: bool = True) -> None:
        self.log('Tear down')
        self.setFreezeFromMock()
        if not drop:
            await self.closeSession()
            return

        self.log('Dropping tables')
        for model in self.models.values():
            drop = self.session.generateDropTable(model)
            self.log(f"\tDropping {model.__name__}: {drop}")
            await self.session.executeWrite(drop)
        await self.closeSession()

    def setFreezeFromMock(self):
        self.freeze = {
            mock.name: mock.freezeVersion().version
            for mock in self.mocks
        }

    async def climb(self) -> None:
        self.log(f"Climbing from version 1 to freeze version")
        currentVersion = 1
        while currentVersion < self.deploymentVersion:
            self.log(f"- Checking deployment index: {currentVersion}")
            deployment = self.deployments[currentVersion]
            self.log(f"{deployment.isFreeze}, {deployment.version}, {deployment.to}")
            await self.onModelChange(deployment.to)
            for mock in self.mocks:
                self.log(f"\tArranging {mock.name}")
                model: type = self.models.get(mock.name)
                await self.session.checkModelModification(model, str(currentVersion - 1))

            if deployment.to == self.freeze:
                self.log(f"Freeze version reached: {deployment.to}")
                break

            currentVersion += 1

    async def setDeployment(self) -> MockDeployment | None:
        target = None
        for deployment in self.deployments:
            if deployment.version == self.deploymentVersion:
                target = deployment
                break

        return target

    async def run(self, deploymentVersion: int, drop: bool = True) -> bool:
        self.deploymentVersion = deploymentVersion
        deployment = await self.setDeployment()
        describe = deployment.describe
        isPassed = False
        try:
            to = deployment.to
            await self.initLog(deployment.getLogName())
            self.describe(to, describe)
            await self.validateVersions(to)
            await self.arrange()
            await self.printModifications()
            await self.act(to)
            await self.printModifications()
            isPassed = await self.assert_()
        except Exception as e:
            self.log(f"Exiting due to error: {e.__str__()}")
            self.log(f"with_traceback: {traceback.format_exc()}")
        finally:
            await self.tearDown(drop)
            print(f"The test for {describe} finished, log at {self.logPath}")
            return isPassed

    async def initLog(self, fileName: str) -> None:
        if self.environment:
            fileName = f"{self.environment}_{fileName}"

        self.logPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log", fileName)
        log_dir = os.path.dirname(self.logPath)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        with open(self.logPath, 'w') as logFile:
            logFile.write("")

    def log(self, message: str) -> None:
        with open(self.logPath, 'a') as logFile:
            logFile.write(f"{message}\n")

    @staticmethod
    def describe(to: dict[str, int], describe: str = '') -> None:
        print(f"Fixture: {describe}")

        print("Models: destination")
        for key, value in to.items():
            print(f"  - {key}: {value}")
