import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_USER = 'root'  # Assuming 'root' is your database username
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'default_db_password')
    DB_HOST = 'localhost'
    DB_NAME = 'emotif_db'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key')
