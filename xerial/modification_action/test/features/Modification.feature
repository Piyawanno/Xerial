Feature: Structure Modification

  @Deployment
  Scenario Outline: Library can perform the structure modification following user models
    Given I am a developer and I have a database named <Database> with stable version of deployment
    When I want to modify the structure of the database to be <To> version
    Then I should be able to see my test result without any error

    Examples:
      | Database | To |
      | Library  |  4 |
      | Library  |  5 |
      | Library  |  6 |
      | Library  |  7 |
      | Shopping |  4 |
      | Shopping |  5 |
      | Shopping |  6 |
      | Shopping |  7 |
