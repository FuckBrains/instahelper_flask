from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from instahelper_app.config import Config



login_manager = LoginManager()
mail = Mail()

bcrypt = Bcrypt()

login_manager.login_view = "panel.login"
login_manager.login_message_category = "info"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from instahelper_app.panel.routes import panel
    from instahelper_app.main.routes import main
    app.register_blueprint(panel, url_prefix='/panel')
    app.register_blueprint(main)
    
    
    login_manager.init_app(app)
    mail.init_app(app)

    bcrypt.init_app(app)

    return app