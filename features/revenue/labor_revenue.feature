Feature: Labor Revenue Management
  As an RFS user
  I need to manage labor effectively
  So that I can maintain accurate labor data

  Background:
    Given the API is accessible
    And I am authenticated with valid credentials
    And a test revision exists
    And the following reference entities exist:
      | Entity     | ID                                   | Name/Code     |
      | Customer   | 22222222-2222-2222-2222-222222222222 | TEST-CUSTOMER |
      | Aircraft   | 33333333-3333-3333-3333-333333333333 | TEST-REG      |
      | CheckType  | 44444444-4444-4444-4444-444444444444 | TEST-CHECK    |
      | Line       | 55555555-5555-5555-5555-555555555555 | TEST-LINE     |

  @revenue_test @labor @create
  Scenario: Create a basic labor revenue entry with rubrics
    Given I have labor revenue data with the following details:
      | Field                | Value                                 |
      | type                 | LABOR                                |
      | customerId           | 22222222-2222-2222-2222-222222222222 |
      | aircraftId           | 33333333-3333-3333-3333-333333333333 |
      | checkTypeId          | 44444444-4444-4444-4444-444444444444 |
      | lineId               | 55555555-5555-5555-5555-555555555555 |
      | isAssociatedToEvent  | false                                |
      | registrationDate     | today                                |
    And I have the following labor rubrics:
      | Type            | Value   | BillableLaborHours |
      | AIRFRAME_LABOR  | 1000.0  | 10.0               |
      | BACKSHOP_LABOR  | 500.0   | 5.0                |
    When I create a new labor revenue entry
    Then the labor revenue should be created successfully
    And the response should contain both rubrics

  @revenue_test @labor @search
  Scenario: Search for labor revenues
    Given I have created a labor revenue with customer code "TEST-CUSTOMER"
    When I search for labor revenues with text "TEST-CUSTOMER"
    Then the search results should contain exactly 1 entry
    And the entry should have customer code "TEST-CUSTOMER"

  @revenue_test @labor @validation @negative
  Scenario: Validate event association dates
    Given I have labor revenue data with event association
    And I set the date out before date in
    When I attempt to create a labor revenue entry
    Then the operation should fail with a validation error
    And the error message should mention "Date Out cannot be before Date In"

  @revenue_test @labor @export
  Scenario: Export labor revenues to Excel
    Given I have created multiple labor revenue entries
    When I export labor revenues to Excel format
    Then the exported file should be successfully generated
    And the Excel file should contain all revenue entries