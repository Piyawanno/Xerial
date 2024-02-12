# Feature: Structure Modification
#   @UserPerspective
#  Scenario Outline: Library can perform the structure modification following user models
#    Given I am at a freeze deployment version of the <Database> database
#    And I have modified the structure of the database to be <To> version
#    When I check out to the <To> deployment version
#    Then I should see the query result of that version
#    Then I will be able to stay on that version
#     Examples:
#       | Database | To |
#       | Library  |  4 |
#       | Library  |  5 |
#       | Library  |  6 |
#       | Library  |  7 |
#       | Shopping |  4 |
#       | Shopping |  5 |
#       | Shopping |  6 |
#       | Shopping |  7 |
