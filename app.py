from flask import Flask, render_template, redirect, url_for, session, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_helper import get_db
from patient import patient_bp
from doctor import doctor_bp
from pharma import pharma_bp
from admin import admin_bp
from config import Config
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv(override=True)  # 기존 환경 변수 덮어쓰기

# 환경 변수 가져오기
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

# Flask 설정에 추가
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

print(SECRET_KEY)

def init_db():
    db = get_db()
    with current_app.open_resource('database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    db.commit()

app.config.from_object(Config)

# 데이터베이스 초기화
with app.app_context():
    init_db()

# Register blueprints
app.register_blueprint(patient_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(pharma_bp)
app.register_blueprint(admin_bp)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
