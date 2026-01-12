"""
Hospital Management System - Complete Analysis
Run: pip install pandas numpy matplotlib seaborn plotly sqlalchemy pymysql openpyxl
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')

# ============================================
# CONFIGURATION
# ============================================

DB_USER = 'root'
DB_PASSWORD = "Duckgoforit@09"  # UPDATE THIS
DB_HOST = '127.0.0.1'
DB_NAME = 'hospital_db'

from urllib.parse import quote_plus

# Create engine
encoded_password = quote_plus(DB_PASSWORD)
engine = create_engine(f'mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}')

# Style settings
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
sns.set_palette("husl")

print("=" * 60)
print("HOSPITAL MANAGEMENT SYSTEM - DATA ANALYSIS")
print("=" * 60)

# ============================================
# DATA EXTRACTION
# ============================================

print("\n[>] Extracting data from database...")

patients = pd.read_sql("SELECT * FROM patients", engine)
doctors = pd.read_sql("SELECT * FROM doctors", engine)
departments = pd.read_sql("SELECT * FROM departments", engine)
appointments = pd.read_sql("SELECT * FROM appointments", engine)
medical_records = pd.read_sql("SELECT * FROM medical_records", engine)
billing = pd.read_sql("SELECT * FROM billing", engine)
admissions = pd.read_sql("SELECT * FROM admissions", engine)
beds = pd.read_sql("SELECT * FROM beds", engine)
lab_tests = pd.read_sql("SELECT * FROM lab_tests", engine)
insurance_claims = pd.read_sql("SELECT * FROM insurance_claims", engine)

print("[OK] Data extraction complete!")

# ============================================
# DATA CLEANING & FEATURE ENGINEERING
# ============================================

print("\n[>] Cleaning and transforming data...")

# Patients
patients['date_of_birth'] = pd.to_datetime(patients['date_of_birth'])
patients['registration_date'] = pd.to_datetime(patients['registration_date'])
patients['age'] = ((datetime.now() - patients['date_of_birth']).dt.days / 365.25).astype(int)

def age_group(age):
    if age < 18: return '0-17'
    elif age < 31: return '18-30'
    elif age < 46: return '31-45'
    elif age < 61: return '46-60'
    else: return '60+'

patients['age_group'] = patients['age'].apply(age_group)

# Appointments
appointments['appointment_date'] = pd.to_datetime(appointments['appointment_date'])
appointments['year'] = appointments['appointment_date'].dt.year
appointments['month'] = appointments['appointment_date'].dt.month
appointments['month_name'] = appointments['appointment_date'].dt.month_name()
appointments['day_name'] = appointments['appointment_date'].dt.day_name()
appointments['hour'] = pd.to_timedelta(appointments['appointment_time'].astype(str)).dt.components['hours']

# Billing
billing['bill_date'] = pd.to_datetime(billing['bill_date'])
billing['year_month'] = billing['bill_date'].dt.to_period('M')

# Admissions
admissions['admission_date'] = pd.to_datetime(admissions['admission_date'])
admissions['discharge_date'] = pd.to_datetime(admissions['discharge_date'])
admissions['length_of_stay'] = (admissions['discharge_date'] - admissions['admission_date']).dt.days

print("[OK] Data transformation complete!")

# ============================================
# KEY METRICS CALCULATION
# ============================================

print("\n[DATA] Calculating Key Performance Indicators...")

# Basic Counts
total_patients = len(patients)
total_doctors = len(doctors)
total_appointments = len(appointments)
total_revenue = billing['total_amount'].sum()

# Appointment Metrics
completed_appointments = len(appointments[appointments['status'] == 'Completed'])
no_show_rate = len(appointments[appointments['status'] == 'No Show']) / len(appointments[appointments['appointment_date'] < datetime.now()]) * 100

# Revenue Metrics
avg_bill_value = billing['total_amount'].mean()
collected_revenue = billing[billing['payment_status'] == 'Paid']['total_amount'].sum()
outstanding_revenue = billing[billing['payment_status'].isin(['Pending', 'Partial', 'Overdue'])]['total_amount'].sum()
collection_rate = (collected_revenue / total_revenue) * 100

# Bed Occupancy
total_beds = len(beds)
occupied_beds = len(beds[beds['status'] == 'Occupied'])
bed_occupancy_rate = (occupied_beds / total_beds) * 100

# Average Length of Stay
avg_los = admissions[admissions['status'] == 'Discharged']['length_of_stay'].mean()

print("\n" + "=" * 60)
print("[STATS] KEY PERFORMANCE INDICATORS")
print("=" * 60)
print(f"Total Patients:        {total_patients:,}")
print(f"Total Doctors:         {total_doctors}")
print(f"Total Appointments:    {total_appointments:,}")
print(f"Completed Appointments:{completed_appointments:,}")
print(f"No-Show Rate:          {no_show_rate:.2f}%")
print(f"Total Revenue:         INR {total_revenue:,.2f}")
print(f"Collected Revenue:     INR {collected_revenue:,.2f}")
print(f"Outstanding:           INR {outstanding_revenue:,.2f}")
print(f"Collection Rate:       {collection_rate:.2f}%")
print(f"Avg Bill Value:        INR {avg_bill_value:,.2f}")
print(f"Bed Occupancy Rate:    {bed_occupancy_rate:.2f}%")
print(f"Avg Length of Stay:    {avg_los:.1f} days")
print("=" * 60)

# ============================================
# VISUALIZATIONS
# ============================================

print("\n[PLOT] Creating Visualizations...")

# Create output directory
import os
os.makedirs('output', exist_ok=True)

# ----- 1. Patient Demographics -----
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Patient Demographics Analysis', fontsize=16, fontweight='bold')

# Gender Distribution
gender_counts = patients['gender'].value_counts()
axes[0, 0].pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=['#3498db', '#e74c3c', '#2ecc71'])
axes[0, 0].set_title('Gender Distribution')

# Age Group Distribution
age_order = ['0-17', '18-30', '31-45', '46-60', '60+']
age_counts = patients['age_group'].value_counts().reindex(age_order)
axes[0, 1].bar(age_counts.index, age_counts.values, color='#3498db')
axes[0, 1].set_title('Age Group Distribution')
axes[0, 1].set_xlabel('Age Group')
axes[0, 1].set_ylabel('Count')

# Blood Group Distribution
blood_counts = patients['blood_group'].value_counts()
axes[1, 0].bar(blood_counts.index, blood_counts.values, color='#e74c3c')
axes[1, 0].set_title('Blood Group Distribution')
axes[1, 0].set_xlabel('Blood Group')
axes[1, 0].set_ylabel('Count')

# City Distribution
city_counts = patients['city'].value_counts().head(8)
axes[1, 1].barh(city_counts.index, city_counts.values, color='#2ecc71')
axes[1, 1].set_title('Patients by City')
axes[1, 1].set_xlabel('Count')

plt.tight_layout()
plt.savefig('output/1_patient_demographics.png', dpi=300, bbox_inches='tight')
plt.close()
print("  [OK] Patient Demographics saved")

# ----- 2. Appointment Analysis -----
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Appointment Analysis', fontsize=16, fontweight='bold')

# Status Distribution
status_counts = appointments['status'].value_counts()
colors = {'Completed': '#2ecc71', 'Scheduled': '#3498db', 'Cancelled': '#e74c3c', 'No Show': '#f39c12'}
axes[0, 0].pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', 
               colors=[colors.get(s, '#95a5a6') for s in status_counts.index])
axes[0, 0].set_title('Appointment Status Distribution')

# Appointments by Type
type_counts = appointments['appointment_type'].value_counts()
axes[0, 1].bar(type_counts.index, type_counts.values, color='#9b59b6')
axes[0, 1].set_title('Appointments by Type')
axes[0, 1].tick_params(axis='x', rotation=45)

# Peak Hours
hour_counts = appointments['hour'].value_counts().sort_index()
axes[1, 0].plot(hour_counts.index, hour_counts.values, marker='o', linewidth=2, color='#3498db')
axes[1, 0].fill_between(hour_counts.index, hour_counts.values, alpha=0.3)
axes[1, 0].set_title('Appointments by Hour')
axes[1, 0].set_xlabel('Hour of Day')
axes[1, 0].set_ylabel('Count')

# Day of Week
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_counts = appointments['day_name'].value_counts().reindex(day_order)
axes[1, 1].bar(day_counts.index, day_counts.values, color='#1abc9c')
axes[1, 1].set_title('Appointments by Day of Week')
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('output/2_appointment_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("  [OK] Appointment Analysis saved")

# ----- 3. Revenue Analysis -----
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Revenue Analysis', fontsize=16, fontweight='bold')

# Monthly Revenue Trend
monthly_revenue = billing.groupby(billing['bill_date'].dt.to_period('M'))['total_amount'].sum()
monthly_revenue.index = monthly_revenue.index.astype(str)
axes[0, 0].plot(range(len(monthly_revenue)), monthly_revenue.values, marker='o', linewidth=2, color='#27ae60')
axes[0, 0].fill_between(range(len(monthly_revenue)), monthly_revenue.values, alpha=0.3, color='#27ae60')
axes[0, 0].set_title('Monthly Revenue Trend')
axes[0, 0].set_xlabel('Month')
axes[0, 0].set_ylabel('Revenue (INR)')
axes[0, 0].tick_params(axis='x', rotation=45)
step = max(1, len(monthly_revenue) // 12)
axes[0, 0].set_xticks(range(0, len(monthly_revenue), step))
axes[0, 0].set_xticklabels(monthly_revenue.index[::step])

# Payment Status
payment_status = billing.groupby('payment_status')['total_amount'].sum()
colors_pay = {'Paid': '#27ae60', 'Pending': '#f39c12', 'Partial': '#3498db', 'Overdue': '#e74c3c'}
axes[0, 1].pie(payment_status, labels=payment_status.index, autopct='%1.1f%%',
               colors=[colors_pay.get(s, '#95a5a6') for s in payment_status.index])
axes[0, 1].set_title('Revenue by Payment Status')

# Payment Method
paid_bills = billing[billing['payment_status'] == 'Paid']
method_counts = paid_bills.groupby('payment_method')['total_amount'].sum()
axes[1, 0].bar(method_counts.index, method_counts.values, color='#8e44ad')
axes[1, 0].set_title('Revenue by Payment Method')
axes[1, 0].set_ylabel('Revenue (INR)')

# Revenue Distribution
axes[1, 1].hist(billing['total_amount'], bins=50, color='#16a085', edgecolor='white')
axes[1, 1].set_title('Bill Amount Distribution')
axes[1, 1].set_xlabel('Bill Amount (INR)')
axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig('output/3_revenue_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("  [OK] Revenue Analysis saved")

# ----- 4. Doctor Performance -----
# Merge doctors with appointments
doctor_stats = appointments.merge(doctors[['doctor_id', 'first_name', 'last_name', 'specialization', 'consultation_fee']], 
                                   on='doctor_id')
doctor_stats['doctor_name'] = doctor_stats['first_name'] + ' ' + doctor_stats['last_name']

doctor_summary = doctor_stats.groupby(['doctor_id', 'doctor_name', 'specialization']).agg({
    'appointment_id': 'count',
    'status': lambda x: (x == 'Completed').sum()
}).reset_index()
doctor_summary.columns = ['doctor_id', 'doctor_name', 'specialization', 'total_appointments', 'completed']
doctor_summary['completion_rate'] = (doctor_summary['completed'] / doctor_summary['total_appointments'] * 100).round(2)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Doctor Performance Analysis', fontsize=16, fontweight='bold')

# Top 10 Doctors by Appointments
top_doctors = doctor_summary.nlargest(10, 'total_appointments')
axes[0].barh(top_doctors['doctor_name'], top_doctors['total_appointments'], color='#3498db')
axes[0].set_title('Top 10 Doctors by Appointments')
axes[0].set_xlabel('Total Appointments')

# Appointments by Specialization
spec_counts = doctor_stats.groupby('specialization')['appointment_id'].count().sort_values(ascending=True)
axes[1].barh(spec_counts.index, spec_counts.values, color='#e67e22')
axes[1].set_title('Appointments by Specialization')
axes[1].set_xlabel('Appointments')

plt.tight_layout()
plt.savefig('output/4_doctor_performance.png', dpi=300, bbox_inches='tight')
plt.close()
print("  [OK] Doctor Performance saved")

# ----- 5. Bed & Admission Analysis -----
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Bed & Admission Analysis', fontsize=16, fontweight='bold')

# Bed Occupancy by Type
bed_occ = beds.groupby('bed_type').apply(lambda x: (x['status'] == 'Occupied').sum() / len(x) * 100)
axes[0, 0].bar(bed_occ.index, bed_occ.values, color='#e74c3c')
axes[0, 0].set_title('Bed Occupancy Rate by Type')
axes[0, 0].set_ylabel('Occupancy %')
axes[0, 0].axhline(y=80, color='red', linestyle='--', label='Target 80%')
axes[0, 0].legend()

# Admission Type
adm_type = admissions['admission_type'].value_counts()
axes[0, 1].pie(adm_type, labels=adm_type.index, autopct='%1.1f%%', colors=['#e74c3c', '#3498db', '#2ecc71'])
axes[0, 1].set_title('Admissions by Type')

# Monthly Admissions
monthly_adm = admissions.groupby(admissions['admission_date'].dt.to_period('M')).size()
monthly_adm.index = monthly_adm.index.astype(str)
axes[1, 0].plot(range(len(monthly_adm)), monthly_adm.values, marker='s', linewidth=2, color='#9b59b6')
axes[1, 0].set_title('Monthly Admission Trend')
axes[1, 0].set_xlabel('Month')
axes[1, 0].set_ylabel('Admissions')
step = max(1, len(monthly_adm) // 12)
axes[1, 0].set_xticks(range(0, len(monthly_adm), step))
axes[1, 0].set_xticklabels(monthly_adm.index[::step], rotation=45)

# Length of Stay Distribution
discharged = admissions[admissions['status'] == 'Discharged']
axes[1, 1].hist(discharged['length_of_stay'].dropna(), bins=20, color='#1abc9c', edgecolor='white')
axes[1, 1].set_title('Length of Stay Distribution')
axes[1, 1].set_xlabel('Days')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].axvline(x=avg_los, color='red', linestyle='--', label=f'Avg: {avg_los:.1f} days')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('output/5_bed_admission_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("  [OK] Bed & Admission Analysis saved")

# ----- 6. Lab Test Analysis -----
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Laboratory Analysis', fontsize=16, fontweight='bold')

# Tests by Category
cat_counts = lab_tests['test_category'].value_counts()
axes[0].pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%')
axes[0].set_title('Tests by Category')

# Most Common Tests
test_counts = lab_tests['test_name'].value_counts().head(10)
axes[1].barh(test_counts.index, test_counts.values, color='#16a085')
axes[1].set_title('Top 10 Lab Tests')
axes[1].set_xlabel('Count')

plt.tight_layout()
plt.savefig('output/6_lab_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("  [OK] Lab Analysis saved")

# ----- 7. Interactive Dashboard (Plotly) -----
print("\n[DATA] Creating Interactive Dashboard...")

# KPI Cards Data
kpi_data = {
    'Metric': ['Total Patients', 'Total Revenue', 'Avg Bill Value', 'Bed Occupancy', 'No-Show Rate', 'Avg LOS'],
    'Value': [f'{total_patients:,}', f'INR {total_revenue/100000:.1f}L', f'INR {avg_bill_value:,.0f}', 
              f'{bed_occupancy_rate:.1f}%', f'{no_show_rate:.1f}%', f'{avg_los:.1f} days']
}

# Create dashboard
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=('Monthly Revenue Trend', 'Appointment Status', 
                   'Patients by Age Group', 'Top Specializations',
                   'Payment Status', 'Daily Appointments'),
    specs=[[{"type": "scatter"}, {"type": "pie"}],
           [{"type": "bar"}, {"type": "bar"}],
           [{"type": "pie"}, {"type": "scatter"}]]
)

# 1. Monthly Revenue
monthly_rev = billing.groupby(billing['bill_date'].dt.to_period('M'))['total_amount'].sum().reset_index()
monthly_rev['bill_date'] = monthly_rev['bill_date'].astype(str)
fig.add_trace(go.Scatter(x=monthly_rev['bill_date'], y=monthly_rev['total_amount'], 
                         mode='lines+markers', name='Revenue', line=dict(color='#27ae60')), row=1, col=1)

# 2. Appointment Status Pie
status_counts = appointments['status'].value_counts()
fig.add_trace(go.Pie(labels=status_counts.index, values=status_counts.values, name='Status'), row=1, col=2)

# 3. Age Group Bar
age_counts = patients['age_group'].value_counts().reindex(['0-17', '18-30', '31-45', '46-60', '60+'])
fig.add_trace(go.Bar(x=age_counts.index, y=age_counts.values, name='Age Group', marker_color='#3498db'), row=2, col=1)

# 4. Specialization Bar
spec_counts = doctor_stats.groupby('specialization')['appointment_id'].count().nlargest(6)
fig.add_trace(go.Bar(x=spec_counts.values, y=spec_counts.index, orientation='h', name='Specialization', 
                     marker_color='#e67e22'), row=2, col=2)

# 5. Payment Status Pie
pay_status = billing.groupby('payment_status')['total_amount'].sum()
fig.add_trace(go.Pie(labels=pay_status.index, values=pay_status.values, name='Payment'), row=3, col=1)

# 6. Daily Appointments (Last 30 days)
last_30 = appointments[appointments['appointment_date'] >= datetime.now() - timedelta(days=30)]
daily_app = last_30.groupby('appointment_date').size().reset_index(name='count')
fig.add_trace(go.Scatter(x=daily_app['appointment_date'], y=daily_app['count'], 
                         mode='lines+markers', name='Daily', line=dict(color='#9b59b6')), row=3, col=2)

fig.update_layout(height=900, title_text="Hospital Management Dashboard", showlegend=False)
fig.write_html('output/7_interactive_dashboard.html')
print("  [OK] Interactive Dashboard saved")

# ============================================
# EXPORT TO EXCEL
# ============================================

print("\n[FILE] Exporting data to Excel...")

with pd.ExcelWriter('output/hospital_analysis_data.xlsx', engine='openpyxl') as writer:
    # Summary Sheet
    summary_df = pd.DataFrame({
        'Metric': ['Total Patients', 'Total Doctors', 'Total Appointments', 'Completed Appointments',
                  'No-Show Rate (%)', 'Total Revenue (INR)', 'Collected Revenue (INR)', 'Outstanding (INR)',
                  'Collection Rate (%)', 'Avg Bill Value (INR)', 'Bed Occupancy (%)', 'Avg Length of Stay (days)'],
        'Value': [total_patients, total_doctors, total_appointments, completed_appointments,
                 round(no_show_rate, 2), round(total_revenue, 2), round(collected_revenue, 2), 
                 round(outstanding_revenue, 2), round(collection_rate, 2), round(avg_bill_value, 2),
                 round(bed_occupancy_rate, 2), round(avg_los, 1)]
    })
    summary_df.to_excel(writer, sheet_name='KPI_Summary', index=False)
    
    # Monthly Revenue
    monthly_revenue_df = billing.groupby(billing['bill_date'].dt.to_period('M')).agg({
        'bill_id': 'count',
        'total_amount': ['sum', 'mean']
    }).reset_index()
    monthly_revenue_df.columns = ['Month', 'Bill_Count', 'Total_Revenue', 'Avg_Bill_Value']
    monthly_revenue_df['Month'] = monthly_revenue_df['Month'].astype(str)
    monthly_revenue_df.to_excel(writer, sheet_name='Monthly_Revenue', index=False)
    
    # Doctor Performance
    doctor_summary.to_excel(writer, sheet_name='Doctor_Performance', index=False)
    
    # Appointment Analysis
    app_by_status = appointments.groupby(['year', 'month', 'status']).size().reset_index(name='count')
    app_by_status.to_excel(writer, sheet_name='Appointment_Status', index=False)
    
    # Patient Demographics
    demo_df = patients.groupby(['gender', 'age_group', 'city']).size().reset_index(name='count')
    demo_df.to_excel(writer, sheet_name='Patient_Demographics', index=False)
    
    # Raw Data Samples
    patients.head(1000).to_excel(writer, sheet_name='Patients_Sample', index=False)
    appointments.head(1000).to_excel(writer, sheet_name='Appointments_Sample', index=False)
    billing.head(1000).to_excel(writer, sheet_name='Billing_Sample', index=False)

print("  [OK] Excel file saved")

# ============================================
# STATISTICAL ANALYSIS
# ============================================

print("\n[STATS] Statistical Analysis...")

# Correlation Analysis
numeric_billing = billing[['subtotal', 'tax', 'discount', 'total_amount']].copy()
correlation_matrix = numeric_billing.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='RdYlGn', center=0, fmt='.2f')
plt.title('Billing Amount Correlations')
plt.tight_layout()
plt.savefig('output/8_correlation_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("  [OK] Correlation Analysis saved")

# ============================================
# INSIGHTS SUMMARY
# ============================================

print("\n" + "=" * 60)
print("[INFO] KEY INSIGHTS & RECOMMENDATIONS")
print("=" * 60)

insights = f"""
1. PATIENT INSIGHTS:
   - Total active patients: {len(patients[patients['status'] == 'Active']):,}
   - Largest age group: {patients['age_group'].value_counts().idxmax()} ({patients['age_group'].value_counts().max():,} patients)
   - Most common blood group: {patients['blood_group'].value_counts().idxmax()}
   - Top city: {patients['city'].value_counts().idxmax()} ({patients['city'].value_counts().max():,} patients)

2. APPOINTMENT INSIGHTS:
   - Completion rate: {(completed_appointments/len(appointments[appointments['appointment_date'] < datetime.now()])*100):.1f}%
   - No-show rate: {no_show_rate:.1f}% (Target: <5%)
   - Peak hours: {appointments['hour'].value_counts().head(3).index.tolist()}
   - Busiest day: {appointments['day_name'].value_counts().idxmax()}

3. REVENUE INSIGHTS:
   - Collection rate: {collection_rate:.1f}%
   - Outstanding amount: INR {outstanding_revenue:,.2f}
   - Average bill value: INR {avg_bill_value:,.2f}
   - Top payment method: {paid_bills['payment_method'].value_counts().idxmax() if len(paid_bills) > 0 else 'N/A'}

4. OPERATIONAL INSIGHTS:
   - Bed occupancy: {bed_occupancy_rate:.1f}%
   - Average length of stay: {avg_los:.1f} days
   - Current admissions: {len(admissions[admissions['status'] == 'Admitted'])}

5. RECOMMENDATIONS:
   - {"[!WARN!] High no-show rate! Implement reminder system." if no_show_rate > 5 else "[OK] No-show rate is acceptable."}
   - {"[!WARN!] Collection rate below 80%! Focus on payment follow-ups." if collection_rate < 80 else "[OK] Collection rate is healthy."}
   - {"[!WARN!] High bed occupancy! Consider capacity expansion." if bed_occupancy_rate > 85 else "[OK] Bed capacity is manageable."}
   - Consider adding more doctors in {doctor_stats.groupby('specialization')['appointment_id'].count().idxmax()} department.
"""

print(insights)

# Save insights to file
with open('output/insights_report.txt', 'w') as f:
    f.write("HOSPITAL MANAGEMENT SYSTEM - ANALYSIS REPORT\n")
    f.write("=" * 60 + "\n")
    f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 60 + "\n\n")
    f.write(insights)

print("\n" + "=" * 60)
print("[OK] ANALYSIS COMPLETE!")
print("=" * 60)
print("\nOutput files created in 'output' folder:")
print("  - 1_patient_demographics.png")
print("  - 2_appointment_analysis.png")
print("  - 3_revenue_analysis.png")
print("  - 4_doctor_performance.png")
print("  - 5_bed_admission_analysis.png")
print("  - 6_lab_analysis.png")
print("  - 7_interactive_dashboard.html")
print("  - 8_correlation_analysis.png")
print("  - hospital_analysis_data.xlsx")
print("  - insights_report.txt")
print("=" * 60)
