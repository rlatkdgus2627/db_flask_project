from flask import render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import doctor_bp
from database.db_helper import get_db

@doctor_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        doctor_license_number = request.form['doctor_license_number']
        hospital_name = request.form['hospital_name']
        doctor_password = request.form['doctor_password']
        confirm_password = request.form['confirm_password']
        phone_number = request.form['phone_number']

        if doctor_password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.')
            return redirect(url_for('doctor.register'))

        db = get_db()

        # 의사 면허 ID 중복 확인
        doctor = db.execute(
            'SELECT id FROM doctor WHERE doctor_license_number = ?',
            (doctor_license_number,)
        ).fetchone()

        if doctor is not None:
            flash('이미 존재하는 의사 면허 ID입니다.')
            return redirect(url_for('doctor.register'))

        # 의사 계정 생성 및 저장
        db.execute(
            'INSERT INTO doctor (doctor_license_number, hospital_name, doctor_password, phone_number) '
            'VALUES (?, ?, ?, ?)',
            (doctor_license_number, hospital_name, generate_password_hash(doctor_password), phone_number)
        )
        db.commit()
        flash('회원가입이 완료되었습니다.')
        return redirect(url_for('doctor.login'))

    return render_template('doctor/register.html')

@doctor_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        doctor_license_number = request.form['doctor_license_number']
        doctor_password = request.form['doctor_password']

        db = get_db()
        doctor = db.execute(
            'SELECT * FROM doctor WHERE doctor_license_number = ?',
            (doctor_license_number,)
        ).fetchone()

        if doctor is None or not check_password_hash(doctor['doctor_password'], doctor_password):
            flash('의사 면허 ID 또는 비밀번호가 잘못되었습니다.')
            return redirect(url_for('doctor.login'))

        # 로그인 성공
        session.clear()
        session['user_id'] = doctor['id']
        session['user_type'] = 'doctor'
        flash('로그인 성공')
        return redirect(url_for('doctor.dashboard'))

    return render_template('doctor/login.html')

@doctor_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('user_type') != 'doctor':
        flash('로그인이 필요합니다.')
        return redirect(url_for('doctor.login'))

    # 대시보드 로직 구현
    return render_template('doctor/dashboard.html')