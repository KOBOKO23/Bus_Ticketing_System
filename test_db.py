import pymysql
import os

# Database configuration
app_config = {
    'host': os.getenv('DB_HOST', 'caboose.proxy.rlwy.net'),  # Railway MySQL Host
    'user': os.getenv('DB_USER', 'root'),  # Railway MySQL User
    'password': os.getenv('DB_PASSWORD', 'KphiL2022*'),  # Railway MySQL Password
    'database': os.getenv('DB_NAME', 'bus_ticketing_system'),  # Railway Database Name
    'port': int(os.getenv('DB_PORT', 28786))  # Railway MySQL Port
}

# Try connecting to the database
try:
    connection = pymysql.connect(
        host=app_config['host'],
        user=app_config['user'],
        password=app_config['password'],
        database=app_config['database'],
        port=app_config['port']
    )
    print("✅ Successfully connected to MySQL!")

    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        print("📌 Tables in the database:")
        for table in tables:
            print(table[0])

except pymysql.MySQLError as e:
    print("❌ Connection failed:", e)

finally:
    if 'connection' in locals():
        connection.close()
        print("🔌 Connection closed.")
