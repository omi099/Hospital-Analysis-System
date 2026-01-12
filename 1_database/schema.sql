-- =============================================
-- HOSPITAL MANAGEMENT SYSTEM DATABASE
-- Complete Schema + Sample Data
-- =============================================

CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

-- Departments
CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(100) NOT NULL,
    floor_number INT,
    phone_extension VARCHAR(10)
);

-- Doctors
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    specialization VARCHAR(100),
    department_id INT,
    experience_years INT,
    consultation_fee DECIMAL(10,2),
    hire_date DATE,
    status ENUM('Active','Inactive','On Leave') DEFAULT 'Active',
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Patients
CREATE TABLE patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male','Female','Other'),
    blood_group VARCHAR(5),
    phone VARCHAR(15),
    email VARCHAR(100),
    address VARCHAR(255),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(15),
    registration_date DATE,
    status ENUM('Active','Inactive') DEFAULT 'Active'
);

-- Appointments
CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    appointment_type ENUM('Consultation','Follow-up','Emergency','Routine Checkup'),
    status ENUM('Scheduled','Completed','Cancelled','No Show') DEFAULT 'Scheduled',
    symptoms TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- Medical Records
CREATE TABLE medical_records (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_id INT,
    diagnosis VARCHAR(255),
    treatment TEXT,
    prescription TEXT,
    blood_pressure VARCHAR(20),
    heart_rate INT,
    temperature DECIMAL(4,1),
    weight DECIMAL(5,2),
    record_date DATE NOT NULL,
    follow_up_date DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
);

-- Wards
CREATE TABLE wards (
    ward_id INT PRIMARY KEY AUTO_INCREMENT,
    ward_name VARCHAR(50) NOT NULL,
    department_id INT,
    floor_number INT,
    total_beds INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Beds
CREATE TABLE beds (
    bed_id INT PRIMARY KEY AUTO_INCREMENT,
    ward_id INT NOT NULL,
    bed_number VARCHAR(10) NOT NULL,
    bed_type ENUM('General','Semi-Private','Private','ICU','NICU') DEFAULT 'General',
    daily_rate DECIMAL(10,2),
    status ENUM('Available','Occupied','Maintenance') DEFAULT 'Available',
    FOREIGN KEY (ward_id) REFERENCES wards(ward_id)
);

-- Admissions
CREATE TABLE admissions (
    admission_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    bed_id INT,
    admission_date DATETIME NOT NULL,
    discharge_date DATETIME,
    admission_type ENUM('Emergency','Planned','Transfer'),
    diagnosis VARCHAR(255),
    status ENUM('Admitted','Discharged','Transferred') DEFAULT 'Admitted',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (bed_id) REFERENCES beds(bed_id)
);

-- Billing
CREATE TABLE billing (
    bill_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    appointment_id INT,
    admission_id INT,
    bill_date DATE NOT NULL,
    subtotal DECIMAL(12,2),
    tax DECIMAL(10,2) DEFAULT 0,
    discount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(12,2) NOT NULL,
    payment_status ENUM('Pending','Partial','Paid','Overdue') DEFAULT 'Pending',
    payment_method ENUM('Cash','Card','Insurance','Online'),
    payment_date DATE,
    due_date DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id),
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

-- Lab Tests
CREATE TABLE lab_tests (
    test_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    test_name VARCHAR(100) NOT NULL,
    test_category ENUM('Blood','Urine','Imaging','Cardiac','Other'),
    test_date DATE NOT NULL,
    result_date DATE,
    result_value TEXT,
    normal_range VARCHAR(100),
    status ENUM('Pending','In Progress','Completed') DEFAULT 'Pending',
    cost DECIMAL(10,2),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- Medicines
CREATE TABLE medicines (
    medicine_id INT PRIMARY KEY AUTO_INCREMENT,
    medicine_name VARCHAR(100) NOT NULL,
    generic_name VARCHAR(100),
    category VARCHAR(50),
    manufacturer VARCHAR(100),
    unit_price DECIMAL(10,2),
    quantity_in_stock INT DEFAULT 0,
    reorder_level INT DEFAULT 50,
    expiry_date DATE
);

-- Staff
CREATE TABLE staff (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role ENUM('Nurse','Technician','Receptionist','Admin','Pharmacist'),
    department_id INT,
    phone VARCHAR(15),
    email VARCHAR(100),
    hire_date DATE,
    salary DECIMAL(10,2),
    shift ENUM('Morning','Afternoon','Night'),
    status ENUM('Active','Inactive') DEFAULT 'Active',
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Insurance Providers
CREATE TABLE insurance_providers (
    insurance_id INT PRIMARY KEY AUTO_INCREMENT,
    provider_name VARCHAR(100) NOT NULL,
    contact_phone VARCHAR(15),
    email VARCHAR(100),
    coverage_percentage DECIMAL(5,2)
);

-- Insurance Claims
CREATE TABLE insurance_claims (
    claim_id INT PRIMARY KEY AUTO_INCREMENT,
    bill_id INT NOT NULL,
    insurance_id INT NOT NULL,
    claim_amount DECIMAL(12,2),
    approved_amount DECIMAL(12,2),
    status ENUM('Submitted','Processing','Approved','Rejected','Paid') DEFAULT 'Submitted',
    submission_date DATE,
    approval_date DATE,
    rejection_reason TEXT,
    FOREIGN KEY (bill_id) REFERENCES billing(bill_id),
    FOREIGN KEY (insurance_id) REFERENCES insurance_providers(insurance_id)
);

-- Create Indexes
CREATE INDEX idx_app_date ON appointments(appointment_date);
CREATE INDEX idx_app_status ON appointments(status);
CREATE INDEX idx_patient_reg ON patients(registration_date);
CREATE INDEX idx_bill_date ON billing(bill_date);
CREATE INDEX idx_bill_status ON billing(payment_status);
