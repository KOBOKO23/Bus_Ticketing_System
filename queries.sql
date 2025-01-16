
	CREATE TABLE bus (
    	busid VARCHAR(20) NOT NULL PRIMARY KEY,
    	origin VARCHAR(50) NOT NULL,
    	destination VARCHAR(50) NOT NULL,
    	cost INT NOT NULL,
    	rating DECIMAL(3,2) NOT NULL,
    	departure TIME,
    	arrival TIME,
    	capacity INT NOT NULL DEFAULT 60,
    	seats_left INT NOT NULL DEFAULT 60,
    	Action VARCHAR(50),
    	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
	);


	CREATE TABLE booking (
    	booking_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    	usersid VARCHAR(255) NOT NULL,
    	busid VARCHAR(20) NOT NULL,
    	name VARCHAR(255) NOT NULL,
    	passengers INT NOT NULL,
    	date_ DATETIME DEFAULT CURRENT_TIMESTAMP,
    	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    	phone VARCHAR(10) NOT NULL,
    	email VARCHAR(255) NOT NULL,
    	seat_number INT,
    	FOREIGN KEY (usersid) REFERENCES users(usersid)
	);


 	CREATE TABLE users (
    	usersid VARCHAR(255) PRIMARY KEY,
    	username VARCHAR(100) NOT NULL,
    	phone VARCHAR(20) NOT NULL,
    	email VARCHAR(50) NOT NULL UNIQUE,
    	password VARCHAR(255) NOT NULL,
    	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	other_names VARCHAR(255) NOT NULL,
    	physical_address VARCHAR(255) NOT NULL,
    	next_of_kin VARCHAR(255) NOT NULL,
    	reset_token VARCHAR(255) 
	);


	INSERT INTO bus (busid, origin, destination, cost, rating, departure, arrival, capacity, seats_left, Action)
    	VALUES
	('12345', 'Nairobi', 'Migori', 1299, 4.3, '16:07:38', '12:00:00', 60, 50, 'Book Now'),
        	('12346', 'Nairobi', 'Migori', 1399, 4.0, '09:30:00', '13:30:00', 60, 60, 'Book Now'),
        	('12347', 'Nairobi', 'Migori', 1499, 4.2, '11:00:00', '14:30:00', 60, 60, 'Book Now'),
        	('12348', 'Nairobi', 'Migori', 1599, 3.9, '14:00:00', '17:00:00', 60, 60, 'Book Now'),

        	('12349', 'Nairobi', 'Kitale', 1999, 3.3, '12:00:00', '15:00:00', 60, 60, 'Book Now'),
        	('12350', 'Nairobi', 'Kitale', 2099, 4.1, '07:30:00', '10:30:00', 60, 60, 'Book Now'),
        	('12351', 'Nairobi', 'Kitale', 2199, 3.7, '16:00:00', '19:00:00', 60, 60, 'Book Now'),
        	('12352', 'Nairobi', 'Kitale', 1899, 4.2, '08:00:00', '11:00:00', 60, 60, 'Book Now'),

        	('12353', 'Nairobi', 'Kisumu', 1289, 4.8, '12:00:00', '14:30:00', 60, 60, 'Book Now'),
        	('12354', 'Nairobi', 'Kisumu', 1389, 4.4, '06:00:00', '09:00:00', 60, 60, 'Book Now'),
        	('12355', 'Nairobi', 'Kisumu', 1489, 4.5, '15:00:00', '18:00:00', 60, 60, 'Book Now'),
        	('12356', 'Nairobi', 'Kisumu', 1589, 4.1, '10:30:00', '13:30:00', 60, 60, 'Book Now'),

        	('12357', 'Nairobi', 'Migori', 1499, 4.2, '17:30:00', '22:00:00', 60, 60, 'Book Now'),
        	('12358', 'Nairobi', 'Migori', 1599, 4.0, '11:30:00', '14:30:00', 60, 60, 'Book Now'),
        	('12359', 'Nairobi', 'Migori', 1699, 3.9, '09:00:00', '12:00:00', 60, 60, 'Book Now'),
        	('12360', 'Nairobi', 'Migori', 1799, 3.8, '16:30:00', '19:30:00', 60, 60, 'Book Now');




	INSERT INTO booking (booking_id, usersid, busid, passengers, date_) 
	VALUES
    	('B001', 'U001', '12345', 3, '2024-12-31'),
    	('B002', 'U002', '12346', 2, '2025-01-02');
