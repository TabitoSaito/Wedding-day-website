import os

class Config:
    """Main config for Flask app
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///../instance/data.db')
    SECRET_KEY_REGISTER = os.environ.get("SECRET_KEY_REGISTER", "admin")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    """config for development environment

    Args:
        Config (_type_): base config object
    """
    DEBUG = True

class ProdConfig(Config):
    """config for production environment

    Args:
        Config (_type_): base config object
    """
    DEBUG = False