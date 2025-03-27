from behave import when, then
import requests
import json
import os
from datetime import datetime, timedelta

@when('I assign rates with the following parameters')
def step_impl(context):
    # Create request data from table
    data = {}
    for row in context.table:
        param = row['Parameter']
        value = row['Value']
        
        # Convert to appropriate type
        if param == 'year':
            value = int(value)
        
        data[param] = value
    
    # Store the parameters for future use
    context.rate_params = data
    
    # Build the URL
    url = f"{context.base_url}/revisions/{context.revision_id}/rates/assign"
    
    # Make the request
    context.logger.info(f"Calling rate assignment API with params: {data}")
    response = requests.post(url, headers=context.headers, json=data)
    
    # Store response
    context.response_status = response.status_code
    try:
        context.response = response.json()
        context.logger.info(f"Rate assignment response: {json.dumps(context.response, indent=2)}")
    except Exception as e:
        context.response = {"error": str(e), "text": response.text}
        context.logger.error(f"Failed to parse response: {e}, raw response: {response.text}")

@then('the rate assignment should return status code {status_code:d}')
def step_impl(context, status_code):
    assert context.response_status == status_code, f"Expected status {status_code}, got {context.response_status}"
    context.logger.info(f"Verified status code: {status_code}")

@then('the response should contain the following rates')
def step_impl(context):
    # Extract expected rates from table
    expected_rates = {}
    for row in context.table:
        rate_type = row['Rate Type']
        value = row['Value']
        
        # Convert to appropriate type (numeric)
        if rate_type == 'level':
            expected_rates[rate_type] = int(value)
        else:
            # Consider both string and numeric rate values
            expected_rates[rate_type] = value
    
    # Verify each expected rate exists in the response
    for rate_type, expected_value in expected_rates.items():
        assert rate_type in context.response, f"Rate '{rate_type}' not found in response"
        
        actual_value = context.response[rate_type]
        
        # Handle different types of values (string vs numeric)
        if isinstance(actual_value, str) and not isinstance(expected_value, str):
            actual_value = int(float(actual_value)) if rate_type == 'level' else actual_value
        elif isinstance(expected_value, str) and expected_value.isdigit() and not isinstance(actual_value, str):
            expected_value = int(expected_value)
        
        assert str(actual_value) == str(expected_value), f"Expected {rate_type} to be {expected_value}, got {actual_value}"
    
    context.logger.info(f"Verified rates: {expected_rates}")

@then('the response should include customer information')
def step_impl(context):
    # Verify the response includes the customer ID and other customer-related fields
    assert 'customerId' in context.response, "Customer ID not found in response"
    
    # Verify the customerID matches what was sent in the prior step
    if hasattr(context, 'rate_params') and 'customerId' in context.rate_params:
        expected_customer_id = context.rate_params['customerId']
        assert context.response['customerId'] == expected_customer_id, f"Expected customerId {expected_customer_id}, got {context.response['customerId']}"
    
    # Check that other customer-related fields exist (even if null)
    assert 'customerName' in context.response, "Customer name field not found in response"
    
    # Optional: check for other related fields
    expected_fields = ['fleetTypeId', 'fleetTypeName', 'checkTypeId', 'checkTypeName']
    for field in expected_fields:
        assert field in context.response, f"Expected field {field} not found in response"
    
    context.logger.info("Verified customer information in response") 