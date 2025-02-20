import os

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Get from environment variable
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Get from environment variable
MAIL_DEFAULT_SENDER = ('Bus_Reservation_System', os.environ.get('MAIL_DEFAULT_SENDER'))
