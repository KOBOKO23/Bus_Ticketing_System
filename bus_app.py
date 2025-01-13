from flask import Flask, render_template, request, redirect, url_for, session, flash, logging
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
            flash("Registration successful. You can now log in.", "success")
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

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                session['user_id'] = user['usersid']
                session['user_name'] = user['username']
                flash("Login successful", "success")
                return redirect(url_for('search'))  # Redirect to search.html after successful login
            else:
                flash("Invalid credentials, please try again.", "danger")
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "danger")
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

        return render_template('search.html', buses=buses)

    return render_template('index.html', user_name=session.get('user_name'))

@app.route('/search', methods=["GET", "POST"])
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
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
        cursor = conn.cursor(dictionary=True)

        # Fetch bus details
        query = "SELECT * FROM bus WHERE busid = %s"
        cursor.execute(query, (busid,))
        busd = cursor.fetchone()

        if not busd:
            return render_template('error.html')

        # Get the current seat count (capacity - seats left)
        seats_left = busd['Seats Left']
        if seats_left <= 0:
            flash("No seats available.", "danger")
            return redirect(url_for('search'))  # Redirect to search if no seats are available

        # When a user clicks 'Book Now', reduce the available seats by 1
        if request.method == 'POST':
            new_seat_count = seats_left - 1  # Decrease seat count by 1
            update_query = "UPDATE bus SET `Seats Left` = %s WHERE busid = %s"
            cursor.execute(update_query, (new_seat_count, busid))
            conn.commit()  # Commit the transaction to save changes

            flash("Booking successful!", "success")
            return redirect(url_for('search'))  # Redirect back to search after booking

        # Show available seats in the booking form
        seats = [i for i in range(1, seats_left + 1)]
        return render_template('book.html', busd=busd, seats=seats)

    except Exception as e:
        logging.error(f"Error in booking route: {e}")
        flash(f"Error: {e}", "danger")
        return render_template('error.html')

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
