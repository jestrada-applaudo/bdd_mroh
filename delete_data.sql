-- Delete in the correct order to respect foreign key constraints
BEGIN TRANSACTION;

-- Turn off NOCOUNT to reduce output noise
SET NOCOUNT ON;

-- First delete any test revisions that may reference the test OpCo
DELETE FROM master.revision.revisions 
WHERE revision_id = '12345678-1234-1234-1234-123456789012'
   OR (opco_id = '11111111-1111-1111-1111-111111111111' AND revision_name LIKE 'Test%')
PRINT 'Deleted test revisions';

-- Delete test Lines (depend on Hangar and OpCo)
DELETE FROM master.parameter.lines 
WHERE line_id = '55555555-5555-5555-5555-555555555555'
   OR op_co_id = '11111111-1111-1111-1111-111111111111' AND line_code = 'TEST-LINE';
PRINT 'Deleted test lines';

-- Delete test Aircraft (depends on Fleet Type)
DELETE FROM master.parameter.aircrafts 
WHERE aircraft_id = '33333333-3333-3333-3333-333333333333'
   OR tail_number = 'TEST-REG';
PRINT 'Deleted test aircraft';

-- Delete test Check Types
DELETE FROM master.parameter.check_types 
WHERE check_type_id = '44444444-4444-4444-4444-444444444444'
   OR check_type_name = 'TEST-CHECK';
PRINT 'Deleted test check types';

-- Delete test Customers
DELETE FROM master.parameter.customers 
WHERE customer_id = '22222222-2222-2222-2222-222222222222'
   OR customer_code = 'TEST-CUSTOMER';
PRINT 'Deleted test customers';

-- Delete test Hangars (depends on OpCo)
DELETE FROM master.parameter.hangars 
WHERE hangar_id = '88888888-8888-8888-8888-888888888888'
   OR (op_co_id = '11111111-1111-1111-1111-111111111111' AND hangar_code = 'TEST-HANGAR');
PRINT 'Deleted test hangars';

-- Delete test Fleet Types (depends on Family Fleet)
DELETE FROM master.parameter.fleet_types 
WHERE fleet_type_id = '77777777-7777-7777-7777-777777777777'
   OR fleet_type_name = 'Test Fleet Type';
PRINT 'Deleted test fleet types';

-- Delete test Family Fleets
DELETE FROM master.parameter.family_fleets 
WHERE family_fleet_id = 'AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA'
   OR family_fleet_name = 'Test Family Fleet';
PRINT 'Deleted test family fleets';

-- Finally delete test OpCo
DELETE FROM master.parameter.opcos 
WHERE opco_id = '11111111-1111-1111-1111-111111111111'
   OR opco_name = 'Test OpCo';
PRINT 'Deleted test OpCo';

-- If everything succeeded, commit the transaction
COMMIT TRANSACTION;
PRINT 'All test data successfully deleted';