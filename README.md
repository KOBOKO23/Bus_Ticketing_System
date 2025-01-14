```python
# Bus Ticketing System

## Overview

The Bus Ticketing System is a web application built using the Flask web framework and MySQL as the database. This MVP allows users to:
- Register an account
- Log in to their profiles
- Book tickets for travel
- Perform CRUD operations on their user profiles
- View the history of their bookings
- Receive notifications each time they book a ticket, cancel a booking, or update their details

## Features


- **User Registration**: Users can create an account by providing their details (username, email, phone number, etc.).
- **User Login**: Users can securely log in using their credentials (email and password).
- **CRUD Operations on User Profiles**: Users can create, read, update, and delete their profile details.
- **Booking Tickets**: Users can book tickets, choose the origin, destination, and departure time, and view available buses.
- **Booking History**: Users can view their previous bookings and manage them.
- **Notifications**: Notifications are sent to users when they book, cancel, or update their bookings.
- **Admin Panel**: Admins can manage buses, view bookings, and update ticket information.

## Technologies Used

- **Backend**: Flask (Python Web Framework)
- **Database**: MySQL
- **MySQL Connector**: To interact with the MySQL database
- **HTML, CSS**: For front-end layout and design

## Project Structure

The project has the following structure:

```
Bus_Reservation_System/
│
├── bus_app.py           # Main Flask application
├── config.py            # Configuration settings
├── queries.sql          # SQL queries for creating tables and inserting data
├── static/              # Static files (CSS, JS, Images)
├── templates/           # HTML templates for rendering views
│
└── .git/                # Git repository for version control
```

- **bus_app.py**: This is the main Flask application file where all routes, views, and logic are handled.
- **config.py**: Contains configuration details like MySQL connection parameters.
- **queries.sql**: Contains SQL queries for creating tables, inserting data, etc.
- **static/**: Stores all static files such as CSS, JavaScript, and images.
- **templates/**: Stores HTML files for rendering the views, such as registration, login, and ticket booking pages.

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd Bus_Reservation_System
   ```

2. **Install dependencies**:
   Make sure you have Python 3 installed, then install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL Database**:
   - Create a MySQL database (e.g., `bus_ticketing`).
   - Run the queries from the `queries.sql` file to set up the necessary tables in the database.

4. **Configure Database Connection**:
   Update `config.py` with your MySQL database credentials:
   ```python
   MYSQL_HOST = 'localhost'
   MYSQL_USER = 'your_mysql_user'
   MYSQL_PASSWORD = 'your_mysql_password'
   MYSQL_DB = 'bus_ticketing'
   ```

5. **Run the Flask Application**:
   After setting up the database and configuration, run the Flask app:
   ```bash
   python bus_app.py
   ```

   The application will start running on the default Flask port (usually `http://127.0.0.1:5000/`).

## Usage

### User Registration
- Visit the registration page to create an account by providing the required information.
  
### User Login
- After registering, log in with your email and password to access your profile and book tickets.

### Booking Tickets
- Once logged in, you can book tickets for travel by choosing the origin, destination, and departure time.

### View and Manage Bookings
- Users can view their booking history, and cancel or update tickets as needed.

### User Profile Management
- You can view and update your profile details, including name, phone number, and address.

### Notifications
- Each time you book, cancel, or update your booking, you will receive a notification.

## SQL Queries

The database tables are created using the `queries.sql` file. This file contains queries for:
- Creating the `users` table for user information.
- Creating the `bus` table for bus routes.
- Creating the `booking` table to store user bookings.

## Testing

To test the system, ensure you have:
- Registered and logged in successfully.
- Created some bookings and checked the booking history.
- Tested CRUD operations on the user profile.
- Verified the notifications are triggered correctly during booking actions.

## Contributing

If you'd like to contribute to the development of this Bus Ticketing System, feel free to fork the repository, make changes, and create a pull request. Your contributions will be highly appreciated.

## License

This project is open-source and available under the [MIT License](LICENSE).
```
