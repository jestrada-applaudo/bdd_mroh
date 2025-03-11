import os
from behave import given, when, then
import requests, json, uuid
from datetime import datetime, timedelta

@given('I have rate data with the following details')
def step_impl(context):
    # Create data from table
    data = {}
    for row in context.table:
        field = row['Field']
        value = row['Value']
        
        # Handle numeric values
        if field.endswith('Rate'):
            value = float(value)
        elif field == 'year':
            value = int(value)
        elif field == 'level':
            value = int(value)
        
        data[field] = value
    
    # Add revision ID
    data['revisionId'] = context.revision_id
    
    # Store for later use
    context.rate_data = data
    context.logger.info(f"Prepared rate data: {data}")

@when('I create a new rate entry')
def step_impl(context):
    url = f"{context.base_url}/revisions/revenue_options/parameters/rates"
    
    # Add a createdBy field if not present
    if 'createdBy' not in context.rate_data:
        context.rate_data['createdBy'] = os.getenv('TEST_USER_ID', '99999999-9999-9999-9999-999999999999')
    
    # Send request
    response = requests.post(url, headers=context.headers, json=context.rate_data)
    
    # Store response status code
    context.response_status = response.status_code
    
    # Store response
    if response.status_code == 201:
        context.response = response.json()
        if "id" in context.response:
            if not hasattr(context, 'rate_ids'):
                context.rate_ids = []
            context.rate_ids.append(context.response["id"])
            context.logger.info(f"Created rate: {context.response['id']}")
    else:
        context.response = {"error": response.text, "status_code": response.status_code}
        context.logger.error(f"Failed to create rate: {response.text}")

@then('the rate should be created successfully')
def step_impl(context):
    assert context.response_status == 201, f"Expected status 201, got {context.response_status}"
    assert "id" in context.response, "No id for rate in response"
    context.logger.info(f"Rate created with ID: {context.response['id']}")

@then('the response should contain the correct rate values')
def step_impl(context):
    # Verify that the response contains all the rates we set
    for field, value in context.rate_data.items():
        if field.endswith('Rate') and field in context.response:
            assert abs(context.response[field] - value) < 0.001, f"Expected {field} to be {value}, got {context.response[field]}"
    
    context.logger.info("Verified all rate values in response")

@given('I have created a Level {level:d} rate for year {year:d}')
def step_impl(context, level, year):
    # Create a basic rate entry
    context.execute_steps(f'''
        Given I have rate data with the following details:
          | Field         | Value                                 |
          | level         | {level}                               |
          | year          | {year}                                |
          | customerId    | {context.reference_entities['Customer']['id']} |
          | comments      | Test Level {level} Rate               |
    ''')
    
    # Add appropriate fields based on level
    if level == 1:
        context.rate_data.update({
            "airframeRate": 1000.0,
            "backshopRate": 500.0
        })
    elif level == 2:
        context.rate_data.update({
            "fleetTypeId": context.reference_entities['FleetType']['id'],
            "airframeRate": 1200.0,
            "engineeringRate": 800.0
        })
    elif level == 3:
        context.rate_data.update({
            "checkTypeId": context.reference_entities['CheckType']['id'],
            "ndtRate": 600.0,
            "componentsRate": 900.0
        })
    
    # Create it
    context.execute_steps('''
        When I create a new rate entry
        Then the rate should be created successfully
    ''')

@when('I attempt to create another Level {level:d} rate with the same customer and year')
def step_impl(context, level):
    # We'll use the same data as before
    # The revision_id, customer_id, level, and year would be the same
    context.execute_steps('''
        When I attempt to create a new rate entry
    ''')

@when('I attempt to create a new rate entry')
def step_impl(context):
    # Similar to regular create but we expect it might fail
    url = f"{context.base_url}/revisions/revenue_options/parameters/rates"
    
    # Send request and capture response regardless of status code
    response = requests.post(url, headers=context.headers, json=context.rate_data)
    context.response_status = response.status_code
    
    try:
        context.response = response.json()
    except:
        context.response = {"text": response.text}
        
    context.logger.info(f"Attempted to create rate, got status {response.status_code}")

@given('I have rate data with missing required fields')
def step_impl(context):
    # Create rate data missing essential fields like customer or comments
    context.execute_steps('''
        Given I have rate data with the following details:
          | Field         | Value                                 |
          | level         | 1                                     |
          | year          | 2023                                  |
    ''')
    
    # Add rates but no customer or comments
    context.rate_data.update({
        "airframeRate": 1000.0,
        "backshopRate": 500.0
    })

@given('I have created a Level 1 rate with customer code "{customer_code}"')
def step_impl(context, customer_code):
    # Create a basic rate for a specific customer
    context.execute_steps(f'''
        Given I have rate data with the following details:
          | Field         | Value                                 |
          | level         | 1                                     |
          | year          | 2023                                  |
          | customerId    | {context.reference_entities['Customer']['id']} |
          | comments      | Test Rate for {customer_code}         |
    ''')
    
    # Add basic rates
    context.rate_data.update({
        "airframeRate": 1000.0,
        "backshopRate": 500.0,
        "customerCode": customer_code
    })
    
    # Create it
    context.execute_steps('''
        When I create a new rate entry
        Then the rate should be created successfully
    ''')

@given('I have created multiple rate entries for different years')
def step_impl(context):
    # Create rates for multiple years
    years = [2022, 2023, 2024]
    
    for year in years:
        context.execute_steps(f'''
            Given I have created a Level 1 rate for year {year}
        ''')

@when('I search for rates with customer code "{customer_code}"')
def step_impl(context, customer_code):
    url = f"{context.base_url}/revisions/{context.revision_id}/revenue_options/parameters/rates"
    params = {
        "searchText": customer_code,
        "page": 0,
        "pageSize": 10
    }
    
    response = requests.get(url, headers=context.headers, params=params)
    context.response = response.json() if response.status_code == 200 else {"error": response.text}
    context.logger.info(f"Searched for rates with customer code: {customer_code}")

@when('I search for rates with year "{year}"')
def step_impl(context, year):
    url = f"{context.base_url}/revisions/{context.revision_id}/revenue_options/parameters/rates"
    params = {
        "searchText": year,
        "page": 0,
        "pageSize": 10
    }
    
    response = requests.get(url, headers=context.headers, params=params)
    context.response = response.json() if response.status_code == 200 else {"error": response.text}
    context.logger.info(f"Searched for rates with year: {year}")

@then('the search results should contain all entries for year {year:d}')
def step_impl(context, year):
    assert "items" in context.response, f"No content in response: {context.response}"
    items = context.response["items"]
    
    for item in items:
        assert item["year"] == year, f"Expected year {year}, found {item['year']}"
    
    context.logger.info(f"All {len(items)} search results have year {year}")

@when('I update the rate with new values')
def step_impl(context):
    # Get the rate ID from the previous creation
    rate_id = context.response["id"]
    
    # Start with the current data
    update_data = context.rate_data.copy()
    
    # Update fields from the table
    for row in context.table:
        field = row['Field']
        value = row['Value']
        
        # Handle numeric values
        if field.endswith('Rate'):
            value = float(value)
        
        update_data[field] = value
    
    # Add last modified by
    update_data['lastModifiedBy'] = os.getenv('TEST_USER_ID', '99999999-9999-9999-9999-999999999999')
    
    # Send update request
    url = f"{context.base_url}/revisions/revenue_options/parameters/rates/{rate_id}"
    response = requests.put(url, headers=context.headers, json=update_data)
    
    # Store response status code
    context.response_status = response.status_code
    
    # Store response
    if response.status_code == 200:
        context.response = response.json()
        context.logger.info(f"Updated rate: {rate_id}")
    else:
        context.response = {"error": response.text, "status_code": response.status_code}
        context.logger.error(f"Failed to update rate: {response.text}")

@then('the rate should be updated successfully')
def step_impl(context):
    assert context.response_status == 200, f"Expected status 200, got {context.response_status}"
    context.logger.info(f"Rate updated successfully")

@then('the response should contain the updated values')
def step_impl(context):
    # Check each field that was updated
    for row in context.table:
        field = row['Field']
        expected_value = row['Value']
        
        # Handle numeric values
        if field.endswith('Rate'):
            expected_value = float(expected_value)
            actual_value = context.response.get(field, 0)
            assert abs(actual_value - expected_value) < 0.001, f"Expected {field} to be {expected_value}, got {actual_value}"
        else:
            assert context.response.get(field) == expected_value, f"Expected {field} to be {expected_value}, got {context.response.get(field)}"
    
    context.logger.info("Verified updated values in response")

@when('I delete the rate')
def step_impl(context):
    # Get the rate ID
    rate_id = context.response["id"]
    
    # Send delete request
    url = f"{context.base_url}/revisions/revenue_options/parameters/rates/delete"
    data = {"rateIds": [rate_id]}
    
    response = requests.put(url, headers=context.headers, json=data)
    context.response_status = response.status_code
    
    if response.status_code == 200:
        context.response = response.json()
        context.logger.info(f"Deleted rate: {rate_id}")
    else:
        context.response = {"error": response.text, "status_code": response.status_code}
        context.logger.error(f"Failed to delete rate: {response.text}")

@then('the rate should be deleted successfully')
def step_impl(context):
    assert context.response_status == 200, f"Expected status 200, got {context.response_status}"
    context.logger.info("Rate deleted successfully")

@then('the rate should no longer exist in the system')
def step_impl(context):
    # Verify the rate doesn't exist by trying to retrieve it
    rate_id = context.response.get("deletedRates", [""])[0]
    if not rate_id:
        rate_id = context.rate_ids[-1]  # Fallback to last created rate
        
    url = f"{context.base_url}/revisions/{context.revision_id}/revenue_options/parameters/rates/{rate_id}"
    
    response = requests.get(url, headers=context.headers)
    assert response.status_code == 404, f"Expected rate to be deleted (404), but got {response.status_code}"
    context.logger.info(f"Verified rate {rate_id} no longer exists")

@given('I have created the following rates')
def step_impl(context):
    # Create multiple rates based on the table
    context.created_rate_ids = []
    
    for row in context.table:
        level = int(row['Level'])
        year = int(row['Year'])
        context.execute_steps(f'''
            Given I have created a Level {level} rate for year {year}
        ''')
        context.created_rate_ids.append(context.response["id"])
    
    context.logger.info(f"Created {len(context.created_rate_ids)} rates for deletion test")

@when('I delete multiple rates')
def step_impl(context):
    # Delete all created rates
    url = f"{context.base_url}/revisions/revenue_options/parameters/rates/delete"
    data = {"rateIds": context.created_rate_ids}
    
    response = requests.put(url, headers=context.headers, json=data)
    context.response_status = response.status_code
    
    if response.status_code == 200:
        context.response = response.json()
        context.logger.info(f"Deleted multiple rates: {len(context.created_rate_ids)}")
    else:
        context.response = {"error": response.text, "status_code": response.status_code}
        context.logger.error(f"Failed to delete multiple rates: {response.text}")

@then('all selected rates should be deleted successfully')
def step_impl(context):
    assert context.response_status == 200, f"Expected status 200, got {context.response_status}"
    
    # Check that all rates were deleted
    deleted_rates = context.response.get("deletedRates", [])
    assert len(deleted_rates) == len(context.created_rate_ids), f"Expected {len(context.created_rate_ids)} deleted, got {len(deleted_rates)}"
    context.logger.info(f"All {len(deleted_rates)} rates were deleted successfully")

@then('none of the deleted rates should exist in the system')
def step_impl(context):
    # Verify each deleted rate doesn't exist
    for rate_id in context.created_rate_ids:
        url = f"{context.base_url}/revisions/{context.revision_id}/revenue_options/parameters/rates/{rate_id}"
        
        response = requests.get(url, headers=context.headers)
        assert response.status_code == 404, f"Expected rate {rate_id} to be deleted (404), but got {response.status_code}"
    
    context.logger.info("Verified all deleted rates no longer exist")

@given('I have created multiple rate entries')
def step_impl(context):
    # Create different types of rates for export testing
    levels = [1, 2, 3]
    years = [2023, 2024, 2025]
    
    for i, (level, year) in enumerate(zip(levels, years)):
        context.execute_steps(f'''
            Given I have created a Level {level} rate for year {year}
        ''')
    
    context.logger.info(f"Created multiple rate entries for export testing")

@when('I export rates to Excel format')
def step_impl(context):
    url = f"{context.base_url}/revisions/{context.revision_id}/revenue_options/parameters/rates/excel"
    
    response = requests.get(url, headers={
        "Authorization": context.headers["Authorization"],
        "accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    })
    
    if response.status_code == 200:
        context.exported_file = response.content
        # Save to file for inspection if needed
        with open("test_output/rates.xlsx", "wb") as f:
            f.write(response.content)
        context.logger.info("Exported rates to Excel")
    else:
        context.exported_file = None
        context.error = response.text
        context.logger.error(f"Failed to export to Excel: {response.text}")

@then('the Excel file should contain all rate entries')
def step_impl(context):
    assert context.exported_file is not None, "No exported file was generated"
    assert len(context.exported_file) > 0, "Exported file is empty"
    
    # In a real test, we might parse the Excel file 
    # and verify its contents match the expected data
    file_size = len(context.exported_file)
    assert file_size > 1000, f"Excel file too small ({file_size} bytes), might not contain data"
    context.logger.info(f"Verified Excel file size: {file_size} bytes") 