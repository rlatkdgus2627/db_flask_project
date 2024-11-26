from flask import render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import admin_bp
from database.db_helper import get_db

@admin_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        admin_username = request.form['admin_username']
        admin_password = request.form['admin_password']
        confirm_password = request.form['confirm_password']

        if admin_password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.')
            return redirect(url_for('admin.register'))

        db = get_db()

        # 관리자 계정 아이디 중복 확인
        admin = db.execute(
            'SELECT id FROM administrator WHERE admin_username = ?',
            (admin_username,)
        ).fetchone()

        if admin is not None:
            flash('이미 존재하는 관리자 계정 아이디입니다.')
            return redirect(url_for('admin.register'))

        # 관리자 계정 생성 및 저장
        db.execute(
            'INSERT INTO administrator (admin_username, admin_password) '
            'VALUES (?, ?)',
            (admin_username, generate_password_hash(admin_password))
        )
        db.commit()
        flash('회원가입이 완료되었습니다.')
        return redirect(url_for('admin.login'))

    return render_template('admin/register.html')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        admin_username = request.form['admin_username']
        admin_password = request.form['admin_password']

        db = get_db()
        admin = db.execute(
            'SELECT * FROM administrator WHERE admin_username = ?',
            (admin_username,)
        ).fetchone()

        if admin is None or not check_password_hash(admin['admin_password'], admin_password):
            flash('관리자 계정 아이디 또는 비밀번호가 잘못되었습니다.')
            return redirect(url_for('admin.login'))

        # 로그인 성공
        session.clear()
        session['user_id'] = admin['id']
        session['user_type'] = 'admin'
        flash('로그인 성공')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/login.html')

@admin_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        flash('로그인이 필요합니다.')
        return redirect(url_for('admin.login'))

    # 대시보드 로직 구현
    return render_template('admin/dashboard.html')

# 백신 종류 추가
@admin_bp.route('/add_vaccine_type', methods=['GET', 'POST'])
def add_vaccine_type():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        flash('로그인이 필요합니다.')
        return redirect(url_for('admin.login'))

    if request.method == 'POST':
        disease_name = request.form['disease_name']
        is_mandatory = request.form.get('is_mandatory', '0')  # 체크박스
        gender = request.form['gender']
        minimum_age = request.form['minimum_age']
        vaccination_interval = request.form['vaccination_interval']

        db = get_db()

        # 백신 종류 추가
        db.execute(
            'INSERT INTO vaccine_type (disease_name, is_mandatory, gender, minimum_age, vaccination_interval) '
            'VALUES (?, ?, ?, ?, ?)',
            (disease_name, int(is_mandatory), gender or None, minimum_age or None, vaccination_interval or None)
        )
        db.commit()
        flash('백신 종류가 추가되었습니다.')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/add_vaccine_type.html')