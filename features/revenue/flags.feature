Feature: Flags Management
  As an RFS user
  I need to manage Flags effectively
  So that I can categorize and identify aircraft events

  Background:
    Given the API is accessible
    And I am authenticated with valid credentials
    And a test revision exists

  @flags_test @create
  Scenario: Create a new operational flag
    Given I have flag data with the following details:
      | Field         | Value                        |
      | order         | 1                            |
      | flag_name     | HR31                         |
      | description   | Operational status indicator |
      | status        | true                         |
      | icon          | C001                         |
    When I create a new flag entry
    Then the flag should be created successfully
    And the response should contain the correct flag values

  @flags_test @create
  Scenario: Create a new commercial flag
    Given I have flag data with the following details:
      | Field         | Value                       |
      | order         | 2                           |
      | flag_name     | CR21                        |
      | description   | Commercial status indicator |
      | status        | true                        |
      | icon          | C002                        |
    When I create a new flag entry
    Then the flag should be created successfully
    And the response should contain the correct flag values

  @flags_test @create
  Scenario: Create a new financial flag
    Given I have flag data with the following details:
      | Field         | Value                      |
      | order         | 3                          |
      | flag_name     | FR05                       |
      | description   | Financial status indicator |
      | status        | true                       |
      | icon          | C003                       |
    When I create a new flag entry
    Then the flag should be created successfully
    And the response should contain the correct flag values

  @flags_test @validation @negative
  Scenario: Attempt to create a flag with duplicate order
    Given I have created a flag with order 1
    When I attempt to create another flag with the same order
    Then the operation should fail with a validation error
    And the error message should mention "duplicate order"

  @flags_test @validation @negative
  Scenario: Attempt to create a flag with duplicate flag name
    Given I have created a flag with name "HR31"
    When I attempt to create another flag with the same name
    Then the operation should fail with a validation error
    And the error message should mention "duplicate flag name"

  @flags_test @validation @negative
  Scenario: Attempt to create a flag with duplicate icon
    Given I have created a flag with icon "C001"
    When I attempt to create another flag with the same icon
    Then the operation should fail with a validation error
    And the error message should mention "duplicate icon"

  @flags_test @validation @negative
  Scenario: Attempt to create a flag with missing required fields
    Given I have flag data with missing required fields
    When I attempt to create a new flag entry
    Then the operation should fail with a validation error
    And the error message should mention "required field"

  @flags_test @search
  Scenario: Search for flags by flag name
    Given I have created a flag with name "HR31"
    When I search for flags with flag name "HR31"
    Then the search results should contain exactly 1 entry
    And the entry should have flag name "HR31"

  @flags_test @search
  Scenario: Search for flags by order
    Given I have created multiple flags with different orders
    When I search for flags with order "2"
    Then the search results should contain flags with order 2

  @flags_test @search @negative
  Scenario: Search with no matching results
    Given I have created multiple flags with different names
    When I search for flags with text "NonExistentFlag"
    Then the flag search results should be empty

  @flags_test @edit
  Scenario: Edit an existing flag
    Given I have created a flag with name "HR31"
    When I update the flag with new values:
      | Field         | Value                 |
      | flag_name     | HR32                  |
      | description   | Updated description   |
    Then the flag should be updated successfully
    And the response should contain the updated flag values

  @flags_test @edit
  Scenario: Change flag status from active to inactive
    Given I have created a flag with active status
    When I update the flag to inactive status
    Then the flag should be updated successfully
    And the response should show the flag as inactive

  @flags_test @sort
  Scenario: Sort flags by order in ascending order
    Given I have created the following flags:
      | Order | Flag Name | Description          |
      | 3     | HR31      | Operational indicator |
      | 1     | CR21      | Commercial indicator  |
      | 2     | FR05      | Financial indicator   |
    When I search for flags with sorting:
      | Field | Direction |
      | order | asc       |
    Then the flag search results should be sorted by "order" in "ascending" order

  @flags_test @sort
  Scenario: Sort flags by flag name in descending order
    Given I have created the following flags:
      | Order | Flag Name | Description          |
      | 1     | CR21      | Commercial indicator  |
      | 2     | FR05      | Financial indicator   |
      | 3     | HR31      | Operational indicator |
    When I search for flags with sorting:
      | Field     | Direction |
      | flag_name | desc      |
    Then the flag search results should be sorted by "flag_name" in "descending" order

  @flags_test @delete
  Scenario: Delete a flag
    Given I have created a flag with name "HR31"
    When I delete the flag
    Then the flag should be deleted successfully
    And the flag should no longer exist in the system

  @flags_test @delete @multiple
  Scenario: Delete multiple flags
    Given I have created the following flags:
      | Order | Flag Name | Description          |
      | 1     | CR21      | Commercial indicator  |
      | 2     | FR05      | Financial indicator   |
      | 3     | HR31      | Operational indicator |
    When I delete multiple flags
    Then all selected flags should be deleted successfully
    And none of the deleted flags should exist in the system

  @flags_test @export
  Scenario: Export flags to Excel
    Given I have created multiple flag entries
    When I export flags to Excel format
    Then the flag exported file should be successfully generated
    And the Excel file should contain all flag entries 