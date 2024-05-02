import asyncio

from behave import *

from xerial.modification_action.test.TableModificationTestFixture import TableModificationTestFixture
from xerial.modification_action.test.steps.context import mockData, mockDeployment

use_step_matcher("re")


@given("I am a developer and I have a database named (?P<Database>.+) with stable version of deployment")
def step_impl(context, Database):
    """
    :type context: behave.runner.Context
    :type Database: str
    """
    context.fixture = TableModificationTestFixture(
        config='/etc/xerial/Xerial.json',
        mocks=mockData[Database],
        deployments=mockDeployment[Database],
        environment=Database
    )


@when("I want to modify the structure of the database to be (?P<To>.+) version")
def step_impl(context, To):
    """
    :type context: behave.runner.Context
    :type To: str
    """
    context.fixture.to = int(To)


@then("I should be able to see my test result without any error")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    actual: bool = asyncio.run(context.fixture.run(context.fixture.to))
    assert actual is True
