from flask import Flask, render_template, request, redirect, url_for, session, flash, logging
from werkzeug.security import generate_password_hash
import mysql.connector
import bcrypt
import os
from flask_mail import Message, Mail
import secrets

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

mail = Mail(app)

app_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'KphiL2022*',
    'database': 'bus_ticketing_system'
}

def get_db_connection():
    return mysql.connector.connect(**app_config)

def send_reset_email(email, reset_link):
    msg = Message('Password Reset Request', sender='no-reply@vukaafrica.com', recipients=[email])
    msg.body = f"To reset your password, visit the following link: {reset_link}"
    mail.send(msg)

def generate_reset_token():
    token = secrets.token_urlsafe(64)
    return token

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO users (usersid, username, email, phone, password)
            VALUES (UUID(), %s, %s, %s, %s)
            """
            cursor.execute(query, (username, email, phone, hashed_password))
            conn.commit()
            flash("Registration successful. You can now log in.")
        except mysql.connector.Error as err:
            flash(f"Database error: {err}")
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('login'))

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
                return redirect(url_for('search')) 
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
            token = generate_reset_token()
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
        flash("Invalid or expired token", "error")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_password = request.form['new_password']
        hashed_password = generate_password_hash(new_password)
        cursor.execute("UPDATE users SET password = %s, reset_token = NULL WHERE reset_token = %s", (hashed_password, token))
        conn.commit()
        
        flash("Your password has been reset. You can now log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')


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
            
            booking_query = """
            INSERT INTO booking (usersid, busid, name, phone, email, passengers)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(booking_query, (user_id, busid, username, phone, email, passengers))
            conn.commit()
            
            booking_id = cursor.lastrowid
            print(f"Booking ID: {booking_id}")
            
            return redirect(url_for('booking_confirmation', booking_id=booking_id))
        
        return render_template('booking_form.html', bus=bus, user=user)
    
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        flash("An error occurred while processing your request.")
        return redirect(url_for('search'))
    
    finally:
        cursor.close()
        conn.close()


@app.route('/booking/confirmation/<int:booking_id>')
def booking_confirmation(booking_id):
    if 'user_id' not in session:
        flash("You need to log in first.")
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        print(f"Session user_id: {session['user_id']}")
        print(f"Requested booking_id: {booking_id}")
        
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
            DATE_FORMAT(b.date_, '%Y-%m-%d %H:%i:%s') as booking_date
        FROM booking b
        JOIN bus ON b.busid = bus.busid
        WHERE b.booking_id = %s AND b.usersid = %s
        """
        
        print(f"Executing query: {query} with booking_id: {booking_id} and user_id: {session['user_id']}")
        
        cursor.execute(query, (booking_id, session['user_id']))
        booking = cursor.fetchone()
        
        if not booking:
            flash("Booking not found.")
            return redirect(url_for('search'))
        
        return render_template('booking_confirmation.html', booking=booking)
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash("An error occurred while retrieving your booking.")
        return redirect(url_for('search'))
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
