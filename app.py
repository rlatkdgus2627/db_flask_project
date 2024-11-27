from flask import Flask, current_app, render_template, request, jsonify
from config import Config
from database.db_helper import get_db, close_db
from patient import patient_bp
from doctor import doctor_bp
from pharma import pharma_bp
from admin import admin_bp

app = Flask(__name__)

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # 데이터베이스 초기화
#     with app.app_context():
#         init_db()

#     # 데이터베이스 연결 및 종료 설정
#     app.teardown_appcontext(close_db)

#     # 블루프린트 등록
#     app.register_blueprint(patient_bp, url_prefix='/patient')
#     app.register_blueprint(doctor_bp, url_prefix='/doctor')
#     app.register_blueprint(pharma_bp, url_prefix='/pharma')
#     app.register_blueprint(admin_bp, url_prefix='/admin')

#     return app

# def init_db():
#     db = get_db()
#     with current_app.open_resource('database/schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))
#     db.commit()

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)

## Render

@app.route("/")
def hello():
    return "Hello World!"

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
@app.route("/login")
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


## Interact

# Login
@app.route('/login_json', methods=['POST'])
def login_json():
    data = request.get_json()
    #print('Received data:', data)
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 200

    user_type = data.get('user-type')
    user_id = data.get('user-id')
    password = data.get('password')
    
    #print(f'user_type: {user_type}, user_id: {user_id}, password: {password}')

    # 이 부분은 로그인 시킬지 말지 결정 -> 로그인 성공하면 성공.json 날라가고, else면 실패.json날라감
    if user_type == 'doctor' and user_id == 'example' and password == '1234':
        return jsonify({"status": "success", "user_type": "doctor", "message": "Login successful"}), 200
    elif user_type == 'patient' and user_id == 'example' and password == '1234':
        return jsonify({"status": "success", "user_type": "patient", "message": "Login successful"}), 200
    elif user_type == 'pharma' and user_id == 'example' and password == '1234':
        return jsonify({"status": "success", "user_type": "pharma", "message": "Login successful"}), 200
    elif user_type == 'admin' and user_id == 'example' and password == '1234':
        return jsonify({"status": "success", "user_type": "admin", "message": "Login successful"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 200

if __name__ == '__main__':
    app.run(debug=True)
