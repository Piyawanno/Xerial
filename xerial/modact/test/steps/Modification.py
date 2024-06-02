from behave import *

from xerial.modact.test.TableModificationTestFixture import TableModificationTestFixture
from xerial.modact.test.steps.context import mockData, mockDeployment

use_step_matcher("re")


@given("I am at a freeze deployment version of the (?P<database_name>.+) database")
async def step_impl(context, database_name):
	"""
	Prepare the test environment to the specified freeze version of the database.
	:type context: behave.runner.Context
	:type database_name: str
	"""
	context.fixture = TableModificationTestFixture(
		config='/etc/xerial/Xerial.json',
		mocks=mockData[database_name],
		deployments=mockDeployment[database_name],
		environment=database_name
	)
	print(f"Database {database_name} set up at freeze version.")


@step("I have modified the structure of the database to be (?P<to_version>.+) version")
async def step_impl(context, to_version):
	"""
	Modify the database structure to the specified version.
	:type context: behave.runner.Context
	:type to_version: str
	"""
	context.fixture.deploymentVersion = to_version
	deployment = context.fixture.setDeployment(to_version)
	describe = deployment.describe
	to = deployment.to
	context.fixture.initLog(deployment.getLogName())
	context.fixture.describe(to, describe)
	await context.fixture.arrange()
	context.fixture.printModifications()
	print(f"Database structure modified to version {to_version}.")


@when("I check out to the (?P<to_version>.+) deployment version")
async def step_impl(context, to_version):
	"""
	Simulate checkout to the specified version.
	:type context: behave.runner.Context
	:type to_version: str
	"""
	await context.fixture.act(to_version)
	context.fixture.printModifications()
	print(f"Checked out to {to_version} deployment version.")


@then("I should see the query result of that version")
async def step_impl(context):
	"""
	Verify that the query results match the expected version.
	:type context: behave.runner.Context
	"""
	await context.assert_()


@then("I will be able to stay on that version")
async def step_impl(context):
	"""
	:type context: behave.runner.Context
	"""
	await context.tearDown(drop=False)