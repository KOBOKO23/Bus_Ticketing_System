from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))  # Default to 3306 if missing
}


MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Get from environment variable
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Get from environment variable
MAIL_DEFAULT_SENDER = ('Bus_Reservation_System', os.environ.get('MAIL_DEFAULT_SENDER'))
