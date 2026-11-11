import sqlite3
import os
import hashlib
from datetime import datetime, timedelta

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(DB_DIR, "cloud_blood_bank.db")
SCHEMA_FILE = os.path.join(DB_DIR, "schema.sql")

def hash_password(password: str) -> str:
    """Hash password using SHA-256 for secure cloud storage."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_db_connection():
    """Create a thread-safe database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionary-like objects
    return conn

def init_database():
    """Reads schema.sql and creates all tables."""
    print("[DB] Initializing Cloud Relational Schema...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("[DB] All 8 tables successfully created.")

def seed_sample_data():
    """Seeds realistic sample data for demo, testing, and presentation."""
    print("[DB] Seeding realistic sample data...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        print("[DB] Database already seeded. Skipping.")
        conn.close()
        return

    # 1. SEED USERS & ROLES
    # Admin
    cursor.execute("""
        INSERT INTO users (full_name, email, password_hash, role, phone, city, address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("Dr. Rajesh Varma (Admin)", "admin@bloodbank.org", hash_password("admin123"), "admin", "+91-9811002233", "Delhi", "Central Red Cross Blood Bank, New Delhi"))
    admin_id = cursor.lastrowid

    # Hospital 1: Apollo Hospital Delhi
    cursor.execute("""
        INSERT INTO users (full_name, email, password_hash, role, phone, city, address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("Apollo Hospital Delhi", "emergency@apollohospitals.com", hash_password("apollo123"), "hospital", "+91-11-26925858", "Delhi", "Sarita Vihar, Mathura Road, New Delhi"))
    apollo_user_id = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO hospitals (hospital_id, user_id, hospital_name, license_number, emergency_desk_contact, emergency_desk_person, google_maps_url, trust_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (1, apollo_user_id, "Indraprastha Apollo Hospital", "HOSP-DL-2024-8841", "+91-9876543210", "Sister Anita (Triage In-Charge)", "https://maps.google.com/?q=Apollo+Hospital+Delhi", 98))

    # Hospital 2: AIIMS Trauma Center
    cursor.execute("""
        INSERT INTO users (full_name, email, password_hash, role, phone, city, address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("AIIMS Trauma Center", "trauma@aiims.edu", hash_password("aiims123"), "hospital", "+91-11-26588500", "Delhi", "Ring Road, Ansari Nagar, New Delhi"))
    aiims_user_id = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO hospitals (hospital_id, user_id, hospital_name, license_number, emergency_desk_contact, emergency_desk_person, google_maps_url, trust_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (2, aiims_user_id, "AIIMS Apex Trauma Center", "HOSP-DL-1998-0012", "+91-9812345678", "Dr. Sameer Khan (CMO)", "https://maps.google.com/?q=AIIMS+Trauma+Center+Delhi", 100))

    # Hospital 3: SMS Medical College & Hospital Jaipur (Travel / Roaming Hub)
    cursor.execute("""
        INSERT INTO users (full_name, email, password_hash, role, phone, city, address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("SMS Medical College & Hospital", "sms.jaipur@hospital.org", hash_password("jaipur123"), "hospital", "+91-141-2560291", "Jaipur", "Jawahar Lal Nehru Marg, Jaipur, Rajasthan"))
    sms_user_id = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO hospitals (hospital_id, user_id, hospital_name, license_number, emergency_desk_contact, emergency_desk_person, google_maps_url, trust_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (3, sms_user_id, "SMS Medical College & Hospital, Jaipur", "RAJ-MCI-HOSP-1994-082", "+91-141-2560291", "Dr. Ashok Saxena (Head of Trauma)", "https://maps.google.com/?q=SMS+Hospital+Jaipur", 100))

    # Donors: 5 Donors with various blood groups
    donors_data = [
        ("Pooja Sharma", "pooja.donor@gmail.com", "donor123", "+91-9876112233", "Delhi", "A+", 1, 1, 3, "2026-08-15"),
        ("Rahul Verma", "rahul.donor@gmail.com", "donor123", "+91-9876223344", "Delhi", "O-", 1, 1, 5, "2026-07-20"), # O- Hero Donor!
        ("Aman Deep", "aman.donor@gmail.com", "donor123", "+91-9876334455", "Delhi", "B+", 1, 0, 1, "2026-09-01"),
        ("Neha Singh", "neha.donor@gmail.com", "donor123", "+91-9876445566", "Delhi", "AB+", 0, 0, 2, "2026-06-10"), # Unavailable currently
        ("Vikram Malhotra", "vikram.donor@gmail.com", "donor123", "+91-9876556677", "Delhi", "O+", 1, 1, 4, "2026-09-12"),
    ]

    for idx, (name, email, pwd, phone, city, bgroup, is_avail, night_avail, count, last_date) in enumerate(donors_data, start=1):
        cursor.execute("""
            INSERT INTO users (full_name, email, password_hash, role, phone, city, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, email, hash_password(pwd), "donor", phone, city, f"Sector-{idx*4}, Rohini, Delhi"))
        uid = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO donors (donor_id, user_id, blood_group, is_available, night_emergency_available, fitness_certificate_url, total_donations, last_donated_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (idx, uid, bgroup, is_avail, night_avail, f"cloud_storage://certificates/cert_donor_{idx}.pdf", count, last_date))

    # 2. SEED REAL-TIME BLOOD INVENTORY (With 35-Day Expiry Simulation for FIFO!)
    today = datetime.now().date()
    
    # Blood Inventory bags across groups:
    # Some collected 30 days ago (5 days left -> EXPIRING SOON, FIFO Priority!)
    # Some collected 7 days ago (28 days left -> FRESH)
    inventory_items = [
        # DELHI-NCR CLUSTER
        ("Central Red Cross Blood Bank", "Delhi", "O-", today - timedelta(days=25), today + timedelta(days=10), "BATCH-O-NEG-001", 3.8),
        ("Central Red Cross Blood Bank", "Delhi", "A+", today - timedelta(days=31), today + timedelta(days=4), "BATCH-A-POS-011", 4.1),
        ("Central Red Cross Blood Bank", "Delhi", "A+", today - timedelta(days=10), today + timedelta(days=25), "BATCH-A-POS-012", 4.0),
        ("City Civil Hospital Blood Bank", "Delhi", "A+", today - timedelta(days=5), today + timedelta(days=30), "BATCH-A-POS-013", 3.9),
        ("Central Red Cross Blood Bank", "Delhi", "B+", today - timedelta(days=29), today + timedelta(days=6), "BATCH-B-POS-021", 4.2),
        ("Central Red Cross Blood Bank", "Delhi", "B+", today - timedelta(days=15), today + timedelta(days=20), "BATCH-B-POS-022", 4.0),
        ("City Civil Hospital Blood Bank", "Delhi", "B+", today - timedelta(days=8), today + timedelta(days=27), "BATCH-B-POS-023", 4.0),
        ("Rotary Blood Bank Delhi", "Delhi", "B+", today - timedelta(days=2), today + timedelta(days=33), "BATCH-B-POS-024", 3.7),
        ("Central Red Cross Blood Bank", "Delhi", "O+", today - timedelta(days=12), today + timedelta(days=23), "BATCH-O-POS-031", 4.0),
        ("City Civil Hospital Blood Bank", "Delhi", "O+", today - timedelta(days=6), today + timedelta(days=29), "BATCH-O-POS-032", 3.9),
        ("Rotary Blood Bank Delhi", "Delhi", "O+", today - timedelta(days=1), today + timedelta(days=34), "BATCH-O-POS-033", 4.1),
        ("Central Red Cross Blood Bank", "Delhi", "AB+", today - timedelta(days=20), today + timedelta(days=15), "BATCH-AB-POS-041", 4.0),
        ("City Civil Hospital Blood Bank", "Delhi", "AB+", today - timedelta(days=14), today + timedelta(days=21), "BATCH-AB-POS-042", 3.8),
        ("City Civil Hospital Blood Bank", "Delhi", "B-", today - timedelta(days=18), today + timedelta(days=17), "BATCH-B-NEG-051", 4.0),
        ("Rotary Blood Bank Delhi", "Delhi", "A-", today - timedelta(days=22), today + timedelta(days=13), "BATCH-A-NEG-061", 3.9),

        # NOIDA CLUSTER
        ("Jaypee Hospital Blood Bank", "Noida", "A+", today - timedelta(days=12), today + timedelta(days=23), "BATCH-NOI-A01", 4.0),
        ("Jaypee Hospital Blood Bank", "Noida", "A+", today - timedelta(days=4), today + timedelta(days=31), "BATCH-NOI-A02", 4.0),
        ("Fortis Hospital Blood Center", "Noida", "B+", today - timedelta(days=10), today + timedelta(days=25), "BATCH-NOI-B01", 4.1),
        ("Fortis Hospital Blood Center", "Noida", "O+", today - timedelta(days=7), today + timedelta(days=28), "BATCH-NOI-O01", 3.9),
        ("District Hospital Blood Bank", "Noida", "O+", today - timedelta(days=2), today + timedelta(days=33), "BATCH-NOI-O02", 4.0),

        # LUCKNOW CLUSTER
        ("KGMU Blood Transfusion Center", "Lucknow", "O+", today - timedelta(days=15), today + timedelta(days=20), "BATCH-LKO-O01", 4.0),
        ("KGMU Blood Transfusion Center", "Lucknow", "O+", today - timedelta(days=8), today + timedelta(days=27), "BATCH-LKO-O02", 4.1),
        ("KGMU Blood Transfusion Center", "Lucknow", "B+", today - timedelta(days=6), today + timedelta(days=29), "BATCH-LKO-B01", 3.9),
        ("Ram Manohar Lohia Hospital", "Lucknow", "B+", today - timedelta(days=20), today + timedelta(days=15), "BATCH-LKO-B02", 4.0),
        ("Ram Manohar Lohia Hospital", "Lucknow", "AB+", today - timedelta(days=10), today + timedelta(days=25), "BATCH-LKO-AB01", 4.0),
        ("Sahara Hospital Blood Bank", "Lucknow", "A+", today - timedelta(days=5), today + timedelta(days=30), "BATCH-LKO-A01", 4.0),
    ]

    for bank_name, city, b_group, coll_date, exp_date, batch_no, temp in inventory_items:
        cursor.execute("""
            INSERT INTO blood_inventory (blood_bank_name, city, blood_group, units_available, collection_date, expiry_date, batch_number, storage_temp_celsius, status)
            VALUES (?, ?, ?, 1, ?, ?, ?, ?, 'available')
        """, (bank_name, city, b_group, str(coll_date), str(exp_date), batch_no, temp))

    # 3. SEED LIVE EMERGENCY REQUESTS (Simulating hospitals asking for blood)
    # Emergency 1: Delhi Apollo
    cursor.execute("""
        INSERT INTO blood_requests (hospital_id, patient_name, patient_ipd_number, blood_group, units_requested, urgency_level, doctor_name, doctor_mci_id, doctor_slip_url, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (1, "Aniket Choudhary", "IPD-TRAUMA-402", "O-", 2, "emergency", "Dr. V. K. Sharma", "MCI-DL-2015-77291", "cloud_storage://slips/slip_emg_402.pdf", "pending"))

    # Emergency 2: Jaipur SMS Hospital (For Travel / Roaming Donor Testing)
    cursor.execute("""
        INSERT INTO blood_requests (hospital_id, patient_name, patient_ipd_number, blood_group, units_requested, urgency_level, doctor_name, doctor_mci_id, doctor_slip_url, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (3, "Kailash Meena", "IPD-TRAUMA-JP-104", "O-", 1, "emergency", "Dr. Ashok Saxena", "RMC-2012-4821", "cloud_storage://slips/jaipur_emg_104.pdf", "pending"))

    # 4. LOG INITIAL AUDIT ENTRY
    cursor.execute("""
        INSERT INTO audit_logs (action, performed_by, details)
        VALUES (?, ?, ?)
    """, ("SYSTEM_INITIALIZATION", "SYSTEM_ENGINE", "Cloud database initialized with multi-role users, inventory and emergency triage queue."))

    conn.commit()
    conn.close()
    print("[DB] Initial sample data seeded successfully!")

if __name__ == "__main__":
    init_database()
    seed_sample_data()
