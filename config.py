import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    DATABASE = os.path.join(basedir, 'database', 'app.db')