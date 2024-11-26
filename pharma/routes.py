from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_helper import get_db

pharma_bp = Blueprint('pharma', __name__, url_prefix='/pharma')

@pharma_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        business_registration_number = request.form['business_registration_number']
        company_name = request.form['company_name']
        company_password = request.form['company_password']
        confirm_password = request.form['confirm_password']

        if company_password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.')
            return redirect(url_for('pharma.register'))

        db = get_db()

        # 사업자 등록 번호 중복 확인
        company = db.execute(
            'SELECT id FROM pharmaceutical_company WHERE business_registration_number = ?',
            (business_registration_number,)
        ).fetchone()

        if company is not None:
            flash('이미 존재하는 사업자 등록 번호입니다.')
            return redirect(url_for('pharma.register'))

        # 제약회사 계정 생성 및 저장
        db.execute(
            'INSERT INTO pharmaceutical_company (business_registration_number, company_name, company_password) '
            'VALUES (?, ?, ?)',
            (business_registration_number, company_name, generate_password_hash(company_password))
        )
        db.commit()
        flash('회원가입이 완료되었습니다.')
        return redirect(url_for('pharma.login'))

    return render_template('pharma/register.html')

@pharma_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        business_registration_number = request.form['business_registration_number']
        company_password = request.form['company_password']

        db = get_db()
        company = db.execute(
            'SELECT * FROM pharmaceutical_company WHERE business_registration_number = ?',
            (business_registration_number,)
        ).fetchone()

        if company is None or not check_password_hash(company['company_password'], company_password):
            flash('사업자 등록 번호 또는 비밀번호가 잘못되었습니다.')
            return redirect(url_for('pharma.login'))

        # 로그인 성공
        session.clear()
        session['user_id'] = company['id']
        session['user_type'] = 'pharma'
        flash('로그인 성공')
        return redirect(url_for('pharma.dashboard'))

    return render_template('pharma/login.html')

@pharma_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('user_type') != 'pharma':
        flash('로그인이 필요합니다.')
        return redirect(url_for('pharma.login'))

    # 대시보드 로직 구현
    return render_template('pharma/dashboard.html')

# 백신 정보 등록
@pharma_bp.route('/add_vaccine', methods=['GET', 'POST'])
def add_vaccine():
    if 'user_id' not in session or session.get('user_type') != 'pharma':
        flash('로그인이 필요합니다.')
        return redirect(url_for('pharma.login'))

    db = get_db()

    if request.method == 'POST':
        vaccine_type_id = request.form['vaccine_type_id']
        vaccine_name = request.form['vaccine_name']
        notes = request.form['notes']

        # 백신 종류 확인
        vaccine_type = db.execute(
            'SELECT id FROM vaccine_type WHERE id = ?',
            (vaccine_type_id,)
        ).fetchone()

        if vaccine_type is None:
            flash('유효하지 않은 백신 종류입니다.')
            return redirect(url_for('pharma.add_vaccine'))

        # 백신 정보 추가
        db.execute(
            'INSERT INTO vaccine (company_id, vaccine_name, vaccine_type_id, notes) '
            'VALUES (?, ?, ?, ?)',
            (session['user_id'], vaccine_name, vaccine_type_id, notes)
        )
        db.commit()
        flash('백신 정보가 등록되었습니다.')
        return redirect(url_for('pharma.dashboard'))

    # 모든 백신 종류(ID, 병명) 조회
    vaccine_types = db.execute(
        'SELECT id, disease_name FROM vaccine_type'
    ).fetchall()

    return render_template('pharma/add_vaccine.html', vaccine_types=vaccine_types)
