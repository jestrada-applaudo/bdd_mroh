# Revenue Management System BDD Tests

This project contains BDD tests for the Revenue Management System, focusing on labor revenue management.

## Setup

1. Create virtual environment:
python3 -m venv venv
2. Activate virtual environment:
source venv/bin/activate
3. Install dependencies:
pip install -r requirements.txt
4. Configure API access in `.env`:
API_BASE_URL=http://your-api-url.com/api
API_TOKEN=your_api_token
## Running the Tests
To run all tests:
behave
To run specific tests:
behave features/revenue/labor_revenue.feature
behave features/revenue/rates.feature
behave features/rate_assignment.feature
To run tests with specific tags:
behave --tags=@revenue_test
behave --tags=@rates_test
## Test Structure

- `features/`: Contains all feature files
- `features/steps/`: Contains step definitions
- `features/revenue/`: Contains revenue-specific features
- `features/revenue/rates.feature`: Contains general rate management tests
- `features/rate_assignment.feature`: Contains rate assignment API tests


# BDD Testing Framework Structure

## Current Implementation (Phase 1)
```
features/
├── rate_assignment.feature    # Rate assignment API tests (level-based prioritization)
├── steps/                     # Step definitions
│   ├── common_steps.py
│   ├── revenue_labor_steps.py
│   ├── rates_steps.py
│   └── rate_assignment_steps.py
└── revenue/                   # Revenue domain
    ├── labor/                 # Labor revenue tests
    │   ├── create_labor.feature          # Create labor revenue entries
    │   ├── update_labor.feature          # Update existing labor entries
    │   ├── delete_labor.feature          # Delete labor entries
    │   ├── get_labor.feature             # Get single labor entry
    │   ├── get_all_labor.feature         # List all labor entries
    │   ├── generate_labor_csv.feature    # Export to CSV
    │   └── generate_labor_excel.feature  # Export to Excel
    └── rates.feature          # Rate management (CRUD operations)
```

## Planned Phases

### Phase 2: Complete Revenue Domain
```
revenue_domain/
├── labor/                      # (Completed in Phase 1)
├── material/                   # Material revenue tests
│   ├── create_material.feature
│   ├── update_material.feature
│   ├── delete_material.feature
│   ├── get_material.feature
│   ├── get_all_material.feature
│   ├── generate_material_csv.feature
│   └── generate_material_excel.feature
├── engineering/                # Engineering revenue tests
│   ├── create_engineering.feature
│   ├── update_engineering.feature
│   ├── delete_engineering.feature
│   ├── get_engineering.feature
│   ├── get_all_engineering.feature
│   ├── generate_engineering_csv.feature
│   └── generate_engineering_excel.feature
└── miscellaneous/             # Miscellaneous revenue tests
    ├── create_misc.feature
    ├── update_misc.feature
    ├── delete_misc.feature
    ├── get_misc.feature
    ├── get_all_misc.feature
    ├── generate_misc_csv.feature
    └── generate_misc_excel.feature
```

### Phase 3: Parameter Domain
```
parameter_domain/
├── aircraft/                   # Aircraft management tests
│   ├── create_aircraft.feature
│   ├── update_aircraft.feature
│   ├── delete_aircraft.feature
│   ├── get_aircraft.feature
│   └── get_all_aircraft.feature
├── category/                   # Category management tests
│   ├── create_category.feature
│   ├── update_category.feature
│   ├── delete_category.feature
│   ├── get_category.feature
│   └── get_all_category.feature
├── checktype/                  # Check type management tests
│   ├── create_checktype.feature
│   ├── update_checktype.feature
│   ├── delete_checktype.feature
│   ├── get_checktype.feature
│   └── get_all_checktype.feature
├── customer/                   # Customer management tests
│   ├── create_customer.feature
│   ├── update_customer.feature
│   ├── delete_customer.feature
│   ├── get_customer.feature
│   └── get_all_customer.feature
├── familyfleet/               # Family fleet management tests
│   ├── create_familyfleet.feature
│   ├── update_familyfleet.feature
│   ├── delete_familyfleet.feature
│   ├── get_familyfleet.feature
│   └── get_all_familyfleet.feature
└── fleettype/                 # Fleet type management tests
    ├── create_fleettype.feature
    ├── update_fleettype.feature
    ├── delete_fleettype.feature
    ├── get_fleettype.feature
    └── get_all_fleettype.feature
```

### Phase 4: Revision Domain
```
revision_domain/
├── revision/                   # Basic revision management tests
│   ├── create_revision.feature
│   ├── update_revision.feature
│   ├── delete_revision.feature
│   ├── get_revision.feature
│   └── get_all_revision.feature
├── rates/                      # Rates functionality tests
│   ├── create_rate.feature
│   ├── update_rate.feature
│   ├── delete_rate.feature
│   ├── get_rate.feature
│   ├── assign_rates.feature   # Rate assignment functionality
│   └── get_rates.feature
├── heat_map/                   # Heat map functionality tests
│   ├── generate_heatmap.feature
│   └── get_heatmap.feature
├── block_restriction/          # Block restrictions tests
│   ├── create_block.feature
│   ├── update_block.feature
│   ├── delete_block.feature
│   └── get_block.feature
└── holidays/                   # Holiday management tests
    ├── create_holiday.feature
    ├── update_holiday.feature
    ├── delete_holiday.feature
    └── get_holiday.feature
```

## Support Files Structure
```
support/
├── steps/                      # Step definitions
│   ├── common/                # Shared steps
│   ├── parameter/             # Parameter domain steps
│   ├── revision/              # Revision domain steps
│   └── revenue/               # Revenue domain steps
├── environment.py             # Test environment setup
├── requirements.txt           # Dependencies
└── .env                      # Configuration
```

## Implementation Timeline

1. **Current Phase (Phase 1)**
   - Basic Labor revenue functionality
   - Core test infrastructure
   - Essential step definitions
   - Rate management (CRUD operations)
   - Rate assignment functionality

2. **Next Steps (Phase 2)**
   - Complete Labor revenue features
   - Material revenue implementation
   - Engineering revenue implementation
   - Miscellaneous revenue implementation

3. **Future Phases**
   - Parameter domain implementation
   - Revision domain implementation
   - Integration tests
   - Performance tests

## Development Guidelines

### Adding New Features
1. Focus on revenue domain completion first
2. Implement features in order of business priority
3. Maintain consistent structure across new implementations
4. Reuse common steps where possible

### Best Practices
- Start with basic CRUD operations
- Add complex scenarios incrementally
- Document dependencies between features
- Maintain clear separation between revenue types

## Test Categories (Current Focus)

### Labor Revenue Tests
- Creation of labor revenue entries
- Retrieval of labor revenue data
- Deletion of labor revenue entries

### Rate Management Tests
- Creating/updating/deleting rate entries for different levels
- Searching and filtering rates
- Sorting and pagination of rate data
- Validation of rate fields

### Rate Assignment Tests
- Assigning rates at Level 1 (Customer + Year)
- Assigning rates at Level 2 (Customer + Year + Fleet Type)
- Assigning rates at Level 3 (Customer + Year + Check Type)
- Default values when no applicable rates are found

### Coming Soon
- Material management
- Engineering management
- Miscellaneous management

## Configuration and Setup

### Current Requirements
- Python 3.8+
- behave==1.2.6
- requests==2.28.1
- python-dotenv==0.21.0

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with appropriate values
```

### Running Tests
```bash
# Run all implemented tests
behave

# Run specific revenue feature
behave features/revenue/labor/creation.feature

# Run rate management tests
behave features/revenue/rates.feature

# Run rate assignment tests
behave features/rate_assignment.feature

# Run tests with specific tag
behave --tags=@labor_revenue
behave --tags=@rates_test
```

## Rate Assignment API

The Rate Assignment API allows assigning rates based on three hierarchical levels:

1. Level 1: Customer/Year/Opco (lowest priority)
2. Level 2: Customer/Year/Fleet Type (medium priority)
3. Level 3: Customer/Year/Check Type (highest priority)

The API endpoint being tested is:
```
POST /revisions/{revisionId}/rates/assign
```

Example request:
```json
{
  "year": 2023,
  "customerId": "22222222-2222-2222-2222-222222222222",
  "checkTypeId": "44444444-4444-4444-4444-444444444444"
}
```
