import os
import logging
import uuid
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timedelta
import pathlib

# Create output directory for test files
pathlib.Path("test_output").mkdir(exist_ok=True)

def before_all(context):
    # Load configuration
    load_dotenv()
    context.base_url = os.getenv('API_BASE_URL', 'http://localhost:8085/mroh-backend-hms/api')
    context.token = os.getenv('API_TOKEN')
    
    # Set up API clients
    context.headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {context.token}",
        "Content-Type": "application/json"
    }
    
    # Track test data
    context.revision_id = None
    context.revenue_ids = []
    context.reference_entities = {}
    context.rate_ids = []  # Track rate IDs
    context.flag_ids = []  # Track flag IDs
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("test_output/bdd_test.log"),
            logging.StreamHandler()
        ]
    )
    context.logger = logging.getLogger(__name__)
    context.logger.info("Test run started")

def before_scenario(context, scenario):
    context.logger.info(f"Starting scenario: {scenario.name}")
    
    # Create a revision if needed and none exists
    if ('revenue_test' in scenario.tags or 'rates_test' in scenario.tags or 'flags_test' in scenario.tags) and not context.revision_id:
        create_test_revision(context, scenario.name)
    
    # Create reference entities if needed
    if hasattr(context, 'reference_entities') and not context.reference_entities:
        # In a real implementation, you might verify these entities exist
        # or create them if they don't
        pass

def after_scenario(context, scenario):
    context.logger.info(f"Completed scenario: {scenario.name}")

def after_all(context):
    # Clean up created revenues
    if context.revenue_ids:
        url = f"{context.base_url}/revisions/revenue_options/parameters/labor/delete"
        data = {"revenueIds": context.revenue_ids}
        try:
            response = requests.put(url, headers=context.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                context.logger.info(f"Cleaned up {len(result.get('deletedRevenues', []))} labor revenue entries")
            else:
                context.logger.error(f"Failed to clean up revenues: {response.text}")
        except Exception as e:
            context.logger.error(f"Error cleaning up revenues: {str(e)}")
    
    # Clean up created rates
    if hasattr(context, 'rate_ids') and context.rate_ids and hasattr(context, 'revision_id') and context.revision_id:
        url = f"{context.base_url}/revisions/{context.revision_id}/rates/delete"
        data = {"rateIds": context.rate_ids}
        try:
            response = requests.put(url, headers=context.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                context.logger.info(f"Cleaned up {len(result.get('deletedItems', []))} rate entries")
            else:
                context.logger.error(f"Failed to clean up rates: {response.text}")
        except Exception as e:
            context.logger.error(f"Error cleaning up rates: {str(e)}")
    
    # Clean up created flags
    if hasattr(context, 'flag_ids') and context.flag_ids and hasattr(context, 'revision_id') and context.revision_id:
        deleted_count = 0
        for flag_id in context.flag_ids:
            url = f"{context.base_url}/revisions/{context.revision_id}/flags"
            payload = {"id": flag_id}
            try:
                response = requests.delete(url, headers=context.headers, json=payload)
                if response.status_code == 200:
                    deleted_count += 1
                else:
                    context.logger.error(f"Failed to clean up flag {flag_id}: {response.text}")
            except Exception as e:
                context.logger.error(f"Error cleaning up flag {flag_id}: {str(e)}")
        
        context.logger.info(f"Cleaned up {deleted_count} flag entries")
    
    context.logger.info("Test run completed")

def create_test_revision(context, scenario_name):
    url = f"{context.base_url}/revisions"
    now = datetime.now()
    
    # Make the revision name more unique
    uuid_part = str(uuid.uuid4())[:8]
    # Remove any problematic characters from scenario name
    safe_name = ''.join(c for c in scenario_name[:15] if c.isalnum() or c.isspace())
    
    data = {
        "opCo": os.getenv('TEST_OPCO_ID', '3fa85f64-5717-4562-b3fc-2c963f66afa6'),
        "fromRevision": os.getenv('FROM_REVISION_ID', '3fa85f64-5717-4562-b3fc-2c963f66afa6'),
        "revisionName": f"Test_{safe_name}_{now.strftime('%Y%m%d%H%M%S')}_{uuid_part}",
        "revisionType": "TEST",
        "year": now.year,
        "week": int(now.strftime("%V")),
        "comment": "Automated test revision",
        "baseline": now.isoformat(),
        "closure": (now + timedelta(days=7)).isoformat(),
        "isOfficial": False  # Set to False to avoid conflicts
    }
    
    try:
        response = requests.post(url, headers=context.headers, json=data)
        if response.status_code == 200:
            result = response.json()
            context.revision_id = result.get("revisionId")
            context.logger.info(f"Created test revision: {context.revision_id}")
            assert context.revision_id, "Test revision not created"
        else:
            context.logger.error(f"Failed to create revision: Status {response.status_code}, Response: {response.text}")
            # Try one more time with a completely random name
            data["revisionName"] = f"Test_BDD_{now.strftime('%Y%m%d%H%M%S')}_{uuid.uuid4()}"
            response = requests.post(url, headers=context.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                context.revision_id = result.get("revisionId")
                context.logger.info(f"Created test revision (retry): {context.revision_id}")
                assert context.revision_id, "Test revision not created on retry"
            else:
                context.logger.error(f"Failed to create revision on retry: Status {response.status_code}, Response: {response.text}")
                assert False, "Test revision not created"
    except Exception as e:
        context.logger.error(f"Exception creating revision: {str(e)}")
        assert False, f"Test revision creation failed: {str(e)}"