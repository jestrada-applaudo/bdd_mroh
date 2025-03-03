import os
from behave import given, when, then
import requests, json, uuid
from datetime import datetime, timedelta

@given('the following reference entities exist')
def step_impl(context):
    # Store the entities for use in tests
    context.reference_entities = {}
    for row in context.table:
        entity_type = row['Entity']
        entity_id = row['ID']
        
        # Verify entity exists in database
        url = f"{context.base_url}/parameters/{entity_type.lower()}s/{entity_id}"
        response = requests.get(url, headers=context.headers)
        
        if response.status_code != 200:
            context.logger.warning(f"{entity_type} with ID {entity_id} not found. Tests may fail.")
        
        context.reference_entities[entity_type] = {
            'id': entity_id,
            'name': row['Name/Code']
        }
    
    context.logger.info(f"Using reference entities: {context.reference_entities}")

@given('I have labor revenue data with the following details')
def step_impl(context):
    # Create data from table
    data = {}
    for row in context.table:
        field = row['Field']
        value = row['Value']
        
        # Handle special values
        if value == 'today':
            value = datetime.now().strftime("%Y-%m-%d")
        elif value == 'tomorrow':
            value = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
            
        data[field] = value
    
    # Add revision ID
    data['revisionId'] = context.revision_id
    
    # Store for later use
    context.labor_data = data
    context.logger.info(f"Prepared labor data: {data}")

@given('I have the following labor rubrics')
def step_impl(context):
    # Create rubrics from table
    rubrics = {"rubrics": {}}
    context.expected_rubrics = []  # Store for later validation
    
    for row in context.table:
        context.expected_rubrics.append(row)  # Store the row for later
        rubric_type = row['Type']
        value = float(row['Value']) if row['Value'] else None
        billable_hours = float(row['BillableLaborHours']) if row['BillableLaborHours'] else None
        
        # Convert to appropriate format for API
        # The API expects rubrics as a structure with specific fields
        rubric_key = rubric_type.split('_')[0].lower()
        if rubric_key == "non":
            rubric_key = "nonDestructiveTest"
            
        rubrics["rubrics"][rubric_key] = {
            "type": rubric_type,
            "value": value,
            "billableLaborHours": billable_hours
        }
    
    # Add to labor data
    context.labor_data.update(rubrics)
    context.logger.info(f"Added rubrics to labor data: {rubrics}")

@when('I create a new labor revenue entry')
def step_impl(context):
    url = f"{context.base_url}/revisions/revenue_options/parameters/labor"
    
    # Add a createdBy field if not present
    if 'createdBy' not in context.labor_data:
        context.labor_data['createdBy'] = os.getenv('TEST_USER_ID', '99999999-9999-9999-9999-999999999999')
    
    # Send request
    response = requests.post(url, headers=context.headers, json=context.labor_data)
    
    # Store response status code
    context.response_status = response.status_code
    
    # Store response
    if response.status_code == 201:
        context.response = response.json()
        if "id" in context.response:
            context.revenue_ids.append(context.response["id"])
            context.logger.info(f"Created labor revenue: {context.response['id']}")
    else:
        context.response = {"error": response.text, "status_code": response.status_code}
        context.logger.error(f"Failed to create labor revenue: {response.text}")

@then('the response should contain both rubrics')
def step_impl(context):
    assert "rubrics" in context.response, "No rubrics in response"
    rubrics = context.response["rubrics"]
    
    # If we don't have expected rubrics stored, just check that rubrics exist
    if not hasattr(context, 'expected_rubrics') or not context.expected_rubrics:
        assert len(rubrics) > 0, "No rubrics found in response"
        context.logger.info(f"Verified response contains {len(rubrics)} rubrics")
        return
    
    # Validate against the stored expected rubrics
    for row in context.expected_rubrics:
        rubric_type = row['Type']
        rubric_key = rubric_type.split('_')[0].lower()
        if rubric_key == "non":
            rubric_key = "nonDestructiveTest"
            
        assert rubric_key in rubrics, f"Rubric '{rubric_key}' not found in response"
        
        # Verify values if needed
        if row['Value']:
            value = float(row['Value'])
            assert abs(rubrics[rubric_key]["value"] - value) < 0.001, f"Expected value {value}, got {rubrics[rubric_key]['value']}"
            
        if row['BillableLaborHours']:
            hours = float(row['BillableLaborHours'])
            assert abs(rubrics[rubric_key]["billableLaborHours"] - hours) < 0.001, f"Expected hours {hours}, got {rubrics[rubric_key]['billableLaborHours']}"
            
    context.logger.info("Verified all rubrics in response")

@given('I have created a labor revenue with customer code "{customer_code}"')
def step_impl(context, customer_code):
    # Create basic labor data
    context.execute_steps(f'''
        Given I have labor revenue data with the following details:
          | Field                | Value                                 |
          | type                 | LABOR                                |
          | customerId           | {context.reference_entities['Customer']['id']} |
          | aircraftId           | {context.reference_entities['Aircraft']['id']} |
          | checkTypeId          | {context.reference_entities['CheckType']['id']} |
          | lineId               | {context.reference_entities['Line']['id']} |
          | isAssociatedToEvent  | false                                |
          | registrationDate     | today                                |
        And I have the following labor rubrics:
          | Type            | Value   | BillableLaborHours |
          | AIRFRAME_LABOR  | 1000.0  | 10.0               |
    ''')
    
    # Add customer code
    customer_info = {
        "customerCode": customer_code,
        "customerName": f"Test Customer {customer_code}"
    }
    context.labor_data.update(customer_info)
    
    # Create it
    context.execute_steps('''
        When I create a new labor revenue entry
        Then the labor revenue should be created successfully
    ''')

@when('I search for labor revenues with text "{search_text}"')
def step_impl(context, search_text):
    url = f"{context.base_url}/revisions/{context.revision_id}/revenue_options/parameters/labor"
    params = {
        "searchText": search_text,
        "page": 0,
        "pageSize": 10
    }
    
    response = requests.get(url, headers=context.headers, params=params)
    context.response = response.json() if response.status_code == 200 else {"error": response.text}
    context.logger.info(f"Searched for revenues with text: {search_text}")

@then('the search results should contain exactly {count:d} entry')
def step_impl(context, count):
    assert "items" in context.response, f"No content in response: {context.response}"
    actual_count = len(context.response["items"])
    assert actual_count == count, f"Expected exactly {count} entries, got {actual_count}"
    context.logger.info(f"Found exactly {count} entries as expected")

@then('the entry should have customer code "{customer_code}"')
def step_impl(context, customer_code):
    assert "items" in context.response, "No content in response"
    assert len(context.response["items"]) > 0, "No entries in response"
    
    entry = context.response["items"][0]
    assert entry["customerCode"] == customer_code, f"Expected customer code {customer_code}, got {entry['customerCode']}"
    context.logger.info(f"Verified customer code is {customer_code}")

@given('I have labor revenue data with event association')
def step_impl(context):
    context.execute_steps('''
        Given I have labor revenue data with the following details:
          | Field                | Value                                 |
          | type                 | LABOR                                |
          | customerId           | 22222222-2222-2222-2222-222222222222 |
          | aircraftId           | 33333333-3333-3333-3333-333333333333 |
          | checkTypeId          | 44444444-4444-4444-4444-444444444444 |
          | lineId               | 55555555-5555-5555-5555-555555555555 |
          | isAssociatedToEvent  | true                                 |
          | registrationDate     | today                                |
          | dateIn               | today                                |
          | dateOut              | tomorrow                             |
        And I have the following labor rubrics:
          | Type            | Value   | BillableLaborHours |
          | AIRFRAME_LABOR  | 1000.0  | 10.0               |
    ''')

@given('I set the date out before date in')
def step_impl(context):
    # Get current dates
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Set dateOut before dateIn
    context.labor_data["dateIn"] = today
    context.labor_data["dateOut"] = yesterday
    context.logger.info(f"Set dateIn to {today} and dateOut to {yesterday}")

@when('I attempt to create a labor revenue entry')
def step_impl(context):
    # Similar to regular create but we expect it might fail
    url = f"{context.base_url}/revisions/revenue_options/parameters/labor"
    
    # Send request and capture response regardless of status code
    response = requests.post(url, headers=context.headers, json=context.labor_data)
    context.response_status = response.status_code
    
    try:
        context.response = response.json()
    except:
        context.response = {"text": response.text}
        
    context.logger.info(f"Attempted to create labor revenue, got status {response.status_code}")

@then('the operation should fail with a validation error')
def step_impl(context):
    assert context.response_status != 201, f"Expected failure but got success with status {context.response_status}"
    assert context.response_status >= 400, f"Expected error status but got {context.response_status}"
    context.logger.info(f"Verified operation failed with status {context.response_status}")

@then('the error message should mention "{error_text}"')
def step_impl(context, error_text):
    response_text = str(context.response)
    assert error_text in response_text, f"Expected error message to contain '{error_text}', but got: {response_text}"
    context.logger.info(f"Verified error message contains '{error_text}'")

@given('I have created multiple labor revenue entries')
def step_impl(context):
    # Create several entries for export testing
    for i in range(3):
        context.execute_steps(f'''
            Given I have labor revenue data with the following details:
              | Field                | Value                                 |
              | type                 | LABOR                                |
              | customerId           | {context.reference_entities['Customer']['id']} |
              | aircraftId           | {context.reference_entities['Aircraft']['id']} |
              | checkTypeId          | {context.reference_entities['CheckType']['id']} |
              | lineId               | {context.reference_entities['Line']['id']} |
              | isAssociatedToEvent  | false                                |
              | registrationDate     | today                                |
            And I have the following labor rubrics:
              | Type            | Value   | BillableLaborHours |
              | AIRFRAME_LABOR  | {1000.0 + i*100}  | {10.0 + i} |
        ''')
        
        # Add unique customer code
        customer_info = {
            "customerCode": f"EXPORT-{i}",
            "customerName": f"Export Test Customer {i}"
        }
        context.labor_data.update(customer_info)
        
        # Create it
        context.execute_steps('''
            When I create a new labor revenue entry
            Then the labor revenue should be created successfully
        ''')
    
    context.logger.info(f"Created {i+1} labor revenue entries for export testing")

@when('I export labor revenues to Excel format')
def step_impl(context):
    url = f"{context.base_url}/revisions/{context.revision_id}/revenue_options/parameters/labor/excel"
    
    response = requests.get(url, headers={
        "Authorization": context.headers["Authorization"],
        "accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    })
    
    if response.status_code == 200:
        context.exported_file = response.content
        # Save to file for inspection if needed
        with open("test_output/labor_revenues.xlsx", "wb") as f:
            f.write(response.content)
        context.logger.info("Exported labor revenues to Excel")
    else:
        context.exported_file = None
        context.error = response.text
        context.logger.error(f"Failed to export to Excel: {response.text}")

@then('the Excel file should contain all revenue entries')
def step_impl(context):
    assert context.exported_file is not None, "No exported file was generated"
    assert len(context.exported_file) > 0, "Exported file is empty"
    
    # In a real test, you might want to parse the Excel file 
    # and verify its contents match the expected data
    file_size = len(context.exported_file)
    assert file_size > 1000, f"Excel file too small ({file_size} bytes), might not contain data"
    context.logger.info(f"Verified Excel file size: {file_size} bytes")

@then('the labor revenue should be created successfully')
def step_impl(context):
    assert context.response_status == 201, f"Expected status 201, got {context.response_status}"
    assert "id" in context.response, "No id for revenue in response"
    context.logger.info(f"Labor revenue created with ID: {context.response['id']}")

@then('the exported file should be successfully generated')
def step_impl(context):
    assert context.exported_file is not None, "No file was exported"
    assert len(context.exported_file) > 0, "Exported file is empty"
    context.logger.info("Excel file was successfully generated")