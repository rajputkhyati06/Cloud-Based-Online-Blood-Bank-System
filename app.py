import os
import sqlite3
import hashlib
import re
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
import io

# -----------------------------------------------------------------------------
# RECOGNIZED INDIAN CITIES WHITELIST FOR GEOGRAPHIC VALIDATION
# Prevents gibberish strings (e.g. 'kkwhdwj') from polluting system state
# -----------------------------------------------------------------------------
VALID_INDIAN_CITIES = {
    'delhi', 'new delhi', 'noida', 'greater noida', 'gurgaon', 'gurugram', 'ghaziabad', 'faridabad',
    'jaipur', 'jodhpur', 'udaipur', 'kota', 'ajmer', 'bikaner',
    'lucknow', 'kanpur', 'agra', 'varanasi', 'prayagraj', 'allahabad', 'meerut', 'aligarh', 'bareilly', 'gorakhpur',
    'mumbai', 'pune', 'nagpur', 'thane', 'nashik', 'aurangabad',
    'chandigarh', 'amritsar', 'ludhiana', 'jalandhar', 'panchkula', 'mohali',
    'bangalore', 'bengaluru', 'mysore', 'mangalore',
    'hyderabad', 'visakhapatnam', 'vijayawada',
    'chennai', 'coimbatore', 'madurai',
    'kolkata', 'howrah',
    'ahmedabad', 'surat', 'vadodara', 'rajkot',
    'bhopal', 'indore', 'gwalior', 'jabalpur',
    'patna', 'gaya', 'muzaffarpur',
    'ranchi', 'jamshedpur',
    'dehradun', 'haridwar', 'rishikesh',
    'shimla', 'jammu', 'srinagar',
    'guwahati', 'bhubaneswar', 'cuttack', 'raipur', 'all'
}

def validate_city_name(city_name: str):
    """Checks if city is a valid recognized Indian city and not random gibberish like 'kkwhdwj'."""
    if not city_name:
        return False, None
    clean = city_name.strip()
    if len(clean) < 2 or len(clean) > 40:
        return False, None
    if not re.match(r'^[a-zA-Z\s\-]+$', clean):
        return False, None
    
    clean_lower = clean.lower()
    if clean_lower in VALID_INDIAN_CITIES:
        return True, clean.title() if clean_lower != 'all' else 'All'
    return False, None

app = Flask(__name__)
app.secret_key = "cloud_blood_bank_super_secret_production_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "database", "cloud_blood_bank.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------------------------------------------------------
# DATABASE CONNECTION HELPER
# -----------------------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# -----------------------------------------------------------------------------
# PUBLIC ROUTE: HOME PAGE & LIVE INVENTORY SEARCH
# -----------------------------------------------------------------------------
@app.route('/')
def index():
    search_city = request.args.get('city', '').strip()
    search_bg = request.args.get('blood_group', '').strip().replace(' ', '+')
    
    # Regional Hub filter with validation against gibberish
    if search_city:
        is_valid, formatted_city = validate_city_name(search_city)
        if is_valid:
            current_city = formatted_city
        else:
            flash(f"'{search_city}' is not a recognized city in our network. Showing default hub (Delhi).", "warning")
            current_city = 'Delhi'
    else:
        current_city = 'Delhi'
    
    all_bgs = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    if search_bg and search_bg in all_bgs:
        display_bgs = [search_bg]
    else:
        display_bgs = all_bgs
        search_bg = ''
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Fetch Live Stock Summary for the selected Regional Hub (or All)
    if current_city == 'All':
        cursor.execute("""
            SELECT blood_group, COUNT(*) as total_units, MIN(expiry_date) as earliest_expiry
            FROM blood_inventory
            WHERE status = 'available'
            GROUP BY blood_group
        """)
    else:
        cursor.execute("""
            SELECT blood_group, COUNT(*) as total_units, MIN(expiry_date) as earliest_expiry
            FROM blood_inventory
            WHERE status = 'available' AND LOWER(city) = LOWER(?)
            GROUP BY blood_group
        """, (current_city,))
    stock_rows = cursor.fetchall()
    stock_dict = {row['blood_group']: row for row in stock_rows}
    
    # 2. Fetch Facility-wise breakdown per blood group for the selected city
    if current_city == 'All':
        cursor.execute("""
            SELECT blood_bank_name, city, blood_group, COUNT(*) as units, MIN(expiry_date) as earliest_expiry
            FROM blood_inventory
            WHERE status = 'available'
            GROUP BY blood_bank_name, city, blood_group
            ORDER BY units DESC
        """)
    else:
        cursor.execute("""
            SELECT blood_bank_name, city, blood_group, COUNT(*) as units, MIN(expiry_date) as earliest_expiry
            FROM blood_inventory
            WHERE status = 'available' AND LOWER(city) = LOWER(?)
            GROUP BY blood_bank_name, city, blood_group
            ORDER BY units DESC
        """, (current_city,))
    facility_rows = cursor.fetchall()
    
    facilities_by_bg = {}
    for f in facility_rows:
        bg = f['blood_group']
        if bg not in facilities_by_bg:
            facilities_by_bg[bg] = []
        facilities_by_bg[bg].append(f)
    
    # 3. Fetch Active Critical Emergencies (Pending requests)
    cursor.execute("""
        SELECT r.*, h.hospital_name, h.emergency_desk_contact, h.google_maps_url
        FROM blood_requests r
        JOIN hospitals h ON r.hospital_id = h.hospital_id
        WHERE r.status = 'pending' AND r.urgency_level = 'emergency'
        ORDER BY r.created_at DESC LIMIT 3
    """)
    pending_emergencies = cursor.fetchall()
    
    conn.close()
    return render_template('index.html', 
                           current_city=current_city,
                           search_city=search_city, 
                           search_bg=search_bg,
                           display_bgs=display_bgs,
                           stock_dict=stock_dict,
                           facilities_by_bg=facilities_by_bg,
                           pending_emergencies=pending_emergencies)

# -----------------------------------------------------------------------------
# AUTHENTICATION: LOGIN & REGISTER
# -----------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_type = request.form.get('login_type', 'standard')
        email = request.form.get('email', '').strip()
        license_number = request.form.get('license_number', '').strip()
        password = request.form.get('password', '').strip()
        pwd_hash = hash_password(password)
        
        conn = get_db()
        cursor = conn.cursor()
        
        # 1. HOSPITAL VERIFICATION LOGIN (Requires Valid Registered Medical License)
        if login_type == 'hospital' or license_number:
            if not license_number:
                conn.close()
                flash("Medical License ID is required for Hospital Emergency Desk Authentication.", "danger")
                return render_template('login.html', active_tab='hospital')
                
            cursor.execute("""
                SELECT h.*, u.user_id, u.email, u.phone, u.city, u.role, u.password_hash
                FROM hospitals h
                JOIN users u ON h.user_id = u.user_id
                WHERE LOWER(h.license_number) = LOWER(?) AND u.password_hash = ?
            """, (license_number, pwd_hash))
            hospital_user = cursor.fetchone()
            
            if not hospital_user:
                # Check if license exists at all in the database registry
                cursor.execute("SELECT * FROM hospitals WHERE LOWER(license_number) = LOWER(?)", (license_number,))
                lic_match = cursor.fetchone()
                conn.close()
                if not lic_match:
                    flash(f"Security Alert: Medical License '{license_number}' is NOT registered in State Health Authority Registry! Access Denied.", "danger")
                else:
                    flash(f"Authentication Failed: Password does not match registered credentials for {lic_match['hospital_name']}.", "danger")
                return render_template('login.html', active_tab='hospital', fill_license=license_number)
            
            # Successfully Verified! Auto-resolve hospital name from the verified license
            hospital_name = hospital_user['hospital_name']
            session['user_id'] = hospital_user['user_id']
            session['full_name'] = hospital_name
            session['hospital_name'] = hospital_name
            session['license_number'] = hospital_user['license_number']
            session['role'] = 'hospital'
            session['city'] = hospital_user['city']
            conn.close()
            
            flash(f"Medical License Verified ({hospital_user['license_number']})! Welcome to {hospital_name} Emergency Triage Portal.", "success")
            return redirect(url_for('hospital_dashboard'))
            
        # 2. STANDARD LOGIN (Donor / Admin)
        else:
            cursor.execute("SELECT * FROM users WHERE email = ? AND password_hash = ?", (email, pwd_hash))
            user = cursor.fetchone()
            
            if user:
                # If someone tries to log into a Hospital account via standard form without license:
                if user['role'] == 'hospital':
                    # Fetch hospital's license to guide them
                    cursor.execute("SELECT * FROM hospitals WHERE user_id = ?", (user['user_id'],))
                    h_info = cursor.fetchone()
                    conn.close()
                    flash(f"Hospital Security Verification Required: Please switch to 'Hospital Login' tab and enter your Medical License ID ({h_info['license_number'] if h_info else ''}).", "warning")
                    return render_template('login.html', active_tab='hospital', fill_email=email, fill_license=h_info['license_number'] if h_info else '')
                
                session['user_id'] = user['user_id']
                session['full_name'] = user['full_name']
                session['role'] = user['role']
                session['city'] = user['city']
                conn.close()
                flash(f"Welcome back, {user['full_name']}!", "success")
                
                if user['role'] == 'donor':
                    return redirect(url_for('donor_dashboard'))
                elif user['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
            else:
                conn.close()
                flash("Invalid email or password. Please try again.", "danger")
                
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form.get('role')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        city = request.form.get('city')
        password = request.form.get('password')
        pwd_hash = hash_password(password)
        
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (full_name, email, password_hash, role, phone, city, address)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (full_name, email, pwd_hash, role, phone, city, f"City: {city}"))
            user_id = cursor.lastrowid
            
            if role == 'donor':
                blood_group = request.form.get('blood_group')
                night_avail = 1 if request.form.get('night_available') else 0
                cursor.execute("""
                    INSERT INTO donors (user_id, blood_group, is_available, night_emergency_available, total_donations)
                    VALUES (?, ?, 1, ?, 0)
                """, (user_id, blood_group, night_avail))
            elif role == 'hospital':
                license_num = request.form.get('license_number', '').strip().upper()
                emergency_person = request.form.get('emergency_person', 'Emergency Desk').strip()
                
                # Anti-Fraud Verification: Govt Medical License format check
                if not license_num or len(license_num) < 8 or '-' not in license_num:
                    conn.close()
                    flash("Anti-Fraud Security Alert: Invalid Medical Council License! Must follow authorized State Health Directorate format (e.g. HOSP-DL-2024-8841 or RAJ-MCI-HOSP-1994-082).", "danger")
                    return redirect(url_for('register'))

                cursor.execute("""
                    INSERT INTO hospitals (user_id, hospital_name, license_number, emergency_desk_contact, emergency_desk_person, google_maps_url, trust_score)
                    VALUES (?, ?, ?, ?, ?, ?, 100)
                """, (user_id, full_name, license_num, phone, emergency_person, f"https://maps.google.com/?q={full_name}"))
            
            conn.commit()
            flash("Account registered successfully! Please sign in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("An account with this email already exists.", "danger")
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for('index'))

# -----------------------------------------------------------------------------
# DONOR PORTAL
# -----------------------------------------------------------------------------
@app.route('/donor/dashboard')
def donor_dashboard():
    if session.get('role') != 'donor':
        flash("Unauthorized access. Please log in as a Donor.", "danger")
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Fetch donor profile
    cursor.execute("""
        SELECT d.*, u.full_name, u.email, u.phone, u.city 
        FROM donors d 
        JOIN users u ON d.user_id = u.user_id 
        WHERE d.user_id = ?
    """, (session['user_id'],))
    donor = dict(cursor.fetchone())
    
    # 2. Calculate 90-Day Medical Cooldown Timer
    today = datetime.now().date()
    days_remaining = 0
    next_eligible_date = today
    if donor.get('last_donated_date'):
        try:
            last_date = datetime.strptime(str(donor['last_donated_date']), "%Y-%m-%d").date()
            next_eligible_date = last_date + timedelta(days=90)
            days_remaining = max(0, (next_eligible_date - today).days)
        except Exception:
            days_remaining = 0
            
    is_eligible_now = (days_remaining == 0)

    # 3. Gamification: Karma Points & Milestone Rewards
    total_donations = donor.get('total_donations', 0)
    karma_points = total_donations * 100
    
    # Rewards unlocks
    rewards = {
        'bronze_badge': total_donations >= 1,
        'recharge_50': 'HERO-REC-50' if total_donations >= 1 else None,
        'silver_badge': total_donations >= 3,
        'pharmacy_20': 'PHARMA-20-HERO' if total_donations >= 3 else None,
        'gold_badge': total_donations >= 5,
        'free_health_checkup': 'VIP-CHECKUP-FREE' if total_donations >= 5 else None,
        'vip_family_pass': 'VIP-FAMILY-PASS-2026' if total_donations >= 5 else None
    }
    
    # 4. Travel / Roaming Mode: Determine Active Location
    home_city = donor['city']
    city_param = request.args.get('city', '').strip()
    if city_param:
        is_valid, formatted_city = validate_city_name(city_param)
        if is_valid:
            active_city = formatted_city
            session['travel_city'] = active_city
            if active_city != home_city and active_city != 'All':
                flash(f"Roaming Radar switched to {active_city}! Scanning local trauma emergencies.", "info")
            elif active_city == home_city:
                flash(f"Returned to Home Base ({home_city}).", "success")
        else:
            flash(f"⚠️ Invalid City: '{city_param}' is not a recognized city in our network! Please enter a valid Indian city (e.g. Delhi, Jaipur, Mumbai, Chandigarh).", "danger")
            active_city = session.get('travel_city', home_city)
    else:
        active_city = session.get('travel_city', home_city)
        
    # 5. Fetch Nearby Blood Banks in Active / Roaming City for Voluntary Walk-In Donation
    cursor.execute("""
        SELECT DISTINCT blood_bank_name, city, 
               CASE WHEN LOWER(city) = 'jaipur' THEN '+91-141-2560291'
                    WHEN LOWER(city) = 'noida' THEN '+91-120-2444444'
                    WHEN LOWER(city) = 'lucknow' THEN '+91-522-2257540'
                    WHEN LOWER(city) = 'mumbai' THEN '+91-22-24146990'
                    ELSE '+91-11-23711551' END as phone, 
               'Open 24x7 for Donors' as timing
        FROM blood_inventory
        WHERE LOWER(city) = LOWER(?)
        LIMIT 3
    """, (active_city,))
    nearby_blood_banks = cursor.fetchall()
    if not nearby_blood_banks:
        cursor.execute("""
            SELECT DISTINCT blood_bank_name, city, '+91-11-23711551' as phone, 'Open 24x7 for Donors' as timing
            FROM blood_inventory LIMIT 3
        """)
        nearby_blood_banks = cursor.fetchall()
    
    # 6. Check if this donor currently has an ACTIVE IN-TRANSIT or VOLUNTEER MISSION
    cursor.execute("""
        SELECT r.*, h.hospital_name, h.emergency_desk_contact, h.emergency_desk_person, h.google_maps_url, u.city as hospital_city
        FROM blood_requests r
        JOIN hospitals h ON r.hospital_id = h.hospital_id
        JOIN users u ON h.user_id = u.user_id
        WHERE r.assigned_donor_id = ? AND r.donor_status IN ('donor_applied', 'doctor_accepted', 'in_transit')
        ORDER BY r.request_id DESC
        LIMIT 1
    """, (donor['donor_id'],))
    active_mission = cursor.fetchone()

    mission_req_id = active_mission['request_id'] if active_mission else -1

    # 7. Fetch Open Emergency Alerts (Type 1: Critical Emergency SOS)
    cursor.execute("""
        SELECT r.*, h.hospital_name, h.emergency_desk_contact, h.emergency_desk_person, h.google_maps_url, u.city as hospital_city
        FROM blood_requests r
        JOIN hospitals h ON r.hospital_id = h.hospital_id
        JOIN users u ON h.user_id = u.user_id
        WHERE r.status = 'pending' AND r.urgency_level = 'emergency'
          AND (r.donor_status IS NULL OR r.donor_status = 'searching')
          AND r.request_id != ?
          AND (LOWER(u.city) = LOWER(?) OR ? = 'All')
          AND (r.blood_group = ? OR ? = 'O-')
        ORDER BY r.created_at DESC
    """, (mission_req_id, active_city, active_city, donor['blood_group'], donor['blood_group']))
    emergency_alerts = cursor.fetchall()

    # 7b. Fetch Open Hospital Blood Bank Restocking Drives (Type 2: Voluntary Appeals)
    cursor.execute("""
        SELECT r.*, h.hospital_name, h.emergency_desk_contact, h.emergency_desk_person, h.google_maps_url, u.city as hospital_city
        FROM blood_requests r
        JOIN hospitals h ON r.hospital_id = h.hospital_id
        JOIN users u ON h.user_id = u.user_id
        WHERE r.status = 'pending' AND r.urgency_level = 'standard'
          AND (r.donor_status IS NULL OR r.donor_status = 'searching')
          AND r.request_id != ?
          AND (LOWER(u.city) = LOWER(?) OR ? = 'All')
          AND (r.blood_group = ? OR r.blood_group = 'All' OR ? = 'O-')
        ORDER BY r.created_at DESC
    """, (mission_req_id, active_city, active_city, donor['blood_group'], donor['blood_group']))
    restock_drives = cursor.fetchall()

    # 8. Fetch All Earned Certificates from the Vault with Formal Date Formatting
    cursor.execute("""
        SELECT * FROM donor_certificates 
        WHERE donor_id = ? 
        ORDER BY issue_date DESC, certificate_id DESC
    """, (donor['donor_id'],))
    raw_certs = cursor.fetchall()
    
    certificates_vault = []
    for c in raw_certs:
        c_dict = dict(c)
        try:
            c_dict['formatted_date'] = datetime.strptime(str(c_dict['issue_date']), '%Y-%m-%d').strftime('%d %B %Y')
        except Exception:
            c_dict['formatted_date'] = str(c_dict['issue_date'])
        certificates_vault.append(c_dict)
    
    cert_count = len(certificates_vault)
    
    # Milestone calculation strictly based on Certificates Earned:
    # 5 Certificates = VIP Zero-Queue Family Pass
    # 10 Certificates = 50% Flat Off Pharmacy Medicine Card
    vip_family_pass_unlocked = (cert_count >= 5)
    pharmacy_50_unlocked = (cert_count >= 10)
    
    conn.close()
    return render_template('donor_dashboard.html', 
                           donor=donor, 
                           home_city=home_city,
                           active_city=active_city,
                           emergency_alerts=emergency_alerts,
                           restock_drives=restock_drives,
                           active_mission=active_mission,
                           certificates_vault=certificates_vault,
                           cert_count=cert_count,
                           vip_family_pass_unlocked=vip_family_pass_unlocked,
                           pharmacy_50_unlocked=pharmacy_50_unlocked,
                           days_remaining=days_remaining,
                           next_eligible_date=next_eligible_date,
                           is_eligible_now=is_eligible_now,
                           nearby_blood_banks=nearby_blood_banks)

@app.route('/donor/accept-emergency/<int:request_id>', methods=['POST'])
def accept_emergency(request_id):
    """When a donor clicks 'I Am Coming!' or volunteers for an emergency/restock call."""
    if session.get('role') != 'donor':
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT donor_id, blood_group FROM donors WHERE user_id = ?", (session['user_id'],))
    donor = cursor.fetchone()
    
    cursor.execute("""
        SELECT r.*, h.hospital_name 
        FROM blood_requests r
        JOIN hospitals h ON r.hospital_id = h.hospital_id
        WHERE r.request_id = ?
    """, (request_id,))
    req = cursor.fetchone()
    
    if req:
        # Step 1 of Handshake: Donor expresses readiness -> donor_status = 'donor_applied'
        cursor.execute("""
            UPDATE blood_requests 
            SET assigned_donor_id = ?, donor_status = 'donor_applied' 
            WHERE request_id = ?
        """, (donor['donor_id'], request_id))
        
        cursor.execute("""
            INSERT INTO audit_logs (action, performed_by, details)
            VALUES (?, ?, ?)
        """, ("DONOR_VOLUNTEERED", session.get('full_name'), f"Donor #{donor['donor_id']} volunteered for Request #{request_id} at {req['hospital_name']}. Awaiting doctor confirmation."))
        
        conn.commit()
        flash(f"Noble Commitment! {req['hospital_name']} Emergency Desk has been alerted that you ({session.get('full_name')}) are volunteering. Please stand by while the attending doctor confirms your arrival slot.", "success")
        
    conn.close()
    return redirect(url_for('donor_dashboard'))

@app.route('/hospital/accept-donor/<int:request_id>', methods=['POST'])
def hospital_accept_donor(request_id):
    """Step 2 of Handshake: Attending Doctor clicks 'Accept Donor' -> gives donor green signal to proceed."""
    if session.get('role') != 'hospital':
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, u.full_name as donor_name, d.donor_id
        FROM blood_requests r
        JOIN donors d ON r.assigned_donor_id = d.donor_id
        JOIN users u ON d.user_id = u.user_id
        WHERE r.request_id = ?
    """, (request_id,))
    req = cursor.fetchone()
    
    if req:
        cursor.execute("UPDATE blood_requests SET donor_status = 'doctor_accepted' WHERE request_id = ?", (request_id,))
        cursor.execute("""
            INSERT INTO audit_logs (action, performed_by, details)
            VALUES (?, ?, ?)
        """, ("DOCTOR_CONFIRMED_DONOR", session.get('full_name'), f"Attending Doctor accepted Donor {req['donor_name']} for Req #{request_id}. Green signal sent."))
        conn.commit()
        flash(f"Volunteer Donor {req['donor_name']} Accepted! Green signal dispatched to donor. They have been instructed to proceed immediately to your Emergency Room.", "success")
    
    conn.close()
    return redirect(url_for('hospital_dashboard'))

@app.route('/hospital/reject-donor/<int:request_id>', methods=['POST'])
def hospital_reject_donor(request_id):
    """Attending Doctor declines / rejects a volunteer donor, reopening requisition to other donors."""
    if session.get('role') != 'hospital':
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, u.full_name as donor_name 
        FROM blood_requests r
        JOIN donors d ON r.assigned_donor_id = d.donor_id
        JOIN users u ON d.user_id = u.user_id
        WHERE r.request_id = ?
    """, (request_id,))
    req = cursor.fetchone()
    
    if req:
        donor_name = req['donor_name']
        # Reset requisition back to searching mode
        cursor.execute("UPDATE blood_requests SET assigned_donor_id = NULL, donor_status = 'searching' WHERE request_id = ?", (request_id,))
        cursor.execute("""
            INSERT INTO audit_logs (action, performed_by, details)
            VALUES (?, ?, ?)
        """, ("DOCTOR_DECLINED_DONOR", session.get('full_name'), f"Doctor declined volunteer {donor_name} for Req #{request_id}. Reopened requisition to queue."))
        conn.commit()
        flash(f"Volunteer offer from {donor_name} was declined. Requisition #REQ-{request_id} has been reopened to find another matching donor.", "info")
    
    conn.close()
    return redirect(url_for('hospital_dashboard'))

@app.route('/hospital/mark-donated/<int:request_id>', methods=['POST'])
def hospital_mark_donated(request_id):
    """Step 3 of Handshake: Hospital verifies blood collection -> issues Life-Saver Certificate & locks 90-day cooldown."""
    if session.get('role') != 'hospital':
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    today_str = str(datetime.now().date())
    
    cursor.execute("SELECT * FROM blood_requests WHERE request_id = ?", (request_id,))
    req = cursor.fetchone()
    
    if req and req['assigned_donor_id']:
        donor_id = req['assigned_donor_id']
        
        # 1. Update donor: +1 donation, update last_donated_date to start 90-day cooldown timer
        cursor.execute("""
            UPDATE donors 
            SET total_donations = total_donations + 1,
                last_donated_date = ?
            WHERE donor_id = ?
        """, (today_str, donor_id))
        
        # 2. Update request status to 'donated'
        cursor.execute("UPDATE blood_requests SET donor_status = 'donated' WHERE request_id = ?", (request_id,))
        
        # 3. Add blood bag to inventory
        expiry_str = str(datetime.now().date() + timedelta(days=35))
        batch_no = f"EMG-COL-{datetime.now().strftime('%Y%m%d%H%M')}"
        cursor.execute("""
            INSERT INTO blood_inventory (blood_bank_name, blood_group, units_available, collection_date, expiry_date, batch_number, storage_temp_celsius, status, city)
            VALUES (?, ?, 1, ?, ?, ?, 4.0, 'available', ?)
        """, (session.get('full_name', 'Hospital Blood Center'), req['blood_group'], today_str, expiry_str, batch_no, session.get('city', 'Delhi')))
        
        # 4. Generate donor certificate entry (Tag as Emergency or Voluntary based on requisition)
        cert_type = 'emergency' if req['urgency_level'] == 'emergency' else 'voluntary'
        cert_code = f"CERT-{'EMG' if cert_type == 'emergency' else 'VOL'}-{donor_id:04d}-{request_id:04d}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        cursor.execute("""
            INSERT INTO donor_certificates (donor_id, blood_group, recipient_hospital, certificate_code, certificate_type, patient_name)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (donor_id, req['blood_group'], session.get('full_name', 'Indraprastha Apollo Hospital'), cert_code, cert_type, req['patient_name']))
        
        cursor.execute("""
            INSERT INTO audit_logs (action, performed_by, details)
            VALUES (?, ?, ?)
        """, ("DONATION_CONFIRMED_BY_HOSPITAL", session.get('full_name'), f"Blood donation confirmed for Req #{request_id} by Donor #{donor_id}. Certificate #{cert_code} issued."))

        conn.commit()
        flash(f"Blood Donation Verified & Confirmed! Life-Saver Certificate issued to Donor #{donor_id}'s vault, and 90-day safe cooldown initiated.", "success")
        
    conn.close()
    return redirect(url_for('hospital_dashboard'))

@app.route('/hospital/cancel-request/<int:request_id>', methods=['POST'])
def cancel_request(request_id):
    """Allows hospital to delete / cancel an open emergency or restock requisition."""
    if session.get('role') != 'hospital':
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT hospital_id FROM hospitals WHERE user_id = ?", (session['user_id'],))
    hospital = cursor.fetchone()
    
    cursor.execute("SELECT * FROM blood_requests WHERE request_id = ? AND hospital_id = ?", (request_id, hospital['hospital_id']))
    req = cursor.fetchone()
    
    if req:
        cursor.execute("DELETE FROM blood_requests WHERE request_id = ?", (request_id,))
        cursor.execute("""
            INSERT INTO audit_logs (action, performed_by, details)
            VALUES (?, ?, ?)
        """, ("REQUISITION_DELETED", session.get('full_name'), f"Cancelled and deleted Requisition #{request_id} ({req['patient_name']}, {req['blood_group']})."))
        conn.commit()
        flash(f"Requisition #REQ-{request_id} for {req['patient_name']} ({req['blood_group']}) has been successfully cancelled & deleted from the live queue.", "warning")
    else:
        flash("Requisition not found or unauthorized.", "danger")
        
    conn.close()
    return redirect(url_for('hospital_dashboard'))

@app.route('/donor/log-voluntary-donation', methods=['POST'])
def log_voluntary_donation():
    """Simulates voluntary walk-in donation at a blood bank, awarding points, certificate & cooldown."""
    if session.get('role') != 'donor':
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    today_str = str(datetime.now().date())
    
    # Increment donations & set last_donated_date to today
    cursor.execute("""
        UPDATE donors 
        SET total_donations = total_donations + 1,
            last_donated_date = ?
        WHERE user_id = ?
    """, (today_str, session['user_id']))
    
    # Automatically add a fresh unit to the Blood Bank Cold Storage Inventory!
    cursor.execute("SELECT blood_group FROM donors WHERE user_id = ?", (session['user_id'],))
    b_group = cursor.fetchone()[0]
    expiry_str = str(datetime.now().date() + timedelta(days=35))
    batch_no = f"VOL-{datetime.now().strftime('%Y%m%d%H%M')}"
    
    cursor.execute("""
        INSERT INTO blood_inventory (blood_bank_name, blood_group, units_available, collection_date, expiry_date, batch_number, storage_temp_celsius, status)
        VALUES ('Central Red Cross Blood Bank', ?, 1, ?, ?, ?, 4.0, 'available')
    """, (b_group, today_str, expiry_str, batch_no))
    
    conn.commit()
    conn.close()
    
    flash(f"Noble Deed Recorded! +100 Karma Points awarded! 1 Unit of {b_group} added to Cold Storage Inventory. Life-Saver Certificate unlocked!", "success")
    return redirect(url_for('donor_dashboard'))

@app.route('/donor/update-status', methods=['POST'])
def update_donor_status():
    if session.get('role') != 'donor':
        return redirect(url_for('login'))
        
    is_avail = 1 if request.form.get('is_available') else 0
    night_avail = 1 if request.form.get('night_available') else 0
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE donors 
        SET is_available = ?, night_emergency_available = ? 
        WHERE user_id = ?
    """, (is_avail, night_avail, session['user_id']))
    conn.commit()
    conn.close()
    
    flash("Your availability preferences have been updated in real-time.", "success")
    return redirect(url_for('donor_dashboard'))

@app.route('/donor/upload-cert', methods=['POST'])
def upload_donor_cert():
    if session.get('role') != 'donor':
        return redirect(url_for('login'))
        
    file = request.files.get('certificate_file')
    if file and file.filename != '':
        filename = f"cert_user_{session['user_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE donors SET fitness_certificate_url = ? WHERE user_id = ?", (filename, session['user_id']))
        conn.commit()
        conn.close()
        flash("Medical fitness report successfully uploaded and archived to Cloud Storage!", "success")
    return redirect(url_for('donor_dashboard'))

# -----------------------------------------------------------------------------
# HOSPITAL PORTAL
# -----------------------------------------------------------------------------
@app.route('/hospital/dashboard')
def hospital_dashboard():
    if session.get('role') != 'hospital':
        flash("Unauthorized access. Please log in as a Hospital.", "danger")
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    
    # Fetch hospital profile
    cursor.execute("""
        SELECT h.*, u.city, u.email, u.phone 
        FROM hospitals h
        JOIN users u ON h.user_id = u.user_id
        WHERE h.user_id = ?
    """, (session['user_id'],))
    hospital = cursor.fetchone()
    
    # Fetch all requests raised by this hospital WITH donor info
    cursor.execute("""
        SELECT r.*, d.blood_group as donor_bg, d.total_donations as donor_donations,
               u.full_name as donor_name, u.phone as donor_phone
        FROM blood_requests r
        LEFT JOIN donors d ON r.assigned_donor_id = d.donor_id
        LEFT JOIN users u ON d.user_id = u.user_id
        WHERE r.hospital_id = ? 
        ORDER BY r.created_at DESC
    """, (hospital['hospital_id'],))
    requests = cursor.fetchall()
    
    # Calculate Enterprise Summary Metrics
    total_reqs = len(requests)
    under_review = sum(1 for r in requests if r['status'] == 'pending')
    in_transit_donors = sum(1 for r in requests if r['donor_status'] in ('donor_applied', 'doctor_accepted', 'in_transit'))
    fulfilled_count = sum(1 for r in requests if r['status'] in ('approved', 'dispatched') or r['donor_status'] == 'donated')
    
    stats = {
        'total': total_reqs,
        'pending': under_review,
        'in_transit': in_transit_donors,
        'fulfilled': fulfilled_count
    }
    
    # Fetch Internal Hospital Blood Bank Cold Storage (Units available per blood group in this hospital)
    all_bgs = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    cursor.execute("""
        SELECT blood_group, COUNT(*) as units
        FROM blood_inventory
        WHERE status = 'available' AND (LOWER(blood_bank_name) LIKE LOWER(?) OR LOWER(city) = LOWER(?))
        GROUP BY blood_group
    """, (f"%{hospital['hospital_name']}%", hospital['city']))
    hosp_stock_rows = cursor.fetchall()
    hosp_stock = {bg: 0 for bg in all_bgs}
    for row in hosp_stock_rows:
        if row['blood_group'] in hosp_stock:
            hosp_stock[row['blood_group']] = row['units']

    # Active incoming donor handshakes waiting for doctor review or arrival
    incoming_donors = [r for r in requests if r['donor_status'] in ('donor_applied', 'doctor_accepted')]

    conn.close()
    return render_template('hospital_dashboard.html', hospital=hospital, requests=requests, stats=stats, hosp_stock=hosp_stock, incoming_donors=incoming_donors)

@app.route('/hospital/create-request', methods=['POST'])
def create_request():
    """Type 1: Critical Emergency SOS Requisition (Mandates Doctor Prescription Slip)"""
    if session.get('role') != 'hospital':
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT h.hospital_id, h.hospital_name, u.city 
        FROM hospitals h 
        JOIN users u ON h.user_id = u.user_id 
        WHERE h.user_id = ?
    """, (session['user_id'],))
    hospital = cursor.fetchone()
    hospital_id = hospital['hospital_id']
    
    patient_name = request.form.get('patient_name', '').strip()
    patient_ipd = request.form.get('patient_ipd', '').strip()
    blood_group = request.form.get('blood_group', '').strip()
    units = int(request.form.get('units', 1))
    doctor_name = request.form.get('doctor_name', '').strip()
    doctor_mci_id = request.form.get('doctor_mci_id', '').strip().upper()
    
    # Anti-Fraud Verification: Doctor MCI Registration ID check
    if not doctor_mci_id or len(doctor_mci_id) < 6 or '-' not in doctor_mci_id:
        conn.close()
        flash("Anti-Fraud Security Alert: Valid Doctor Medical Council Registration ID (MCI/NMC) is mandatory (e.g. MCI-DL-2018-99410)!", "danger")
        return redirect(url_for('hospital_dashboard'))
    
    # MANDATORY DOCTOR PRESCRIPTION SLIP VERIFICATION
    slip_file = request.files.get('doctor_slip')
    if not slip_file or slip_file.filename == '':
        conn.close()
        flash("Requisition Blocked: Attending Doctor's signed prescription paper (PDF/Image) is strictly mandatory for Emergency requisitions!", "danger")
        return redirect(url_for('hospital_dashboard'))
        
    slip_filename = f"slip_{hospital_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{slip_file.filename}"
    slip_file.save(os.path.join(app.config['UPLOAD_FOLDER'], slip_filename))
        
    cursor.execute("""
        INSERT INTO blood_requests (hospital_id, patient_name, patient_ipd_number, blood_group, units_requested, urgency_level, doctor_name, doctor_mci_id, doctor_slip_url, status, donor_status)
        VALUES (?, ?, ?, ?, ?, 'emergency', ?, ?, ?, 'pending', 'searching')
    """, (hospital_id, patient_name, patient_ipd, blood_group, units, doctor_name, doctor_mci_id, slip_filename))
    
    cursor.execute("""
        INSERT INTO audit_logs (action, performed_by, details)
        VALUES (?, ?, ?)
    """, ("EMERGENCY_SOS_RAISED", hospital['hospital_name'], f"Emergency SOS raised for {patient_name} ({blood_group}, {units} units). Signed Doctor Slip archived."))

    conn.commit()
    conn.close()
    
    flash(f"Critical Emergency SOS Requisition raised! All eligible {blood_group} donors in {hospital['city']} have been alerted on their radar.", "success")
    return redirect(url_for('hospital_dashboard'))

@app.route('/hospital/create-restock-drive', methods=['POST'])
def create_restock_drive():
    """Type 2: Hospital Blood Bank Storage Restock Drive (Voluntary Donation Call)"""
    if session.get('role') != 'hospital':
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT h.hospital_id, h.hospital_name, u.city 
        FROM hospitals h 
        JOIN users u ON h.user_id = u.user_id 
        WHERE h.user_id = ?
    """, (session['user_id'],))
    hospital = cursor.fetchone()
    hospital_id = hospital['hospital_id']
    
    blood_group = request.form.get('blood_group', 'All').strip()
    units = int(request.form.get('units', 5))
    drive_title = request.form.get('drive_title', 'Hospital Blood Bank Restocking Drive').strip()
    officer_name = request.form.get('officer_name', 'Blood Bank In-Charge').strip()
    
    cursor.execute("""
        INSERT INTO blood_requests (hospital_id, patient_name, patient_ipd_number, blood_group, units_requested, urgency_level, doctor_name, doctor_mci_id, status, donor_status)
        VALUES (?, ?, 'STORAGE-RESTOCK-DRIVE', ?, ?, 'standard', ?, 'HOSP-BLOOD-BANK', 'pending', 'searching')
    """, (hospital_id, drive_title, blood_group, units, officer_name))
    
    cursor.execute("""
        INSERT INTO audit_logs (action, performed_by, details)
        VALUES (?, ?, ?)
    """, ("RESTOCK_DRIVE_OPENED", hospital['hospital_name'], f"Opened Blood Bank Restock Drive for {units} units of {blood_group}."))

    conn.commit()
    conn.close()
    
    flash(f"Hospital Blood Bank Restocking Call published! Donors in {hospital['city']} can now view and register for walk-in donations.", "success")
    return redirect(url_for('hospital_dashboard'))

# -----------------------------------------------------------------------------
# ADMIN CONSOLE & FIFO DISPATCH LOGIC
# -----------------------------------------------------------------------------
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash("Unauthorized access. Administrator privileges required.", "danger")
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Stock summary for meters
    cursor.execute("""
        SELECT blood_group, COUNT(*) as total_units 
        FROM blood_inventory 
        WHERE status = 'available' 
        GROUP BY blood_group
    """)
    stock_summary = cursor.fetchall()
    
    # 2. Total units & expiring soon count (< 7 days)
    today = datetime.now().date()
    seven_days = today + timedelta(days=7)
    
    cursor.execute("SELECT COUNT(*) FROM blood_inventory WHERE status = 'available'")
    total_stock_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM blood_inventory WHERE status = 'available' AND expiry_date <= ?", (str(seven_days),))
    expiring_soon_count = cursor.fetchone()[0]
    
    # 3. Pending Requisitions
    cursor.execute("""
        SELECT r.*, h.hospital_name, h.emergency_desk_contact
        FROM blood_requests r
        JOIN hospitals h ON r.hospital_id = h.hospital_id
        WHERE r.status = 'pending'
        ORDER BY CASE WHEN r.urgency_level = 'emergency' THEN 0 ELSE 1 END, r.created_at ASC
    """)
    pending_requests = cursor.fetchall()
    
    # 4. Inventory Bags (FIFO sorted by Expiry Date ASC)
    cursor.execute("""
        SELECT * FROM blood_inventory 
        WHERE status = 'available' 
        ORDER BY expiry_date ASC
    """)
    raw_bags = cursor.fetchall()
    
    inventory_bags = []
    for bag in raw_bags:
        b_dict = dict(bag)
        exp = datetime.strptime(b_dict['expiry_date'], "%Y-%m-%d").date()
        b_dict['days_left'] = max(0, (exp - today).days)
        inventory_bags.append(b_dict)
        
    # Chart Data Preparation (PowerBI style analytics)
    all_bgs = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    stock_map = {row['blood_group']: row['total_units'] for row in stock_summary}
    chart_labels = all_bgs
    chart_values = [stock_map.get(bg, 0) for bg in all_bgs]

    # 5. Cloud Telemetry KPIs
    cursor.execute("SELECT COUNT(*) FROM donors")
    total_donors_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM hospitals")
    total_hospitals_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM blood_requests WHERE status = 'approved'")
    total_dispatched_count = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(storage_temp_celsius) FROM blood_inventory WHERE status = 'available'")
    avg_temp_val = cursor.fetchone()[0]
    avg_temp = round(avg_temp_val, 1) if avg_temp_val else 4.0

    # 6. Approved Dispatches History (with Gate-Pass Tokens)
    cursor.execute("""
        SELECT r.*, h.hospital_name, p.token_code, p.issued_timestamp
        FROM blood_requests r
        JOIN hospitals h ON r.hospital_id = h.hospital_id
        LEFT JOIN dispatch_passes p ON r.request_id = p.request_id
        WHERE r.status = 'approved'
        ORDER BY r.created_at DESC
        LIMIT 15
    """)
    approved_dispatches = cursor.fetchall()

    # 7. Registered Hospitals Directory & Trust Scores
    cursor.execute("""
        SELECT h.*, u.city, u.email, u.phone 
        FROM hospitals h
        JOIN users u ON h.user_id = u.user_id
        ORDER BY h.hospital_name ASC
    """)
    hospitals_list = cursor.fetchall()

    # 8. Real-time Security Audit Logs & Forensic Trail
    cursor.execute("""
        SELECT * FROM audit_logs 
        ORDER BY timestamp DESC 
        LIMIT 30
    """)
    audit_logs = cursor.fetchall()
    
    conn.close()
    return render_template('admin_dashboard.html',
                           stock_summary=stock_summary,
                           total_stock_count=total_stock_count,
                           expiring_soon_count=expiring_soon_count,
                           pending_requests=pending_requests,
                           inventory_bags=inventory_bags,
                           chart_labels=chart_labels,
                           chart_values=chart_values,
                           total_donors_count=total_donors_count,
                           total_hospitals_count=total_hospitals_count,
                           total_dispatched_count=total_dispatched_count,
                           avg_temp=avg_temp,
                           approved_dispatches=approved_dispatches,
                           hospitals_list=hospitals_list,
                           audit_logs=audit_logs)

@app.route('/admin/approve/<int:request_id>', methods=['POST'])
def approve_request(request_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM blood_requests WHERE request_id = ?", (request_id,))
    req = cursor.fetchone()
    
    if req:
        # FIFO DISPATCH ALGORITHM:
        # Find the earliest expiring available bag of this blood group
        cursor.execute("""
            SELECT bag_id, batch_number, expiry_date 
            FROM blood_inventory 
            WHERE blood_group = ? AND status = 'available' 
            ORDER BY expiry_date ASC LIMIT 1
        """, (req['blood_group'],))
        assigned_bag = cursor.fetchone()
        
        assigned_bag_id = None
        if assigned_bag:
            assigned_bag_id = assigned_bag['bag_id']
            # Deduct bag from cold storage
            cursor.execute("UPDATE blood_inventory SET status = 'dispatched' WHERE bag_id = ?", (assigned_bag_id,))
        
        # Mark request as approved
        cursor.execute("""
            UPDATE blood_requests 
            SET status = 'approved', dispatch_bag_id = ? 
            WHERE request_id = ?
        """, (assigned_bag_id, request_id))
        
        # Generate Official Digital Gate-Pass Token
        token = f"PASS-{datetime.now().strftime('%Y%m')}-{request_id:04d}"
        qr_payload = f"TOKEN={token}|HOSP={req['hospital_id']}|GROUP={req['blood_group']}|BAG={assigned_bag_id}"
        
        cursor.execute("""
            INSERT OR REPLACE INTO dispatch_passes (request_id, token_code, approved_by, qr_payload)
            VALUES (?, ?, ?, ?)
        """, (request_id, token, session.get('full_name', 'Admin Officer'), qr_payload))
        
        # Security Audit Log
        cursor.execute("""
            INSERT INTO audit_logs (action, performed_by, details)
            VALUES (?, ?, ?)
        """, ("REQUEST_APPROVED_FIFO", session.get('full_name'), f"Req #{request_id} approved. Allocated Bag #{assigned_bag_id} via FIFO."))

        conn.commit()
        flash(f"Requisition #{request_id} APPROVED! Assigned Bag #{assigned_bag_id} via FIFO algorithm. Gate-Pass Token generated.", "success")
        
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reject/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    reason = request.form.get('rejection_reason', 'Verification discrepancy in prescription slip or MCI credentials').strip()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE blood_requests SET status = 'rejected' WHERE request_id = ?", (request_id,))
    cursor.execute("""
        INSERT INTO audit_logs (action, performed_by, details)
        VALUES (?, ?, ?)
    """, ("REQUEST_REJECTED", session.get('full_name', 'Admin Officer'), f"Req #{request_id} rejected. Reason: {reason}"))
    conn.commit()
    conn.close()
    
    flash(f"Requisition #{request_id} rejected. Reason: {reason}", "warning")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add-stock', methods=['POST'])
def add_stock():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    blood_bank_name = request.form.get('blood_bank_name', 'Central Red Cross Blood Bank')
    blood_group = request.form.get('blood_group')
    batch_number = request.form.get('batch_number')
    temp = float(request.form.get('temp', 4.0))
    
    today = datetime.now().date()
    expiry = today + timedelta(days=35) # 35-day rule
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO blood_inventory (blood_bank_name, blood_group, units_available, collection_date, expiry_date, batch_number, storage_temp_celsius, status)
        VALUES (?, ?, 1, ?, ?, ?, ?, 'available')
    """, (blood_bank_name, blood_group, str(today), str(expiry), batch_number, temp))
    
    cursor.execute("""
        INSERT INTO audit_logs (action, performed_by, details)
        VALUES (?, ?, ?)
    """, ("NEW_UNIT_INTAKE", session.get('full_name', 'Admin Officer'), f"Intake of {blood_group} (Batch: {batch_number}, Temp: {temp}°C) recorded in cold storage."))
    
    conn.commit()
    conn.close()
    
    flash(f"New unit of {blood_group} (Batch: {batch_number}) registered in cold storage. Expiry set to {expiry} (35-day rule).", "success")
    return redirect(url_for('admin_dashboard'))

# -----------------------------------------------------------------------------
# DYNAMIC PDF GENERATORS (GATE-PASS & LIFE-SAVER CERTIFICATE)
# -----------------------------------------------------------------------------
@app.route('/download-gatepass/<int:request_id>')
def download_gatepass(request_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, h.hospital_name, h.license_number, p.token_code, p.issued_timestamp, p.approved_by, b.batch_number
        FROM blood_requests r
        JOIN hospitals h ON r.hospital_id = h.hospital_id
        LEFT JOIN dispatch_passes p ON r.request_id = p.request_id
        LEFT JOIN blood_inventory b ON r.dispatch_bag_id = b.bag_id
        WHERE r.request_id = ?
    """, (request_id,))
    item = cursor.fetchone()
    conn.close()
    
    if not item:
        flash("Gate-pass not found.", "danger")
        return redirect(url_for('index'))
        
    # Generate PDF in memory buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor("#B91C1C"), alignment=1)
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.HexColor("#475569"), alignment=1, spaceAfter=15)
    
    story.append(Paragraph("OFFICIAL BLOOD BANK DISPATCH GATE-PASS", title_style))
    story.append(Paragraph(f"TOKEN: <b>{item['token_code'] or 'PASS-CONFIRMED'}</b> &nbsp;|&nbsp; AUTHORIZED RELEASE SLIP", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#B91C1C"), spaceAfter=15))
    
    data = [
        [Paragraph("<b>Hospital Name:</b>", styles['Normal']), Paragraph(f"{item['hospital_name']}", styles['Normal'])],
        [Paragraph("<b>Hospital License:</b>", styles['Normal']), Paragraph(f"{item['license_number']}", styles['Normal'])],
        [Paragraph("<b>Patient Name:</b>", styles['Normal']), Paragraph(f"{item['patient_name']} (Bed/IPD: {item['patient_ipd_number']})", styles['Normal'])],
        [Paragraph("<b>Blood Group Allocated:</b>", styles['Normal']), Paragraph(f"<b>{item['blood_group']}</b> (Units: {item['units_requested']})", styles['Normal'])],
        [Paragraph("<b>Assigned Batch Code:</b>", styles['Normal']), Paragraph(f"<code>{item['batch_number'] or 'ALLOCATED'}</code>", styles['Normal'])],
        [Paragraph("<b>Attending Doctor:</b>", styles['Normal']), Paragraph(f"{item['doctor_name']} ({item['doctor_mci_id']})", styles['Normal'])],
        [Paragraph("<b>Dispatch Authorized By:</b>", styles['Normal']), Paragraph(f"{item['approved_by'] or 'Central Logistics Desk'}", styles['Normal'])],
        [Paragraph("<b>Issue Timestamp:</b>", styles['Normal']), Paragraph(f"{item['issued_timestamp'] or datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])],
    ]
    t = Table(data, colWidths=[160, 340])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F8FAFC")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 25))
    
    note_style = ParagraphStyle('Note', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=9, textColor=colors.HexColor("#64748B"), alignment=1)
    story.append(Paragraph("This is a digitally verified Cloud Dispatch Token. Cold chain temperature (2°C - 6°C) must be maintained during ambulance transport.", note_style))
    
    doc.build(story)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"GatePass_{item['token_code']}.pdf", mimetype='application/pdf')

@app.route('/download-certificate/<int:cert_id>')
def download_certificate(cert_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Try fetching by certificate_id first, fallback to latest certificate for donor_id
    cursor.execute("""
        SELECT c.*, u.full_name, u.city 
        FROM donor_certificates c
        JOIN donors d ON c.donor_id = d.donor_id
        JOIN users u ON d.user_id = u.user_id 
        WHERE c.certificate_id = ?
    """, (cert_id,))
    cert = cursor.fetchone()
    
    if not cert:
        # Fallback query if cert_id was passed as donor_id
        cursor.execute("""
            SELECT c.*, u.full_name, u.city 
            FROM donor_certificates c
            JOIN donors d ON c.donor_id = d.donor_id
            JOIN users u ON d.user_id = u.user_id 
            WHERE c.donor_id = ?
            ORDER BY c.issue_date DESC, c.certificate_id DESC LIMIT 1
        """, (cert_id,))
        cert = cursor.fetchone()
        
    conn.close()
    
    if not cert:
        flash("Certificate record not found. Donate blood to earn official certificates!", "warning")
        return redirect(url_for('donor_dashboard'))
        
    cert_type = cert['certificate_type'] or 'voluntary'
    is_emergency = (cert_type == 'emergency')
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=45, rightMargin=45, topMargin=45, bottomMargin=45)
    styles = getSampleStyleSheet()
    story = []
    
    # Theme color based on certificate type
    primary_c = colors.HexColor("#B91C1C") if is_emergency else colors.HexColor("#065F46") # Crimson for EMG, Emerald for VOL
    title_text = "CRITICAL EMERGENCY LIFE-SAVER CERTIFICATE" if is_emergency else "VOLUNTARY GOODWILL BLOOD DONATION CERTIFICATE"
    sub_text = "ACUTE TRAUMA RESUSCITATION HONOR & LIFETIME MERIT" if is_emergency else "COMMUNITY HEALTHCARE VOLUNTARY SERVICE AWARD"
    
    cert_title = ParagraphStyle('CertTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22, textColor=primary_c, alignment=1, spaceAfter=6)
    cert_sub = ParagraphStyle('CertSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor("#1E293B"), alignment=1, spaceAfter=18)
    cert_body = ParagraphStyle('CertBody', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=17, textColor=colors.HexColor("#334155"), alignment=1, spaceAfter=16)
    
    story.append(Spacer(1, 30))
    story.append(Paragraph(title_text, cert_title))
    story.append(Paragraph(sub_text, cert_sub))
    story.append(HRFlowable(width="70%", thickness=2, color=primary_c, spaceAfter=25))
    
    story.append(Paragraph("This is to proudly certify that", cert_body))
    story.append(Paragraph(f"<b><font size='18' color='#0F172A'>{cert['full_name']}</font></b>", cert_title))
    story.append(Paragraph(f"Certified Blood Group: <b>{cert['blood_group']}</b> &nbsp;|&nbsp; City: <b>{cert['city']}</b>", cert_body))
    
    if is_emergency:
        desc_text = (
            f"heroically responded to an acute <b>Critical Emergency Blood Requisition</b> at <b>{cert['recipient_hospital']}</b>.<br/>"
            f"Your rapid, life-saving donation directly aided the emergency trauma stabilization of patient <b>{cert['patient_name'] or 'Trauma Patient'}</b>.<br/>"
            "The National Healthcare Council salutes your exemplary bravery and noble commitment to saving lives."
        )
    else:
        desc_text = (
            f"generously completed a selfless <b>Voluntary Blood Donation</b> at <b>{cert['recipient_hospital']}</b>.<br/>"
            "Your noble contribution safeguards essential hospital cold storage reserves and protects future patients in need.<br/>"
            "We deeply honor your ongoing dedication to humanitarian service."
        )
        
    story.append(Paragraph(desc_text, cert_body))
    story.append(Spacer(1, 25))
    
    meta_style = ParagraphStyle('Meta', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, textColor=colors.HexColor("#64748B"), alignment=1)
    story.append(Paragraph(f"Issue Date: <b>{cert['issue_date']}</b> &nbsp;|&nbsp; Official Code: <b>{cert['certificate_code']}</b>", meta_style))
    story.append(Paragraph(f"Authorized by: <b>{cert['recipient_hospital']}</b> & Central Red Cross Logistics Council", meta_style))
    
    doc.build(story)
    buffer.seek(0)
    filename = f"Certificate_{cert['certificate_code']}.pdf"
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

# -----------------------------------------------------------------------------
# APPLICATION ENTRYPOINT
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    print("\n=======================================================")
    print(">>> CLOUD BLOOD BANK WEB APPLICATION RUNNING <<<")
    print(">>> Access URL: http://127.0.0.1:5000 <<<")
    print("=======================================================\n")
    app.run(debug=True, port=5000)
