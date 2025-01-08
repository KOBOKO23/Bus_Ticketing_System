from flask import Flask, abort, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'KphiL2022*',
    'database': 'bus_ticketing_system'
}

# Register Route
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = mysql.connector.connect(**app_config)
        cursor = conn.cursor()

        query = """
        INSERT INTO users (usersid, username, email, phone, password)
        VALUES (UUID(), %s, %s, %s, %s)
        """
        cursor.execute(query, (username, email, phone, hashed_password))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        conn = mysql.connector.connect(**app_config)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user_id'] = user['usersid']
            session['user_name'] = user['username']
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password", "danger")

    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Protect the Index Route with Login
@app.route('/', methods=["GET", "POST"])
def index():
    conn = mysql.connector.connect(**app_config)
    cursor = conn.cursor()

    # Check if there are any registered users
    query = "SELECT COUNT(*) FROM users"
    cursor.execute(query)
    user_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    # Redirect to register if no users are found
    if user_count == 0:
        return redirect(url_for('register'))

    # Redirect to login if the session doesn't have a user_id
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        origin = request.form['from']
        destination = request.form['to']

        conn = mysql.connector.connect(**app_config)
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT *
        FROM bus
        WHERE origin = %s AND destination = %s
        """
        cursor.execute(query, (origin.capitalize(), destination.capitalize()))
        buses = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('result.html', buses=buses)

    return render_template('index.html', user_name=session.get('user_name'))

# Search bar for updating
@app.route('/updateid', methods=["GET", "POST"])
def update():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        record_id = request.form['id']
        
        if not record_id.isdigit():
            return "Invalid ID format",
        return redirect(f"/change/{record_id}")
    
    return render_template('updateid.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
