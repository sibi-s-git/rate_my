import os

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev_db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig:
    TESTING = True
    SECRET_KEY = os.getenv("SECRET_KEY", "test_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///test_db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "prod_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///prod_db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
