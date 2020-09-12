import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///insta.db"
    MONGODB_DATABASE = "instadb"
    MONGODB_USERNAME = "jrkha"
    MONGODB_PASSWORD = "JrKHa425266"
    MONGODB_PORT = ""
    MONGODB_HOST = "mongodb+srv://jrkha:JrKHa425266@instahelper-cluster.grmna.mongodb.net/instadb?retryWrites=true&w=majority"
    SECRET_KEY = "3c25743573557e402a40537afd27"
    """MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = "587"
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')"""