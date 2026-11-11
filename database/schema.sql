-- ======================================================================
-- CLOUD-BASED ONLINE BLOOD BANK & EMERGENCY TRIAGE SYSTEM
-- Relational Database Schema (Cloud DBaaS Compatible)
-- ======================================================================

-- 1. USERS TABLE (Base authentication table for all 3 roles)
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('donor', 'hospital', 'admin')) NOT NULL,
    phone TEXT NOT NULL,
    city TEXT NOT NULL,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. DONORS PROFILE TABLE (Details specific to donors)
CREATE TABLE IF NOT EXISTS donors (
    donor_id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    blood_group TEXT CHECK(blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')) NOT NULL,
    is_available BOOLEAN DEFAULT 1,                -- 1 = Available, 0 = Unavailable
    night_emergency_available BOOLEAN DEFAULT 1,  -- Willing to donate at night (1 AM - 5 AM)
    fitness_certificate_url TEXT,                 -- Cloud Object Storage URL for Medical Certificate
    total_donations INTEGER DEFAULT 0,
    last_donated_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 3. HOSPITALS PROFILE TABLE (Details specific to registered hospitals)
CREATE TABLE IF NOT EXISTS hospitals (
    hospital_id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    hospital_name TEXT NOT NULL,
    license_number TEXT NOT NULL,                  -- Medical Council / Govt Registration License
    emergency_desk_contact TEXT NOT NULL,
    emergency_desk_person TEXT NOT NULL,
    google_maps_url TEXT,
    trust_score INTEGER DEFAULT 100,               -- Decreased if hospital raises false emergency
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 4. BLOOD INVENTORY TABLE (Real-Time Cold Storage Stock with 35-Day Expiry Tracking)
CREATE TABLE IF NOT EXISTS blood_inventory (
    bag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    blood_bank_name TEXT NOT NULL,
    city TEXT NOT NULL DEFAULT 'Delhi',            -- Regional Hub (Delhi, Noida, Lucknow, etc.)
    blood_group TEXT CHECK(blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')) NOT NULL,
    units_available INTEGER DEFAULT 1,             -- Typically 1 bag = 1 unit (approx 350-450 ml)
    collection_date DATE NOT NULL,
    expiry_date DATE NOT NULL,                     -- 35-day shelf-life date (FIFO Algorithm sorting key)
    batch_number TEXT NOT NULL,
    storage_temp_celsius REAL DEFAULT 4.0,         -- Ideal cold storage temperature (2°C - 6°C)
    status TEXT CHECK(status IN ('available', 'reserved', 'dispatched', 'expired')) DEFAULT 'available'
);

-- 5. BLOOD REQUESTS & EMERGENCY TRIAGE TABLE (Hospital requisitions)
CREATE TABLE IF NOT EXISTS blood_requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_id INTEGER NOT NULL,
    patient_name TEXT NOT NULL,
    patient_ipd_number TEXT NOT NULL,              -- In-Patient Department / Bed Number
    blood_group TEXT NOT NULL,
    units_requested INTEGER NOT NULL,
    urgency_level TEXT CHECK(urgency_level IN ('standard', 'emergency')) NOT NULL,
    doctor_name TEXT NOT NULL,
    doctor_mci_id TEXT NOT NULL,                   -- Doctor Medical Council Registration ID
    doctor_slip_url TEXT,                          -- Cloud Storage URL of signed emergency slip
    status TEXT CHECK(status IN ('pending', 'approved', 'rejected', 'dispatched')) DEFAULT 'pending',
    dispatch_bag_id INTEGER,                       -- Linked bag assigned via FIFO
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
);

-- 6. DIGITAL DISPATCH GATE-PASS TABLE (Official token for hospital pickup)
CREATE TABLE IF NOT EXISTS dispatch_passes (
    pass_id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER UNIQUE NOT NULL,
    token_code TEXT UNIQUE NOT NULL,               -- e.g., 'PASS-DELHI-9082'
    approved_by TEXT NOT NULL,
    issued_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    qr_payload TEXT NOT NULL,
    FOREIGN KEY (request_id) REFERENCES blood_requests(request_id)
);

-- 7. DONOR LIFE-SAVER CERTIFICATES TABLE (Automated appreciation certificate)
CREATE TABLE IF NOT EXISTS donor_certificates (
    certificate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_id INTEGER NOT NULL,
    blood_group TEXT NOT NULL,
    recipient_hospital TEXT NOT NULL,
    issue_date DATE DEFAULT (DATE('now')),
    certificate_code TEXT UNIQUE NOT NULL,         -- e.g., 'CERT-HERO-2026-441'
    certificate_pdf_url TEXT,
    FOREIGN KEY (donor_id) REFERENCES donors(donor_id)
);

-- 8. CLOUD AUDIT TRAIL LOGS (Security & Compliance)
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    performed_by TEXT NOT NULL,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
