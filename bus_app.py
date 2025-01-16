from flask import Flask, render_template, request, redirect, url_for, session, flash, logging
from werkzeug.security import generate_password_hash
import mysql.connector
import bcrypt
import os
from flask_mail import Message, Mail
import secrets
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import SignatureExpired, BadData
from email_validator import validate_email, EmailNotValidError  

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

mail = Mail(app)

app_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'KphiL2022*',
    'database': 'bus_ticketing_system'
}

def generate_ticket(booking):
    pdf_file = f"ticket_{booking['booking_id']}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)

    c.drawString(100, 750, f"Booking ID: {booking['booking_id']}")
    c.drawString(100, 730, f"Passenger Name: {booking['name']}")
    c.drawString(100, 710, f"Phone: {booking['phone']}")
    c.drawString(100, 690, f"Email: {booking['email']}")
    c.drawString(100, 670, f"From: {booking['origin']}")
    c.drawString(100, 650, f"To: {booking['destination']}")
    c.drawString(100, 630, f"Departure: {booking['departure']}")
    c.drawString(100, 610, f"Arrival: {booking['arrival']}")
    c.drawString(100, 590, f"Total Cost: {booking['cost']}")

    c.save()

    return pdf_file

def get_db_connection():
    return mysql.connector.connect(**app_config)


def send_reset_email(email, reset_link):
    msg = Message('Password Reset Request', sender='no-reply@vukaafrica.com', recipients=[email])
    msg.body = f"To reset your password, visit the following link: {reset_link}"
    mail.send(msg)

def generate_reset_token(email):
    s = Serializer(app.config['SECRET_KEY'], salt='password-reset')
    return s.dumps({'email': email})

def verify_reset_token(token, expiration=3600):
    s = Serializer(app.config['SECRET_KEY'], salt='password-reset')
    try:
        # This will raise an exception if the token is invalid or expired
        email = s.loads(token, max_age=expiration)['email']
    except SignatureExpired:
        # Token has expired
        return None
    except BadData:
        # Invalid token
        return None
    return email

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username', 'Not provided')
        email = request.form['email']
        phone = request.form.get('phone', 'Not provided')
        password = request.form['password']
        other_names = request.form.get('other_names', 'Not provided')
        physical_address = request.form.get('physical_address', 'Not provided') 
        next_of_kin = request.form.get('next_of_kin', 'Not provided') 

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check for duplicate email
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("Email is already registered. Please use a different email.")
                return redirect(url_for('register'))

            # Insert new user into the database
            query = """
            INSERT INTO users (usersid, username, email, phone, password, other_names, physical_address, next_of_kin)
            VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (username, email, phone, hashed_password, other_names, physical_address, next_of_kin))
            conn.commit()

            flash("Registration successful. You can now log in.")
            return redirect(url_for('login'))

        except mysql.connector.IntegrityError:
            flash("Registration failed. Email might already be in use.")
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "danger")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                session['user_id'] = user['usersid']
                session['user_name'] = user['username']
                return redirect(url_for('profile'))
            else:
                flash("Invalid credentials, please try again.")
        except mysql.connector.Error as err:
            flash(f"Database error: {err}")
        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash("You have successfully logged out.")
    return redirect(url_for('login'))


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            token = generate_reset_token(email)  # Pass email here
            cursor.execute("UPDATE users SET reset_token = %s WHERE email = %s", (token, email))
            conn.commit()
            
            reset_link = url_for('reset_password', token=token, _external=True)
            send_reset_email(email, reset_link)
            
            flash("Password reset link sent to your email", "success")
            return redirect(url_for('login'))
        else:
            flash("Email not found", "error")
    
    return render_template('forgot_password.html')
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE reset_token = %s", (token,))
    user = cursor.fetchone()
    
    if not user:
        flash("Invalid or expired token")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_password = request.form['new_password']
        hashed_password = generate_password_hash(new_password)
        cursor.execute("UPDATE users SET password = %s, reset_token = NULL WHERE reset_token = %s", (hashed_password, token))
        conn.commit()
        
        flash("Your password has been reset. You can now log in.")
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash("You need to log in first.")
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE usersid = %s LIMIT 1"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        if not user:
            flash("User not found.")
            return redirect(url_for('login'))

        # Debugging: print user data
        print(f"User data fetched: {user}")  # This will help track if user data is correct

        # Ensure all user fields have default values if missing
        user['surname'] = user.get('surname', 'Not provided')
        user['other_names'] = user.get('other_names', 'Not provided')
        user['email'] = user.get('email', 'Not provided')
        user['phone'] = user.get('phone', 'Not provided')
        user['physical_address'] = user.get('physical_address', 'Not provided')
        user['next_of_kin'] = user.get('next_of_kin', 'Not provided')

        # Debugging: print session data
        print(f"Session data: {session}") 

        return render_template('profile.html', user=user)
    
    except mysql.connector.Error as err:
        flash(f"Database error: {err}")
        return redirect(url_for('login'))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash("You need to log in first.")
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch the current user details
        query = "SELECT * FROM users WHERE usersid = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        if not user:
            flash("User not found.")
            return redirect(url_for('login'))

        if request.method == 'POST':
            # Get updated profile data from the form
            username = request.form['username']
            other_names = request.form['other_names']
            email = request.form['email']
            phone = request.form['phone']
            physical_address = request.form['physical_address']
            next_of_kin = request.form['next_of_kin']
            password = request.form.get('password')  # Get password if provided

            # If password is provided, hash it (make sure to define a hashing function like bcrypt)
            if password:
                password = hash_password(password)  # Replace with actual password hashing function

            # Update the user profile in the database
            update_query = """
                UPDATE users
                SET username = %s, other_names = %s, email = %s, phone = %s, 
                    physical_address = %s, next_of_kin = %s
            """
            
            # If password was provided, include it in the update query
            if password:
                update_query += ", password = %s"
                cursor.execute(update_query + " WHERE usersid = %s", 
                               (username, other_names, email, phone, physical_address, next_of_kin, password, user_id))
            else:
                cursor.execute(update_query + " WHERE usersid = %s", 
                               (username, other_names, email, phone, physical_address, next_of_kin, user_id))
            
            conn.commit()
            flash("Profile updated successfully!")
            return redirect(url_for('profile'))  # After updating, redirect to the profile page

        return render_template('edit_profile.html', user=user)

    except mysql.connector.Error as err:
        flash(f"Database error: {err}")
        return redirect(url_for('login'))

    finally:
        cursor.close()
        conn.close()


@app.route('/', methods=["GET", "POST"])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM users"
        cursor.execute(query)
        user_count = cursor.fetchone()[0]

        if user_count == 0:
            return redirect(url_for('register'))
    except mysql.connector.Error as err:
        flash(f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

    if request.method == "POST":
        origin = request.form['from']
        destination = request.form['to']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT *
            FROM bus
            WHERE origin = %s AND destination = %s
            """
            cursor.execute(query, (origin.capitalize(), destination.capitalize()))
            buses = cursor.fetchall()
        except mysql.connector.Error as err:
            flash(f"Database error: {err}")
            return redirect(url_for('index'))
        finally:
            cursor.close()
            conn.close()

        return render_template('search.html', buses=buses)

    return render_template('index.html', user_name=session.get('user_name'))

@app.route('/search', methods=["GET", "POST"])
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    origin = request.form.get('origin')
    destination = request.form.get('destination')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if origin and destination:
            query = "SELECT * FROM bus WHERE origin LIKE %s AND destination LIKE %s"
            cursor.execute(query, (f"%{origin}%", f"%{destination}%"))
        else:
            query = "SELECT * FROM bus"
            cursor.execute(query)

        buses = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Database error: {err}")
        return redirect(url_for('search'))
    finally:
        cursor.close()
        conn.close()

    return render_template('search.html', det=buses)


@app.route('/book/<int:busid>', methods=['GET', 'POST'])
def book(busid):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Fetch bus details
        query = "SELECT busid, origin, destination, cost, seats_left, departure, arrival FROM bus WHERE busid = %s"
        cursor.execute(query, (busid,))
        bus = cursor.fetchone()
        
        if not bus:
            flash("Bus not found.")
            return redirect(url_for('search'))
        
        seats_left = bus[4]
        
        if 'user_id' not in session:
            flash("You need to log in first.")
            return redirect(url_for('login'))
        
        user_id = session['user_id']
        user_query = "SELECT username, phone, email FROM users WHERE usersid = %s"
        cursor.execute(user_query, (user_id,))
        user = cursor.fetchone()
        
        if not user:
            flash("User not found.")
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            username = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            passengers = int(request.form['passengers'])
            
            if passengers > seats_left:
                flash("Not enough seats available.")
                return redirect(url_for('book', busid=busid))
            
            updated_seats = seats_left - passengers
            update_query = "UPDATE bus SET seats_left = %s WHERE busid = %s"
            cursor.execute(update_query, (updated_seats, busid))
            
            # Allocate seats for each passenger
            for seat_number in range(1, passengers + 1):
                # Find the lowest available seat number for the current bus
                seat_query = """
                SELECT seat_number FROM booking WHERE busid = %s ORDER BY seat_number ASC
                """
                cursor.execute(seat_query, (busid,))
                booked_seats = cursor.fetchall()
                
                # Find the first available seat number that is not taken
                new_seat_number = 1
                for booked_seat in booked_seats:
                    if booked_seat[0] != new_seat_number:
                        break
                    new_seat_number += 1

                # Insert the booking with the allocated seat number
                booking_query = """
                INSERT INTO booking (usersid, busid, name, phone, email, passengers, seat_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(booking_query, (user_id, busid, username, phone, email, 1, new_seat_number))
            
            conn.commit()
            
            # Get the first booking ID of the first passenger's booking
            booking_id = cursor.lastrowid
            print(f"Booking ID: {booking_id}")
            
            return redirect(url_for('booking_confirmation', booking_id=booking_id))
        
        # Format the bus date
        if isinstance(bus[5], datetime):
            bus_date = bus[5].strftime('%Y-%m-%d')
        elif isinstance(bus[5], timedelta):
            bus_date = (datetime.now() + bus[5]).strftime('%Y-%m-%d')
        else:
            bus_date = None
        
        return render_template('booking_form.html', bus=bus, user=user, bus_date=bus_date)
    
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        flash("An error occurred while processing your request.")
        return redirect(url_for('search'))
    
    finally:
        cursor.close()
        conn.close()


@app.route('/booking_confirmation/<int:booking_id>', methods=['GET'])
def booking_confirmation(booking_id):
    try:
        print(f"Booking ID: {booking_id}")
        print(f"Session user_id: {session.get('user_id')}")
        print(f"Session content: {session}")
        
        query = """
            SELECT 
                b.booking_id,
                b.name,
                b.phone,
                b.email,
                b.passengers,
                bus.origin,
                bus.destination,
                bus.departure,
                bus.arrival,
                bus.cost,
                DATE_FORMAT(b.date_, '%%Y-%%m-%%d %%H:%%i:%%s') as booking_date
            FROM booking b
            JOIN bus ON b.busid = bus.busid
            WHERE b.booking_id = %(booking_id)s AND b.usersid = %(user_id)s
        """
        
        print(f"Executing query with parameters: booking_id={booking_id}, user_id={session.get('user_id')}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, {'booking_id': booking_id, 'user_id': session.get('user_id')})
        bookings = cursor.fetchall()
        
        if not bookings:
            flash("No booking found.")
            return redirect(url_for('search'))
        
        booking = bookings[0]
        return render_template('booking_confirmation.html', booking=booking)
    
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        flash("An error occurred while processing your request.")
        return redirect(url_for('search'))
    
    finally:
        cursor.close()
        conn.close()


@app.route('/user/bookings', methods=['GET'])
def user_bookings():
    if 'user_id' not in session:
        flash("You need to log in first.")
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        booking_query = """
        SELECT 
            booking_id, busid, name, passengers, date_, phone, email, created_at
        FROM 
            booking
        WHERE 
            usersid = %s
        ORDER BY 
            created_at DESC
        """
        cursor.execute(query, (booking_id, user_id))
        bookings = cursor.fetchall()
        
        return render_template('user_bookings.html', bookings=bookings)
    
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        flash("An error occurred while retrieving booking history.")
        return redirect(url_for('search'))
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
