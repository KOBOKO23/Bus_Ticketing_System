from flask import Flask, abort, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import mysql.connector
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

app_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'KphiL2022*',
    'database': 'bus_ticketing_system'
}

def get_db_connection():
    return mysql.connector.connect(**app_config)

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
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "danger")
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
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "danger")
            return redirect(url_for('login'))
        finally:
            cursor.close()
            conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user_id'] = user['usersid']
            session['user_name'] = user['username']
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash("You have successfully logged out.", "success")
    return redirect(url_for('login'))

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
        flash(f"Database error: {err}", "danger")
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
            flash(f"Database error: {err}", "danger")
            return redirect(url_for('index'))
        finally:
            cursor.close()
            conn.close()

        return render_template('result.html', buses=buses)

    return render_template('index.html', user_name=session.get('user_name'))

@app.route('/updateid', methods=["GET", "POST"])
def update():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        record_id = request.form['id']
        if not record_id.isdigit():
            flash("Invalid ID format.", "danger")
            return redirect(url_for('update'))
        return redirect(f"/change/{record_id}")

    return render_template('updateid.html')

@app.route('/booked/<busid>', methods=["POST"])
def booked(busid):
    if 'user_id' not in session:
        flash("Please log in to book a ticket.", "danger")
        return redirect(url_for('login'))

    passengers = request.form.get('num_passengers')
    user_id = session['user_id']
    user_name = session['user_name']

    if not passengers.isdigit() or int(passengers) <= 0:
        flash("Invalid number of passengers.", "danger")
        return redirect(url_for('index'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM bus WHERE busid = %s"
        cursor.execute(query, (busid,))
        if cursor.fetchone()[0] == 0:
            flash("Invalid bus ID.", "danger")
            return redirect(url_for('index'))

        query = """
        INSERT INTO bookings (bookingid, userid, busid, passengers)
        VALUES (UUID(), %s, %s, %s)
        """
        cursor.execute(query, (user_id, busid, passengers))
        conn.commit()
    except mysql.connector.Error as err:
        flash(f"Database error: {err}", "danger")
        return redirect(url_for('index'))
    finally:
        cursor.close()
        conn.close()

    flash(f"Thank you, {user_name}, your booking for bus {busid} is confirmed!", "success")
    return render_template('booked.html', user_name=user_name, busid=busid, passengers=passengers)

@app.route('/confirmation/<booking_id>')
def confirmation(booking_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM bookings WHERE bookingid = %s"
        cursor.execute(query, (booking_id,))
        booking = cursor.fetchone()

        if not booking:
            abort(404)
    except mysql.connector.Error as err:
        flash(f"Database error: {err}", "danger")
    finally:
        cursor.close()
        conn.close()

    return render_template('confirmation.html', booking=booking)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
