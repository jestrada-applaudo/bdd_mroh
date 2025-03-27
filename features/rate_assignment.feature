Feature: Rate Assignment API
  As an RFS user
  I need to manage the rates applied to event tariffs based on the fleet characteristics, checks, or customer agreements
  So that I can ensure accurate billing for each event

  Background:
    Given the API is accessible
    And I am authenticated with valid credentials
    And a test revision exists
    And the following reference entities exist:
      | Entity     | ID                                   | Name/Code     |
      | Customer   | 22222222-2222-2222-2222-222222222222 | TEST-CUSTOMER |
      | FleetType  | FF010A6B-9188-4A5D-A1EC-D7EF253AD051 | TEST-FLEET    |
      | CheckType  | 44444444-4444-4444-4444-444444444444 | TEST-CHECK    |

  @rates_test
  Scenario: Assign Rates for Customer at Level 1 (lowest priority)
    # First create the required rate
    Given I have rate data with the following details:
      | Field         | Value                                   |
      | level         | 1                                       |
      | year          | 2023                                    |
      | customerId    | 22222222-2222-2222-2222-222222222222   |
      | airframeRate  | 1000                                    |
      | backshopRate  | 500                                     |
      | comments      | Test Level 1 Rate                       |
    When I create a new rate entry
    Then the rate should be created successfully
    # Now test rate assignment
    When I assign rates with the following parameters:
      | Parameter      | Value                                   |
      | year           | 2023                                    |
      | customerId     | 22222222-2222-2222-2222-222222222222   |
      | checkTypeId    | 44444444-4444-4444-4444-444444444444   |
    Then the rate assignment should return status code 200
    And the response should contain the following rates:
      | Rate Type       | Value  |
      | airframeRate    | 1000   |
      | backshopRate    | 500    |
      | level           | 1      |

  @rates_test
  Scenario: Assign Rates for Customer and Fleet Type at Level 2 (medium priority)
    # First create the required rate
    Given I have rate data with the following details:
      | Field         | Value                                   |
      | level         | 2                                       |
      | year          | 2023                                    |
      | customerId    | 22222222-2222-2222-2222-222222222222   |
      | fleetTypeId   | FF010A6B-9188-4A5D-A1EC-D7EF253AD051   |
      | airframeRate  | 1200                                    |
      | backshopRate  | 600                                     |
      | comments      | Test Level 2 Rate                       |
    When I create a new rate entry
    Then the rate should be created successfully
    # Now test rate assignment
    When I assign rates with the following parameters:
      | Parameter      | Value                                   |
      | year           | 2023                                    |
      | customerId     | 22222222-2222-2222-2222-222222222222   |
      | fleetTypeId    | FF010A6B-9188-4A5D-A1EC-D7EF253AD051   |
    Then the rate assignment should return status code 200
    And the response should contain the following rates:
      | Rate Type       | Value  |
      | airframeRate    | 1200   |
      | backshopRate    | 600    |
      | level           | 2      |

  @rates_test
  Scenario: Assign Rates for Customer and Check Type at Level 3 (highest priority)
    # First create the required rate
    Given I have rate data with the following details:
      | Field         | Value                                   |
      | level         | 3                                       |
      | year          | 2023                                    |
      | customerId    | 22222222-2222-2222-2222-222222222222   |
      | checkTypeId   | 44444444-4444-4444-4444-444444444444   |
      | airframeRate  | 1500                                    |
      | backshopRate  | 800                                     |
      | comments      | Test Level 3 Rate                       |
    When I create a new rate entry
    Then the rate should be created successfully
    # Now test rate assignment
    When I assign rates with the following parameters:
      | Parameter      | Value                                   |
      | year           | 2023                                    |
      | customerId     | 22222222-2222-2222-2222-222222222222   |
      | checkTypeId    | 44444444-4444-4444-4444-444444444444   |
    Then the rate assignment should return status code 200
    And the response should contain the following rates:
      | Rate Type       | Value  |
      | airframeRate    | 1500   |
      | backshopRate    | 800    |
      | level           | 3      |

  @rates_test
  Scenario: No Applicable Rates Found Should Return Default Values of Zero
    When I assign rates with the following parameters:
      | Parameter      | Value                                   |
      | year           | 2026                                    |
      | customerId     | 22222222-2222-2222-2222-222222222222   |
      | checkTypeId    | 44444444-4444-4444-4444-444444444444   |
    Then the rate assignment should return status code 200
    And the response should contain the following rates:
      | Rate Type       | Value  |
      | airframeRate    | 0      |
      | backshopRate    | 0      |
      | engineeringRate | 0      |
      | interiorsRate   | 0      |
      | ndtRate         | 0      |
      | componentsRate  | 0      |
      | paintRate       | 0      |
      
  @rates_test
  Scenario: Specific API Example - Assign Rates with Given Parameters
    # First create the required rate (same as Level 1)
    Given I have rate data with the following details:
      | Field         | Value                                   |
      | level         | 1                                       |
      | year          | 2023                                    |
      | customerId    | 22222222-2222-2222-2222-222222222222   |
      | airframeRate  | 1000                                    |
      | backshopRate  | 500                                     |
      | comments      | Test Example Rate                       |
    When I create a new rate entry
    Then the rate should be created successfully
    # Now test the specific API example
    When I assign rates with the following parameters:
      | Parameter      | Value                                   |
      | year           | 2023                                    |
      | customerId     | 22222222-2222-2222-2222-222222222222   |
      | checkTypeId    | 44444444-4444-4444-4444-444444444444   |
    Then the rate assignment should return status code 200
    And the response should contain the following rates:
      | Rate Type       | Value  |
      | airframeRate    | 1000   |
      | backshopRate    | 500    |
      | level           | 1      |
    And the response should include customer information 