from behave import given
import requests

@given('the API is accessible')
def step_impl(context):
    # Simple check - could be enhanced
    assert context.base_url, "API base URL not configured"
    assert context.token, "API token not configured"
    context.logger.info("API configuration verified")

@given('I am authenticated with valid credentials')
def step_impl(context):
    assert context.headers.get("Authorization"), "Authentication header not set"
    context.logger.info("Authentication configured")

@given('a test revision exists')
def step_impl(context):
    assert context.revision_id, "Test revision not created"
    context.logger.info(f"Using test revision: {context.revision_id}")

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
