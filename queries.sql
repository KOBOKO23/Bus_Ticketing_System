
	CREATE TABLE IF NOT EXISTS bus (
            busid VARCHAR(20) PRIMARY KEY,
            origin VARCHAR(50) NOT NULL,
            destination VARCHAR(50) NOT NULL,
            cost INT NOT NULL,
            rating DECIMAL(3, 2) NOT NULL,
            departure DATETIME NOT NULL,
            capacity INT NOT NULL DEFAULT 60,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );


	CREATE TABLE IF NOT EXISTS booking (
    	booking_id VARCHAR(20) PRIMARY KEY,
    	usersid VARCHAR(255) NOT NULL,
    	busid VARCHAR(20) NOT NULL,
    	passengers INT NOT NULL,
    	date_ DATE NOT NULL,
    	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    	FOREIGN KEY (usersid) REFERENCES users(usersid) ON DELETE CASCADE,
    	FOREIGN KEY (busid) REFERENCES bus(busid) ON DELETE CASCADE
	);

 	CREATE TABLE IF NOT EXISTS users (
    	usersid VARCHAR(255) PRIMARY KEY,
    	username VARCHAR(100) NOT NULL,
    	phone_number VARCHAR(20) NOT NULL,
    	email VARCHAR(50) NOT NULL UNIQUE,
    	password VARCHAR(255) NOT NULL,  -- Add the password field with appropriate size
    	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
	);

