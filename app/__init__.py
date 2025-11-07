from flask import Flask
import locale
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv

from .extensions import db, login_manager
from .models import User

def create_app(config_class='app.config.Config') -> Flask:
    """create app. Initialise database, login manager and bootstrap5. Add blueprints

    Args:
        config_class (str, optional): configuration class containing app settings. Defaults to 'app.config.Config'.

    Returns:
        Flask: app to run webserver
    """
    load_dotenv()
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

    # create app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_pyfile('config.py', silent=True)

    # initialise
    db.init_app(app)
    login_manager.init_app(app)
    Bootstrap5(app)

    # create database
    with app.app_context():
        db.create_all()

    # create user loader
    @login_manager.user_loader
    def load_user(user_id):
        return db.get_or_404(User, user_id)

    # register blueprints
    from .blueprints.main import main_bp
    from .blueprints.auth import auth_bp
    from .blueprints.comments import comment_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(comment_bp)
    return app