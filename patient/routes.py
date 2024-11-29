from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_helper import get_db
from . import patient_bp

@patient_bp.route('/register', methods=['GET', 'POST'])
def register():
    # 이미 로그인된 경우 대시보드로 리다이렉트
    if 'user_id' in session and session.get('user_type') == 'patient':
        return redirect(url_for('patient.dashboard'))

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
    # 이미 로그인된 경우 대시보드로 리다이렉트
    if 'user_id' in session and session.get('user_type') == 'patient':
        return redirect(url_for('patient.dashboard'))

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
        session['user_username'] = user['patient_name']
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

# 백신 접종 정보 조회
@patient_bp.route('/vaccination_status')
def vaccination_status():
    if 'user_id' not in session or session.get('user_type') != 'patient':
        flash('로그인이 필요합니다.')
        return redirect(url_for('patient.login'))

    db = get_db()

    # 환자 정보 가져오기
    patient = db.execute(
        'SELECT * FROM patient WHERE id = ?',
        (session['user_id'],)
    ).fetchone()

    if patient is None:
        flash('환자 정보를 찾을 수 없습니다.')
        return redirect(url_for('patient.login'))

    # 나이 계산
    from datetime import datetime, timedelta
    today = datetime.today()
    birthday = patient['birthday']
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    gender = patient['gender']

    # 환자가 맞아야 할 모든 백신 종류 조회
    vaccine_types = db.execute(
        '''
        SELECT vt.*, v.vaccination_date
        FROM vaccine_type vt
        LEFT JOIN (
            SELECT vaccination.vaccine_id, vaccination.vaccination_date
            FROM vaccination
            JOIN vaccine ON vaccination.vaccine_id = vaccine.id
            WHERE vaccination.patient_id = ?
        ) v ON vt.id = v.vaccine_id
        WHERE (vt.gender IS NULL OR vt.gender = ?)
        AND (vt.minimum_age IS NULL OR vt.minimum_age <= ?)
        ''',
        (patient['id'], gender, age)
    ).fetchall()

    vaccination_info = []
    for vt in vaccine_types:
        last_date = vt['vaccination_date']
        needs_vaccination = False
        if last_date is None:
            needs_vaccination = True
        else:
            last_date_dt = datetime.strptime(last_date.strftime('%Y-%m-%d'), '%Y-%m-%d')
            interval = vt['vaccination_interval']  # 일 수로 저장되었다고 가정
            if interval:
                next_due_date = last_date_dt + timedelta(days=interval)
                if today >= next_due_date:
                    needs_vaccination = True
            else:
                needs_vaccination = False  # 접종 주기가 없으면 1회 접종으로 간주

        vaccination_info.append({
            'disease_name': vt['disease_name'],
            'is_mandatory': vt['is_mandatory'],
            'last_vaccination_date': last_date,
            'needs_vaccination': needs_vaccination
        })

    return render_template('patient/vaccination_status.html', vaccination_info=vaccination_info)

# 백신 정보 조회
@patient_bp.route('/vaccine_info', methods=['GET', 'POST'])
def vaccine_info():
    if 'user_id' not in session or session.get('user_type') != 'patient':
        flash('로그인이 필요합니다.')
        return redirect(url_for('patient.login'))

    db = get_db()

    if request.method == 'POST':
        disease_name = request.form.get('disease_name')
        if not disease_name:
            flash('병명을 선택해주세요.')
            return redirect(url_for('patient.vaccine_info'))

        # 선택된 병명에 따른 백신 리스트 조회
        vaccines = db.execute(
            '''
            SELECT v.vaccine_name, pc.company_name, v.notes
            FROM vaccine v
            JOIN pharmaceutical_company pc ON v.company_id = pc.id
            JOIN vaccine_type vt ON v.vaccine_type_id = vt.id
            WHERE vt.disease_name = ?
            ''',
            (disease_name,)
        ).fetchall()

        return render_template('patient/vaccine_list.html', vaccines=vaccines, disease_name=disease_name)
    else:
        # 모든 백신 종류(ID, 병명) 조회
        vaccine_types = db.execute(
            'SELECT id, disease_name FROM vaccine_type'
        ).fetchall()

        return render_template('patient/vaccine_info.html', vaccine_types=vaccine_types)
