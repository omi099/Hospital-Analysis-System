"""
Hospital Data Generator - Generates 50,000+ records
Run: pip install faker mysql-connector-python
Then: python data_generator.py
"""

import random
from datetime import datetime, timedelta
from faker import Faker
import mysql.connector

fake = Faker()
Faker.seed(2026)
random.seed(2026)

# UPDATE THESE
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Duckgoforit@09',
    'database': 'hospital_db'
}

# Reference Data
DEPARTMENTS = [
    'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Gynecology',
    'General Medicine', 'Dermatology', 'ENT', 'Ophthalmology', 'Psychiatry',
    'Emergency', 'ICU'
]

SPECIALIZATIONS = {
    'Cardiology': 'Cardiologist',
    'Neurology': 'Neurologist',
    'Orthopedics': 'Orthopedic Surgeon',
    'Pediatrics': 'Pediatrician',
    'Gynecology': 'Gynecologist',
    'General Medicine': 'General Physician',
    'Dermatology': 'Dermatologist',
    'ENT': 'ENT Specialist',
    'Ophthalmology': 'Ophthalmologist',
    'Psychiatry': 'Psychiatrist',
    'Emergency': 'Emergency Physician',
    'ICU': 'Intensivist'
}

BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad']

DIAGNOSES = [
    'Hypertension', 'Diabetes Type 2', 'Upper Respiratory Infection', 'Migraine',
    'Gastritis', 'Arthritis', 'Bronchitis', 'Anemia', 'Thyroid Disorder',
    'Vitamin Deficiency', 'Allergic Rhinitis', 'UTI', 'Anxiety', 'Asthma'
]

LAB_TESTS = [
    ('Complete Blood Count', 'Blood', 500),
    ('Blood Sugar', 'Blood', 150),
    ('Lipid Profile', 'Blood', 800),
    ('Thyroid Profile', 'Blood', 1200),
    ('Liver Function Test', 'Blood', 900),
    ('Kidney Function Test', 'Blood', 850),
    ('Urine Routine', 'Urine', 200),
    ('ECG', 'Cardiac', 400),
    ('X-Ray', 'Imaging', 600),
    ('Ultrasound', 'Imaging', 1500)
]

MEDICINES = [
    ('Paracetamol 500mg', 'Acetaminophen', 'Analgesic', 2.50),
    ('Amoxicillin 500mg', 'Amoxicillin', 'Antibiotic', 8.00),
    ('Omeprazole 20mg', 'Omeprazole', 'Antacid', 5.00),
    ('Metformin 500mg', 'Metformin', 'Antidiabetic', 3.00),
    ('Amlodipine 5mg', 'Amlodipine', 'Antihypertensive', 4.50),
    ('Cetirizine 10mg', 'Cetirizine', 'Antihistamine', 2.00),
    ('Ibuprofen 400mg', 'Ibuprofen', 'Anti-inflammatory', 3.50),
    ('Azithromycin 500mg', 'Azithromycin', 'Antibiotic', 15.00)
]

INSURANCE_PROVIDERS = [
    ('Star Health', 80), ('ICICI Lombard', 75), ('HDFC Ergo', 70),
    ('Max Bupa', 85), ('Bajaj Allianz', 75), ('New India Assurance', 70)
]

WARDS = [
    ('General Ward A', 'General', 20, 500),
    ('General Ward B', 'General', 20, 500),
    ('Semi-Private', 'Semi-Private', 10, 1500),
    ('Private Ward', 'Private', 8, 3000),
    ('ICU', 'ICU', 10, 8000),
    ('Pediatric Ward', 'General', 15, 800)
]


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def generate_all_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Generating Hospital Data...")
    
    # 1. Departments
    print("1. Inserting Departments...")
    for i, dept in enumerate(DEPARTMENTS, 1):
        cursor.execute(
            "INSERT INTO departments (department_name, floor_number, phone_extension) VALUES (%s, %s, %s)",
            (dept, (i % 4) + 1, f"10{i:02d}")
        )
    conn.commit()
    
    # 2. Doctors (60)
    print("2. Inserting Doctors...")
    for i in range(60):
        dept_id = (i % 12) + 1
        dept_name = DEPARTMENTS[dept_id - 1]
        cursor.execute("""
            INSERT INTO doctors (first_name, last_name, email, phone, specialization, 
                department_id, experience_years, consultation_fee, hire_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            fake.first_name(), fake.last_name(), fake.unique.email(),
            fake.phone_number()[:15], SPECIALIZATIONS[dept_name], dept_id,
            random.randint(2, 25), random.choice([500, 700, 1000, 1500, 2000]),
            fake.date_between(start_date='-10y', end_date='-1y'),
            random.choices(['Active', 'On Leave'], weights=[95, 5])[0]
        ))
    conn.commit()
    
    # 3. Patients (5000)
    print("3. Inserting Patients...")
    for i in range(5000):
        gender = random.choice(['Male', 'Female'])
        cursor.execute("""
            INSERT INTO patients (first_name, last_name, date_of_birth, gender, blood_group,
                phone, email, address, city, state, zip_code, emergency_contact_name,
                emergency_contact_phone, registration_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            fake.first_name_male() if gender == 'Male' else fake.first_name_female(),
            fake.last_name(), fake.date_of_birth(minimum_age=1, maximum_age=90),
            gender, random.choice(BLOOD_GROUPS), fake.phone_number()[:15],
            fake.email() if random.random() > 0.3 else None, fake.street_address(),
            random.choice(CITIES), 'Maharashtra', fake.postcode()[:10],
            fake.name(), fake.phone_number()[:15],
            fake.date_between(start_date='-2y', end_date='today'),
            random.choices(['Active', 'Inactive'], weights=[95, 5])[0]
        ))
        if (i + 1) % 1000 == 0:
            print(f"   {i + 1} patients inserted...")
            conn.commit()
    conn.commit()
    
    # 4. Appointments (15000)
    print("4. Inserting Appointments...")
    times = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00',
             '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00']
    symptoms = ['Fever', 'Headache', 'Cough', 'Body Pain', 'Fatigue', 'Chest Pain',
                'Dizziness', 'Nausea', 'Back Pain', 'Joint Pain']
    
    for i in range(15000):
        app_date = fake.date_between(start_date='-2y', end_date='+1m')
        if app_date < datetime.now().date():
            status = random.choices(['Completed', 'Cancelled', 'No Show'], weights=[85, 10, 5])[0]
        else:
            status = 'Scheduled'
        
        cursor.execute("""
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time,
                appointment_type, status, symptoms)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            random.randint(1, 5000), random.randint(1, 60), app_date,
            random.choice(times),
            random.choices(['Consultation', 'Follow-up', 'Routine Checkup', 'Emergency'], 
                          weights=[50, 25, 20, 5])[0],
            status, ', '.join(random.sample(symptoms, random.randint(1, 3)))
        ))
        if (i + 1) % 3000 == 0:
            print(f"   {i + 1} appointments inserted...")
            conn.commit()
    conn.commit()
    
    # 5. Medical Records (12000)
    print("5. Inserting Medical Records...")
    for i in range(12000):
        record_date = fake.date_between(start_date='-2y', end_date='today')
        cursor.execute("""
            INSERT INTO medical_records (patient_id, doctor_id, appointment_id, diagnosis,
                treatment, prescription, blood_pressure, heart_rate, temperature, weight,
                record_date, follow_up_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            random.randint(1, 5000), random.randint(1, 60),
            random.randint(1, 15000) if random.random() > 0.1 else None,
            random.choice(DIAGNOSES), fake.sentence(), fake.sentence(),
            f"{random.randint(100, 140)}/{random.randint(60, 90)}",
            random.randint(60, 100), round(random.uniform(97, 100), 1),
            round(random.uniform(40, 100), 1), record_date,
            record_date + timedelta(days=random.choice([7, 14, 30])) if random.random() > 0.3 else None
        ))
        if (i + 1) % 3000 == 0:
            print(f"   {i + 1} records inserted...")
            conn.commit()
    conn.commit()
    
    # 6. Wards and Beds
    print("6. Inserting Wards and Beds...")
    for i, (name, bed_type, total, rate) in enumerate(WARDS, 1):
        cursor.execute(
            "INSERT INTO wards (ward_name, department_id, floor_number, total_beds) VALUES (%s, %s, %s, %s)",
            (name, random.randint(1, 12), (i % 4) + 1, total)
        )
        for bed_num in range(1, total + 1):
            cursor.execute("""
                INSERT INTO beds (ward_id, bed_number, bed_type, daily_rate, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                i, f"{name[:2].upper()}{bed_num:03d}", bed_type, rate,
                random.choices(['Available', 'Occupied', 'Maintenance'], weights=[60, 35, 5])[0]
            ))
    conn.commit()
    
    # 7. Admissions (2000)
    print("7. Inserting Admissions...")
    for i in range(2000):
        adm_date = fake.date_time_between(start_date='-2y', end_date='now')
        if adm_date < datetime.now() - timedelta(days=7):
            dis_date = adm_date + timedelta(days=random.randint(1, 14))
            status = 'Discharged'
        else:
            dis_date = None
            status = 'Admitted'
        
        cursor.execute("""
            INSERT INTO admissions (patient_id, doctor_id, bed_id, admission_date,
                discharge_date, admission_type, diagnosis, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            random.randint(1, 5000), random.randint(1, 60), random.randint(1, 83),
            adm_date, dis_date,
            random.choices(['Emergency', 'Planned', 'Transfer'], weights=[30, 60, 10])[0],
            random.choice(DIAGNOSES), status
        ))
    conn.commit()
    
    # 8. Billing (10000)
    print("8. Inserting Billing...")
    for i in range(10000):
        bill_date = fake.date_between(start_date='-2y', end_date='today')
        subtotal = random.choice([500, 700, 1000, 1500, 2000, 3000, 5000, 8000, 15000, 25000])
        discount = subtotal * random.choice([0, 0, 0.05, 0.10])
        tax = (subtotal - discount) * 0.05
        total = subtotal - discount + tax
        
        days_old = (datetime.now().date() - bill_date).days
        if days_old > 30:
            status = random.choices(['Paid', 'Overdue'], weights=[85, 15])[0]
        elif days_old > 7:
            status = random.choices(['Paid', 'Partial', 'Pending'], weights=[70, 15, 15])[0]
        else:
            status = random.choices(['Paid', 'Pending'], weights=[50, 50])[0]
        
        cursor.execute("""
            INSERT INTO billing (patient_id, appointment_id, admission_id, bill_date,
                subtotal, tax, discount, total_amount, payment_status, payment_method,
                payment_date, due_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            random.randint(1, 5000),
            random.randint(1, 15000) if random.random() > 0.2 else None,
            random.randint(1, 2000) if random.random() > 0.7 else None,
            bill_date, subtotal, round(tax, 2), round(discount, 2), round(total, 2),
            status,
            random.choice(['Cash', 'Card', 'Insurance', 'Online']) if status == 'Paid' else None,
            bill_date + timedelta(days=random.randint(0, 15)) if status == 'Paid' else None,
            bill_date + timedelta(days=30)
        ))
        if (i + 1) % 2000 == 0:
            print(f"   {i + 1} bills inserted...")
            conn.commit()
    conn.commit()
    
    # 9. Lab Tests (8000)
    print("9. Inserting Lab Tests...")
    for i in range(8000):
        test = random.choice(LAB_TESTS)
        test_date = fake.date_between(start_date='-2y', end_date='today')
        if test_date < datetime.now().date() - timedelta(days=3):
            status = 'Completed'
            result_date = test_date + timedelta(days=random.randint(1, 3))
        else:
            status = random.choice(['Pending', 'In Progress'])
            result_date = None
        
        cursor.execute("""
            INSERT INTO lab_tests (patient_id, doctor_id, test_name, test_category,
                test_date, result_date, result_value, normal_range, status, cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            random.randint(1, 5000), random.randint(1, 60), test[0], test[1],
            test_date, result_date,
            f"{random.uniform(50, 150):.1f}" if status == 'Completed' else None,
            '70-110', status, test[2]
        ))
        if (i + 1) % 2000 == 0:
            print(f"   {i + 1} tests inserted...")
            conn.commit()
    conn.commit()
    
    # 10. Medicines
    print("10. Inserting Medicines...")
    for med in MEDICINES:
        cursor.execute("""
            INSERT INTO medicines (medicine_name, generic_name, category, manufacturer,
                unit_price, quantity_in_stock, reorder_level, expiry_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            med[0], med[1], med[2], fake.company(), med[3],
            random.randint(100, 1000), 50,
            fake.date_between(start_date='+6m', end_date='+3y')
        ))
    conn.commit()
    
    # 11. Staff (100)
    print("11. Inserting Staff...")
    roles = ['Nurse', 'Technician', 'Receptionist', 'Admin', 'Pharmacist']
    salaries = {'Nurse': (25000, 50000), 'Technician': (20000, 40000),
                'Receptionist': (18000, 30000), 'Admin': (30000, 60000), 'Pharmacist': (28000, 45000)}
    
    for _ in range(100):
        role = random.choice(roles)
        sal_range = salaries[role]
        cursor.execute("""
            INSERT INTO staff (first_name, last_name, role, department_id, phone, email,
                hire_date, salary, shift, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            fake.first_name(), fake.last_name(), role, random.randint(1, 12),
            fake.phone_number()[:15], fake.email(),
            fake.date_between(start_date='-8y', end_date='-1m'),
            random.randint(*sal_range), random.choice(['Morning', 'Afternoon', 'Night']),
            random.choices(['Active', 'Inactive'], weights=[95, 5])[0]
        ))
    conn.commit()
    
    # 12. Insurance
    print("12. Inserting Insurance Data...")
    for prov in INSURANCE_PROVIDERS:
        cursor.execute("""
            INSERT INTO insurance_providers (provider_name, contact_phone, email, coverage_percentage)
            VALUES (%s, %s, %s, %s)
        """, (prov[0], fake.phone_number()[:15], fake.company_email(), prov[1]))
    conn.commit()
    
    # 13. Insurance Claims (1500)
    print("13. Inserting Insurance Claims...")
    for _ in range(1500):
        claim_amt = random.randint(5000, 50000)
        status = random.choices(['Submitted', 'Processing', 'Approved', 'Rejected', 'Paid'],
                               weights=[10, 15, 25, 10, 40])[0]
        sub_date = fake.date_between(start_date='-1y', end_date='today')
        
        cursor.execute("""
            INSERT INTO insurance_claims (bill_id, insurance_id, claim_amount, approved_amount,
                status, submission_date, approval_date, rejection_reason)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            random.randint(1, 10000), random.randint(1, 6), claim_amt,
            round(claim_amt * random.uniform(0.6, 1.0), 2) if status in ['Approved', 'Paid'] else None,
            status, sub_date,
            sub_date + timedelta(days=random.randint(7, 30)) if status in ['Approved', 'Paid'] else None,
            'Documentation incomplete' if status == 'Rejected' else None
        ))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 50)
    print("DATA GENERATION COMPLETE!")
    print("=" * 50)
    print("Records created:")
    print("- Departments: 12")
    print("- Doctors: 60")
    print("- Patients: 5,000")
    print("- Appointments: 15,000")
    print("- Medical Records: 12,000")
    print("- Wards: 6, Beds: 83")
    print("- Admissions: 2,000")
    print("- Billing: 10,000")
    print("- Lab Tests: 8,000")
    print("- Medicines: 8")
    print("- Staff: 100")
    print("- Insurance Claims: 1,500")
    print("=" * 50)


if __name__ == "__main__":
    generate_all_data()
