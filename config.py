import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    load_dotenv()
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    DATABASE = os.path.join(basedir, 'database', 'app.db')