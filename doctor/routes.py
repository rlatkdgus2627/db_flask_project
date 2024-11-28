from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_helper import get_db
from . import doctor_bp

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

# 접종 이력 추가
@doctor_bp.route('/add_vaccination', methods=['GET', 'POST'])
def add_vaccination():
    if 'user_id' not in session or session.get('user_type') != 'doctor':
        flash('로그인이 필요합니다.')
        return redirect(url_for('doctor.login'))

    db = get_db()

    if request.method == 'POST':
        vaccine_id = request.form['vaccine_id']
        patient_name = request.form['patient_name']
        resident_registration_number = request.form['resident_registration_number']
        vaccination_date = request.form['vaccination_date']

        # 환자 정보 확인
        patient = db.execute(
            'SELECT * FROM patient WHERE patient_name = ? AND resident_registration_number = ?',
            (patient_name, resident_registration_number)
        ).fetchone()

        if patient is None:
            flash('해당 환자를 찾을 수 없습니다.')
            return redirect(url_for('doctor.add_vaccination'))

        # 백신 정보 확인
        vaccine = db.execute(
            'SELECT * FROM vaccine WHERE id = ?',
            (vaccine_id,)
        ).fetchone()

        if vaccine is None:
            flash('선택한 백신이 존재하지 않습니다.')
            return redirect(url_for('doctor.add_vaccination'))

        # 접종 정보 등록
        db.execute(
            'INSERT INTO vaccination (vaccine_id, patient_id, vaccination_date) '
            'VALUES (?, ?, ?)',
            (vaccine_id, patient['id'], vaccination_date)
        )
        db.commit()
        flash('접종 이력이 추가되었습니다.')
        return redirect(url_for('doctor.dashboard'))

    else:
        # 백신 종류에 따른 백신 리스트 출력
        vaccine_types = db.execute(
            'SELECT id, disease_name FROM vaccine_type'
        ).fetchall()

        return render_template('doctor/add_vaccination.html', vaccine_types=vaccine_types)

# 접종 이력 조회
@doctor_bp.route('/view_vaccination', methods=['GET', 'POST'])
def view_vaccination():
    if 'user_id' not in session or session.get('user_type') != 'doctor':
        flash('로그인이 필요합니다.')
        return redirect(url_for('doctor.login'))

    db = get_db()

    if request.method == 'POST':
        patient_name = request.form['patient_name']
        resident_registration_number = request.form['resident_registration_number']

        # 환자 정보 확인
        patient = db.execute(
            'SELECT * FROM patient WHERE patient_name = ? AND resident_registration_number = ?',
            (patient_name, resident_registration_number)
        ).fetchone()

        if patient is None:
            flash('해당 환자를 찾을 수 없습니다.')
            return redirect(url_for('doctor.view_vaccination'))

        # 접종 이력 조회
        records = db.execute(
            '''
            SELECT vaccination.vaccination_date, vaccine.vaccine_name, vaccine_type.disease_name
            FROM vaccination
            JOIN vaccine ON vaccination.vaccine_id = vaccine.id
            JOIN vaccine_type ON vaccine.vaccine_type_id = vaccine_type.id
            WHERE vaccination.patient_id = ?
            ORDER BY vaccination.vaccination_date DESC
            LIMIT 10
            ''',
            (patient['id'],)
        ).fetchall()

        return render_template('doctor/view_vaccination.html', records=records, patient=patient)

    return render_template('doctor/view_vaccination.html', records=[], patient=None)
