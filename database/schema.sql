-- 환자 테이블 (Patient Table)
CREATE TABLE IF NOT EXISTS patient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_username TEXT NOT NULL UNIQUE,
    patient_password TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    resident_registration_number TEXT NOT NULL UNIQUE,
    gender TEXT NOT NULL,
    birthday DATE NOT NULL
);

-- 의사 테이블 (Doctor Table)
CREATE TABLE IF NOT EXISTS doctor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_license_number TEXT NOT NULL UNIQUE,
    hospital_name TEXT NOT NULL,
    doctor_password TEXT NOT NULL,
    phone_number TEXT NOT NULL
);

-- 제약회사 테이블 (Pharmaceutical Company Table)
CREATE TABLE IF NOT EXISTS pharmaceutical_company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_registration_number TEXT NOT NULL UNIQUE,
    company_name TEXT NOT NULL,
    company_password TEXT NOT NULL
);

-- 관리자 테이블 (Administrator Table)
CREATE TABLE IF NOT EXISTS administrator (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_username TEXT NOT NULL UNIQUE,
    admin_password TEXT NOT NULL
);

-- 백신 종류 테이블 (Vaccine Type Table)
CREATE TABLE IF NOT EXISTS vaccine_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disease_name TEXT NOT NULL,
    is_mandatory INTEGER NOT NULL,
    gender TEXT,
    minimum_age INTEGER,
    vaccination_interval INTEGER
);

-- 백신 테이블 (Vaccine Table)
CREATE TABLE IF NOT EXISTS vaccine (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    vaccine_name TEXT NOT NULL,
    vaccine_type_id INTEGER NOT NULL,
    notes TEXT,
    FOREIGN KEY (company_id) REFERENCES pharmaceutical_company(id),
    FOREIGN KEY (vaccine_type_id) REFERENCES vaccine_type(id)
);

-- 접종 테이블 (Vaccination Table)
CREATE TABLE IF NOT EXISTS vaccination (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vaccine_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    vaccination_date DATE NOT NULL,
    FOREIGN KEY (vaccine_id) REFERENCES vaccine(id),
    FOREIGN KEY (patient_id) REFERENCES patient(id)
);