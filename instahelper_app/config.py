import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///insta.db"
    SECRET_KEY = "3c25743573557e402a40537afd27"
    """MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = "587"
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')"""