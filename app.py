from flask import Flask, current_app, g
from config import Config
from database.db_helper import get_db, close_db
from patient import patient_bp
from doctor import doctor_bp
from pharma import pharma_bp
from admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 데이터베이스 초기화
    with app.app_context():
        init_db()

    # 데이터베이스 연결 및 종료 설정
    app.teardown_appcontext(close_db)

    # 블루프린트 등록
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
    app.register_blueprint(pharma_bp, url_prefix='/pharma')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

def init_db():
    db = get_db()
    with current_app.open_resource('database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    db.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
## Render

# Registration
@app.route("/registration_doctor")
def reg_d():
    return render_template('FE/Registeration/Doctor_Registration_Form.html')

@app.route("/registration_admin")
def reg_a():
    return render_template('FE/Registeration/Administrator_Registration_Form.html')

@app.route("/registration_patient")
def reg_pat():
    return render_template('FE/Registeration/Patient_Registeration.html')

@app.route("/registration_pharm")
def reg_pha():
    return render_template('FE/Registeration/Pharmaceutical_Company_Registration_Form.html')

# Login
@app.route("/registration_pharm")
def login():
    return render_template('FE/Registeration/Multi_User_Login_Form.html')

# Patient
@app.route("/vaccine_detail_info")
def vaccine_detail_info():
    return render_template('FE/Patient/Vaccine_detail_information.html')

@app.route("/vaccine_info_query")
def vaccine_info_query():
    return render_template('FE/Patient/Vaccine_Information_Query_Page.html')

# Doctor
@app.route("/add_vaccine_rec")
def add_vaccine_rec():
    return render_template('FE/Doctor/Add_Vaccination_Record.html')

@app.route("/vaccine_rec_query")
def vaccine_rec_query():
    return render_template('FE/Doctor/Vaccination_Record_Query.html')

# Admin & Pharm
@app.route("/reg_vaccine_info")
def reg_vaccine_info():
    return render_template('FE/Admin&Pharm/Register_Vaccine_Info.html')

@app.route("/reg_vaccine_type")
def reg_vaccine_type():
    return render_template('FE/Admin&Pharm/Register_Vaccine_Type.html')