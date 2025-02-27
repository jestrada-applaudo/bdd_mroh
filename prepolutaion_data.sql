-- Set up test user ID for created_by/last_modified_by fields
DECLARE @TestUserId UNIQUEIDENTIFIER = '99999999-9999-9999-9999-999999999999';

-- Insert OpCo
INSERT INTO master.[parameter].opcos 
(opco_id, opco_name, logo_blob_name, status, created_by, last_modified_by)
VALUES 
('11111111-1111-1111-1111-111111111111', 'Test OpCo', 'test-logo.png', 'ACTIVE', @TestUserId, @TestUserId);

-- Insert Family Fleet (required for Fleet Type)
INSERT INTO master.parameter.family_fleets
(family_fleet_id, aircraft_manufacturer, family_fleet_name, body_type, status, created_by, last_modified_by)
VALUES
('AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA', 'Boeing', 'Test Family Fleet', 'NARROW BODY', 'ACTIVE', @TestUserId, @TestUserId);

-- Insert Fleet Type (references Family Fleet)
INSERT INTO master.parameter.fleet_types 
(fleet_type_id, fleet_type_name, family_fleet_id, status, created_by, last_modified_by)
VALUES 
('77777777-7777-7777-7777-777777777777', 'Test Fleet Type', 'AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA', 'ACTIVE', @TestUserId, @TestUserId);

-- Insert a Hangar (required for Line)
INSERT INTO master.parameter.hangars 
(hangar_id, op_co_id, hangar_code, hangar_name, hangar_order, status, created_by, last_modified_by, active, overflow)
VALUES 
('88888888-8888-8888-8888-888888888888', '11111111-1111-1111-1111-111111111111', 'TEST-HANGAR', 'Test Hangar', 1, 'ACTIVE', @TestUserId, @TestUserId, 1, 1);

-- Insert Customer
INSERT INTO master.parameter.customers 
(customer_id, customer_name, customer_code, color_hex, status, created_by, last_modified_by)
VALUES 
('22222222-2222-2222-2222-222222222222', 'Test Customer', 'TEST-CUSTOMER', '#FF5733', 'ACTIVE', @TestUserId, @TestUserId);

-- Insert Aircraft (references Fleet Type)
INSERT INTO master.parameter.aircrafts 
(aircraft_id, tail_number, ship_number, fleet_type_id, status, created_by, last_modified_by)
VALUES 
('33333333-3333-3333-3333-333333333333', 'TEST-REG', 'SHIP001', '77777777-7777-7777-7777-777777777777', 'ACTIVE', @TestUserId, @TestUserId);

-- Insert Check Type
INSERT INTO master.parameter.check_types 
(check_type_id, check_type_name, additional_information, status, created_by, last_modified_by)
VALUES 
('44444444-4444-4444-4444-444444444444', 'TEST-CHECK', 'Test Check Type', 'ACTIVE', @TestUserId, @TestUserId);

-- Insert Line (with required hangar association and op_co_id instead of opco_id)
INSERT INTO master.parameter.lines 
(line_id, hangar_id, op_co_id, line_code, line_name, line_order, active, status, created_by, last_modified_by)
VALUES 
('55555555-5555-5555-5555-555555555555', '88888888-8888-8888-8888-888888888888', '11111111-1111-1111-1111-111111111111', 'TEST-LINE', 'Test Line', 1, 1, 'ACTIVE', @TestUserId, @TestUserId);

-- Insert a test Revision (optional, as the test will create one, but useful for debugging)
INSERT INTO master.revision.revisions 
(revision_id, opco_id, revision_name, revision_type, year, week, status, is_official)
VALUES 
('12345678-1234-1234-1234-123456789012', '11111111-1111-1111-1111-111111111111', 'Test BDD Revision', 'TEST', YEAR(GETDATE()), DATEPART(WEEK, GETDATE()), 'ACTIVE', 0);