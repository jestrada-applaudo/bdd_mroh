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
    context.rate_ids = []  # Add this line to track rate IDs
    
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
    if 'revenue_test' in scenario.tags and not context.revision_id:
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
    if hasattr(context, 'rate_ids') and context.rate_ids:
        url = f"{context.base_url}/revisions/revenue_options/parameters/rates/delete"
        data = {"rateIds": context.rate_ids}
        try:
            response = requests.put(url, headers=context.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                context.logger.info(f"Cleaned up {len(result.get('deletedRates', []))} rate entries")
            else:
                context.logger.error(f"Failed to clean up rates: {response.text}")
        except Exception as e:
            context.logger.error(f"Error cleaning up rates: {str(e)}")
    
    context.logger.info("Test run completed")

def create_test_revision(context, scenario_name):
    url = f"{context.base_url}/revisions"
    now = datetime.now()
    
    data = {
        "opCo": os.getenv('TEST_OPCO_ID', '3fa85f64-5717-4562-b3fc-2c963f66afa6'),
        "fromRevision": os.getenv('FROM_REVISION_ID', '3fa85f64-5717-4562-b3fc-2c963f66afa6'),
        "revisionName": f"Test {scenario_name[:20]} {now.strftime('%Y%m%d%H%M%S')}",
        "revisionType": "TEST",
        "year": now.year,
        "week": int(now.strftime("%V")),
        "comment": "Automated test revision",
        "baseline": now.isoformat(),
        "closure": (now + timedelta(days=7)).isoformat(),
        "isOfficial": True
    }
    
    try:
        response = requests.post(url, headers=context.headers, json=data)
        if response.status_code == 200:
            result = response.json()
            context.revision_id = result.get("revisionId")
            context.logger.info(f"Created test revision: {context.revision_id}")
        else:
            context.logger.error(f"Failed to create revision: Status {response.status_code}, Response: {response.text}")
    except Exception as e:
        context.logger.error(f"Exception creating revision: {str(e)}")