Feature: Rates Management
  As an RFS user
  I need to manage Rates effectively
  So that I can maintain accurate and up-to-date Rates data

  Background:
    Given the API is accessible
    And I am authenticated with valid credentials
    And a test revision exists
    And the following reference entities exist:
      | Entity     | ID                                   | Name/Code     |
      | Customer   | 22222222-2222-2222-2222-222222222222 | TEST-CUSTOMER |
      | FleetType  | 77777777-7777-7777-7777-777777777777 | TEST-FLEET    |
      | CheckType  | 44444444-4444-4444-4444-444444444444 | TEST-CHECK    |

  @rates_test @create @level1
  Scenario: Create a Level 1 Rate
    Given I have rate data with the following details:
      | Field         | Value                                 |
      | level         | 1                                     |
      | year          | 2023                                  |
      | customerId    | 22222222-2222-2222-2222-222222222222 |
      | airframeRate  | 1000.50                              |
      | backshopRate  | 500.75                               |
      | comments      | Test Level 1 Rate                    |
    When I create a new rate entry
    Then the rate should be created successfully
    And the response should contain the correct rate values

  @rates_test @create @level2
  Scenario: Create a Level 2 Rate with Fleet Type
    Given I have rate data with the following details:
      | Field         | Value                                 |
      | level         | 2                                     |
      | year          | 2023                                  |
      | customerId    | 22222222-2222-2222-2222-222222222222 |
      | fleetTypeId   | 77777777-7777-7777-7777-777777777777 |
      | airframeRate  | 1200.50                              |
      | engineeringRate | 800.25                             |
      | comments      | Test Level 2 Rate                    |
    When I create a new rate entry
    Then the rate should be created successfully
    And the response should contain the correct rate values

  @rates_test @create @level3
  Scenario: Create a Level 3 Rate with Check Type
    Given I have rate data with the following details:
      | Field         | Value                                 |
      | level         | 3                                     |
      | year          | 2023                                  |
      | customerId    | 22222222-2222-2222-2222-222222222222 |
      | checkTypeId   | 44444444-4444-4444-4444-444444444444 |
      | ndtRate       | 600.25                               |
      | componentsRate | 900.75                              |
      | comments      | Test Level 3 Rate                    |
    When I create a new rate entry
    Then the rate should be created successfully
    And the response should contain the correct rate values

  @rates_test @validation @negative
  Scenario: Validate rate creation with duplicate data
    Given I have created a Level 1 rate for year 2023
    When I attempt to create another Level 1 rate with the same customer and year
    Then the operation should fail with a validation error
    And the error message should mention "duplicate"

  @rates_test @validation @negative
  Scenario: Validate rate creation without required fields
    Given I have rate data with missing required fields
    When I attempt to create a new rate entry
    Then the operation should fail with a validation error
    And the error message should mention "required field"

  @rates_test @search
  Scenario: Search for rates by customer
    Given I have created a Level 1 rate with customer code "TEST-CUSTOMER"
    When I search for rates with customer code "TEST-CUSTOMER"
    Then the search results should contain exactly 1 entry
    And the entry should have customer code "TEST-CUSTOMER"

  @rates_test @search
  Scenario: Search for rates by year
    Given I have created multiple rate entries for different years
    When I search for rates with year "2023"
    Then the search results should contain all entries for year 2023

  @rates_test @edit
  Scenario: Edit an existing rate
    Given I have created a Level 1 rate for year 2023
    When I update the rate with new values:
      | Field         | Value      |
      | airframeRate  | 2000.75    |
      | comments      | Updated comments |
    Then the rate should be updated successfully
    And the response should contain the updated values

  @rates_test @delete
  Scenario: Delete a single rate
    Given I have created a Level 1 rate for year 2023
    When I delete the rate
    Then the rate should be deleted successfully
    And the rate should no longer exist in the system

  @rates_test @delete @multiple
  Scenario: Delete multiple rates
    Given I have created the following rates:
      | Level | Year | Customer      |
      | 1     | 2023 | TEST-CUSTOMER |
      | 2     | 2024 | TEST-CUSTOMER |
      | 3     | 2025 | TEST-CUSTOMER |
    When I delete multiple rates
    Then all selected rates should be deleted successfully
    And none of the deleted rates should exist in the system

  @rates_test @export
  Scenario: Export rates to Excel
    Given I have created multiple rate entries
    When I export rates to Excel format
    Then the exported file should be successfully generated
    And the Excel file should contain all rate entries 