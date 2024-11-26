from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

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
