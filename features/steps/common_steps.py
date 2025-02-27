from behave import given

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
