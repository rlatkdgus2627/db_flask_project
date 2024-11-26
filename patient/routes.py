from flask import render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import patient_bp
from database.db_helper import get_db

@patient_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        patient_username = request.form['patient_username']
        patient_password = request.form['patient_password']
        confirm_password = request.form['confirm_password']
        phone_number = request.form['phone_number']
        patient_name = request.form['patient_name']
        resident_registration_number = request.form['resident_registration_number']
        gender = request.form['gender']
        birthday = request.form['birthday']

        if patient_password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.')
            return redirect(url_for('patient.register'))

        db = get_db()

        # 아이디와 주민등록번호 중복 확인
        user = db.execute(
            'SELECT id FROM patient WHERE patient_username = ? OR resident_registration_number = ?',
            (patient_username, resident_registration_number)
        ).fetchone()

        if user is not None:
            flash('이미 존재하는 아이디 또는 주민등록번호입니다.')
            return redirect(url_for('patient.register'))

        # 사용자 생성 및 저장
        db.execute(
            'INSERT INTO patient (patient_username, patient_password, phone_number, patient_name, resident_registration_number, gender, birthday) '
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (patient_username, generate_password_hash(patient_password), phone_number, patient_name, resident_registration_number, gender, birthday)
        )
        db.commit()
        flash('회원가입이 완료되었습니다.')
        return redirect(url_for('patient.login'))

    return render_template('patient/register.html')

@patient_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        patient_username = request.form['patient_username']
        patient_password = request.form['patient_password']

        db = get_db()
        user = db.execute(
            'SELECT * FROM patient WHERE patient_username = ?',
            (patient_username,)
        ).fetchone()

        if user is None or not check_password_hash(user['patient_password'], patient_password):
            flash('아이디 또는 비밀번호가 잘못되었습니다.')
            return redirect(url_for('patient.login'))

        # 로그인 성공
        session.clear()
        session['user_id'] = user['id']
        session['user_type'] = 'patient'
        flash('로그인 성공')
        return redirect(url_for('patient.dashboard'))

    return render_template('patient/login.html')

@patient_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('user_type') != 'patient':
        flash('로그인이 필요합니다.')
        return redirect(url_for('patient.login'))

    # 대시보드 로직 구현
    return render_template('patient/dashboard.html')
