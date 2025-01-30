create database device_event_db;

USE device_event_db;

show tables in device_event_db;

SELECT * from events;

DROP TABLE categories;
 
DROP SCHEMA device_event_db;

INSERT INTO categories (name, description) VALUES
('DeviceOnline', 'Tracking Device is connected to internet, this could be as a result of the device being turned on or gaining connectivity after loss'),
('DeviceOffline', 'Tracking Device is not connected to internet, this could be as a result of the device being turned off or losing connectivity'),
('DeviceHeartbeat', 'A ping request sent by device every 5 minutes to show online state'),
('DeviceBatteryLow', 'Battery of our device is low and has reached threshold to notify customer (20% - low, 10% - very low, 4% - critical)'),
('DeviceCharging', 'Device plugged in to charge'),
('DeviceOverheating', 'A warning for when a device gets too hot due to over charging or location temperature')
