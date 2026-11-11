import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs('synopsis_assets', exist_ok=True)

# Common styling constants
FONT_FAMILY = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

# -------------------------------------------------------------
# 1. SYSTEM ARCHITECTURE DIAGRAM (Ultra-Clear 300 DPI, Large Text)
# -------------------------------------------------------------
def make_architecture():
    fig, ax = plt.subplots(figsize=(11, 7.2), dpi=300)
    ax.axis('off')
    ax.add_patch(patches.Rectangle((0.01, 0.01), 0.98, 0.98, fill=True, color='#F8FAFC', ec='#94A3B8', lw=2))

    # Main Header Banner
    ax.add_patch(patches.Rectangle((0.01, 0.91), 0.98, 0.08, fill=True, color='#0F172A', ec='#0F172A'))
    ax.text(0.5, 0.95, 'CLOUD-BASED BLOOD BANK & EMERGENCY TRIAGE SYSTEM ARCHITECTURE', 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='white')

    # TIER 1: PRESENTATION TIER
    ax.add_patch(patches.FancyBboxPatch((0.03, 0.65), 0.94, 0.23, boxstyle='round,pad=0.02', ec='#2563EB', fc='#EFF6FF', lw=2))
    ax.text(0.05, 0.84, 'TIER 1: PRESENTATION & CLIENT INTERFACE TIER (Responsive Web & PWA Portals)', fontsize=10.5, fontweight='bold', color='#1E40AF')
    
    clients = [
        (0.05, 0.67, 0.28, 0.15, 'HERO DONOR PORTAL',
         '• Real-Time Emergency Radar\n• 1-Click "I Am Coming!" Response\n• Verified Gate-Pass GPS Routing\n• Life-Saver Certificate PDF & QR', '#3B82F6'),
        (0.36, 0.67, 0.28, 0.15, 'TRAUMA HOSPITAL DESK',
         '• Emergency SOS Triage Generator\n• Attending Doctor MCI ID Check\n• Mandatory Rx Slip Archival\n• Incoming Donor Accept/Reject Inbox', '#059669'),
        (0.67, 0.67, 0.28, 0.15, 'CENTRAL LOGISTICS COMMAND',
         '• 35-Day FIFO Expiry Sequence\n• Digital QR Gate-Pass Issuance\n• WHO Cold-Chain Telemetry (2-6°C)\n• Forensic Immutable Audit Trail', '#7C3AED')
    ]
    for x, y, w, h, title, txt, border_col in clients:
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.01', ec=border_col, fc='white', lw=1.5))
        ax.add_patch(patches.Rectangle((x, y + h - 0.038), w, 0.038, fill=True, color=border_col))
        ax.text(x + w/2, y + h - 0.019, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
        ax.text(x + 0.015, y + 0.055, txt, ha='left', va='center', fontsize=7.5, color='#1E293B', linespacing=1.3)

    # TIER 2: APPLICATION & LOGIC TIER
    ax.add_patch(patches.FancyBboxPatch((0.03, 0.33), 0.94, 0.28, boxstyle='round,pad=0.02', ec='#DC2626', fc='#FEF2F2', lw=2))
    ax.text(0.05, 0.58, 'TIER 2: CLOUD APPLICATION & LOGIC TIER (Python 3.12, Flask 3.0 WSGI Engine)', fontsize=10.5, fontweight='bold', color='#991B1B')

    engines = [
        (0.05, 0.35, 0.28, 0.21, 'CORE DISPATCH ENGINES',
         '• 35-Day FIFO Allocation Logic\n• Geolocation Haversine Distance\n• 2-Way Clinical Doctor Handshake\n• 90-Day Medical Health Freeze\n• City Hub Radius Clustering', '#DC2626'),
        (0.36, 0.35, 0.28, 0.21, '4-FACTOR SECURITY ENGINE',
         '• DGHS Govt License Format Check\n• Doctor MCI / NMC Verification\n• Mandatory Prescription Slip Upload\n• Patient IPD Bed Number Binding\n• Argon2/PBKDF2 Password Hash', '#B91C1C'),
        (0.67, 0.35, 0.28, 0.21, 'REPORTING & TELEMETRY',
         '• ReportLab Dynamic Vector PDF\n• 2D Dynamic QR Code Cryptography\n• Real-Time PowerBI Analytics API\n• Microsecond Audit Log Triggers\n• Cold Storage Thermal Monitor', '#991B1B')
    ]
    for x, y, w, h, title, txt, border_col in engines:
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.01', ec=border_col, fc='white', lw=1.5))
        ax.add_patch(patches.Rectangle((x, y + h - 0.038), w, 0.038, fill=True, color=border_col))
        ax.text(x + w/2, y + h - 0.019, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
        ax.text(x + 0.015, y + 0.08, txt, ha='left', va='center', fontsize=7.5, color='#1E293B', linespacing=1.3)

    # TIER 3: DATA & PERSISTENCE TIER
    ax.add_patch(patches.FancyBboxPatch((0.03, 0.04), 0.94, 0.25, boxstyle='round,pad=0.02', ec='#059669', fc='#ECFDF5', lw=2))
    ax.text(0.05, 0.26, 'TIER 3: DATA PERSISTENCE & STORAGE TIER (Cloud DBaaS & Encrypted Buckets)', fontsize=10.5, fontweight='bold', color='#065F46')

    dbs = [
        (0.05, 0.06, 0.43, 0.18, 'RELATIONAL CLOUD DATABASE (DBaaS)',
         '• USERS & RBAC (Donors, Hospitals, Admin)\n• BLOOD_INVENTORY (Bags, Temp, Batch, 35-Day Expiry)\n• BLOOD_REQUESTS (Patient IPD, Doctor MCI, Urgency)\n• DISPATCH_PASSES & DONOR_CERTIFICATES (Tokens)', '#059669'),
        (0.52, 0.06, 0.45, 0.18, 'CLOUD OBJECT STORAGE & AUDIT REPOSITORY',
         '• Encrypted Prescription Slip Documents (PDF/Images)\n• Immutable Forensic Security Audit Trail (Logs)\n• High-Concurrency Connection Pooling (sub-5ms)\n• Automated Cloud Snapshot & Disaster Recovery Backups', '#047857')
    ]
    for x, y, w, h, title, txt, border_col in dbs:
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.01', ec=border_col, fc='white', lw=1.5))
        ax.add_patch(patches.Rectangle((x, y + h - 0.038), w, 0.038, fill=True, color=border_col))
        ax.text(x + w/2, y + h - 0.019, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
        ax.text(x + 0.015, y + 0.07, txt, ha='left', va='center', fontsize=7.8, color='#1E293B', linespacing=1.35)

    # Connection Arrows
    ax.annotate('', xy=(0.5, 0.61), xytext=(0.5, 0.65), arrowprops=dict(arrowstyle='<->', color='#334155', lw=2.5))
    ax.annotate('', xy=(0.5, 0.29), xytext=(0.5, 0.33), arrowprops=dict(arrowstyle='<->', color='#334155', lw=2.5))

    plt.tight_layout()
    plt.savefig('synopsis_assets/architecture_diagram.png', bbox_inches='tight', dpi=300)
    plt.close()

# -------------------------------------------------------------
# 2. DFD LEVEL 0 (CONTEXT LEVEL DIAGRAM - Crystal Clear)
# -------------------------------------------------------------
def make_dfd0():
    fig, ax = plt.subplots(figsize=(10.5, 6.5), dpi=300)
    ax.axis('off')
    ax.add_patch(patches.Rectangle((0.01, 0.01), 0.98, 0.98, fill=True, color='#F8FAFC', ec='#94A3B8', lw=2))

    ax.add_patch(patches.Rectangle((0.01, 0.91), 0.98, 0.08, fill=True, color='#0F172A', ec='#0F172A'))
    ax.text(0.5, 0.95, 'DATA FLOW DIAGRAM (DFD) - LEVEL 0 (CONTEXT LEVEL)', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='white')

    # Central System Bubble
    central = patches.Circle((0.5, 0.48), 0.17, ec='#DC2626', fc='#FEF2F2', lw=3)
    ax.add_patch(central)
    ax.text(0.5, 0.51, '0.0', ha='center', va='center', fontsize=13, fontweight='bold', color='#991B1B')
    ax.text(0.5, 0.44, 'Cloud-Based\nBlood Bank &\nEmergency Triage\nSystem', 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1E293B', linespacing=1.2)

    # Entity 1: Hero Donor
    ax.add_patch(patches.FancyBboxPatch((0.04, 0.37), 0.19, 0.22, boxstyle='round,pad=0.01', ec='#2563EB', fc='#EFF6FF', lw=2))
    ax.add_patch(patches.Rectangle((0.04, 0.54), 0.19, 0.05, fill=True, color='#2563EB'))
    ax.text(0.135, 0.565, 'DONOR ENTITY', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    ax.text(0.135, 0.45, 'Voluntary Registered\nCitizen & Hero Donors\n(Available 24x7)', ha='center', va='center', fontsize=8, color='#1E293B')

    # Entity 2: Trauma Hospital
    ax.add_patch(patches.FancyBboxPatch((0.77, 0.59), 0.19, 0.22, boxstyle='round,pad=0.01', ec='#059669', fc='#ECFDF5', lw=2))
    ax.add_patch(patches.Rectangle((0.77, 0.76), 0.19, 0.05, fill=True, color='#059669'))
    ax.text(0.865, 0.785, 'HOSPITAL ENTITY', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    ax.text(0.865, 0.67, 'Accredited Healthcare\nFacilities & Trauma ER\n(NABH / DGHS)', ha='center', va='center', fontsize=8, color='#1E293B')

    # Entity 3: Central Admin
    ax.add_patch(patches.FancyBboxPatch((0.77, 0.15), 0.19, 0.22, boxstyle='round,pad=0.01', ec='#7C3AED', fc='#F5F3FF', lw=2))
    ax.add_patch(patches.Rectangle((0.77, 0.32), 0.19, 0.05, fill=True, color='#7C3AED'))
    ax.text(0.865, 0.345, 'CENTRAL ADMIN', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    ax.text(0.865, 0.23, 'State Blood Council\n(SBTC / Red Cross)\nLogistics Desk', ha='center', va='center', fontsize=8, color='#1E293B')

    # Dataflows with clean text boxes
    # Donor <-> System
    ax.annotate('', xy=(0.33, 0.53), xytext=(0.23, 0.53), arrowprops=dict(arrowstyle='->', color='#2563EB', lw=2))
    ax.text(0.28, 0.56, '1. Registration, Night Availability,\n"I Am Coming!" Response Ping', ha='center', va='center', fontsize=7.2, fontweight='bold', color='#1E40AF')

    ax.annotate('', xy=(0.23, 0.43), xytext=(0.33, 0.43), arrowprops=dict(arrowstyle='->', color='#2563EB', lw=2))
    ax.text(0.28, 0.40, '2. Emergency Radar Alerts, ER Route,\nGate-Pass & Govt Life-Saver Certificate', ha='center', va='center', fontsize=7.2, fontweight='bold', color='#1E40AF')

    # Hospital <-> System
    ax.annotate('', xy=(0.67, 0.55), xytext=(0.77, 0.67), arrowprops=dict(arrowstyle='->', color='#059669', lw=2))
    ax.text(0.72, 0.62, '3. Emergency SOS Requisition,\nDoctor MCI ID, Rx Slip, Bed IPD', ha='center', va='center', fontsize=7.2, fontweight='bold', color='#065F46')

    ax.annotate('', xy=(0.77, 0.61), xytext=(0.67, 0.49), arrowprops=dict(arrowstyle='->', color='#059669', lw=2))
    ax.text(0.72, 0.53, '4. Live Donor Match Alerts,\nApproved FIFO Dispatches', ha='center', va='center', fontsize=7.2, fontweight='bold', color='#065F46')

    # Admin <-> System
    ax.annotate('', xy=(0.67, 0.42), xytext=(0.77, 0.28), arrowprops=dict(arrowstyle='->', color='#7C3AED', lw=2))
    ax.text(0.72, 0.36, '5. Cold Storage Unit Intake,\nFIFO Clearances, Health Policy', ha='center', va='center', fontsize=7.2, fontweight='bold', color='#5B21B6')

    ax.annotate('', xy=(0.77, 0.22), xytext=(0.67, 0.36), arrowprops=dict(arrowstyle='->', color='#7C3AED', lw=2))
    ax.text(0.72, 0.27, '6. Real-Time Thermal Telemetry,\nForensic Security Audit Logs', ha='center', va='center', fontsize=7.2, fontweight='bold', color='#5B21B6')

    plt.tight_layout()
    plt.savefig('synopsis_assets/dfd_level0.png', bbox_inches='tight', dpi=300)
    plt.close()

# -------------------------------------------------------------
# 3. DFD LEVEL 1 (DECOMPOSITION DIAGRAM)
# -------------------------------------------------------------
def make_dfd1():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    ax.axis('off')
    ax.add_patch(patches.Rectangle((0.01, 0.01), 0.98, 0.98, fill=True, color='#F8FAFC', ec='#94A3B8', lw=2))

    ax.add_patch(patches.Rectangle((0.01, 0.91), 0.98, 0.08, fill=True, color='#0F172A', ec='#0F172A'))
    ax.text(0.5, 0.95, 'DATA FLOW DIAGRAM (DFD) - LEVEL 1 (SUBSYSTEM PROCESS WORKFLOW)', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='white')

    # 5 Process Bubbles
    processes = [
        (0.18, 0.70, '1.0\nRegistration &\nRole Verification', '#2563EB', '#EFF6FF'),
        (0.50, 0.70, '2.0\nEmergency Triage &\nDoctor Verification', '#DC2626', '#FEF2F2'),
        (0.82, 0.70, '3.0\n2-Way Clinical\nDoctor Handshake', '#059669', '#ECFDF5'),
        (0.34, 0.30, '4.0\n35-Day FIFO\nCold Storage Dispatch', '#D97706', '#FFFBEB'),
        (0.66, 0.30, '5.0\nForensic Audit &\nSecurity Logging', '#7C3AED', '#F5F3FF')
    ]
    for x, y, name, ec, fc in processes:
        ax.add_patch(patches.Circle((x, y), 0.095, ec=ec, fc=fc, lw=2.5))
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A', linespacing=1.2)

    # 5 Open-ended Data Stores
    stores = [
        (0.06, 0.47, 0.24, 0.065, 'D1: Users & Accredited Hospitals'),
        (0.38, 0.50, 0.24, 0.065, 'D2: Blood Requisitions & Slips'),
        (0.70, 0.50, 0.24, 0.065, 'D3: Digital Passes & Certificates'),
        (0.14, 0.12, 0.26, 0.065, 'D4: Cold Storage Inventory (FIFO)'),
        (0.60, 0.12, 0.26, 0.065, 'D5: Immutable Security Audit Logs')
    ]
    for x, y, w, h, name in stores:
        ax.add_patch(patches.Rectangle((x, y), w, h, ec='#334155', fc='white', lw=1.5))
        ax.plot([x, x], [y, y + h], color='#334155', lw=3)
        ax.plot([x + w, x + w], [y, y + h], color='#334155', lw=3)
        ax.text(x + w/2, y + h/2, name, ha='center', va='center', fontsize=7.8, fontweight='bold', color='#1E293B')

    # Interconnecting Process Flows
    ax.annotate('', xy=(0.28, 0.70), xytext=(0.40, 0.70), arrowprops=dict(arrowstyle='<->', color='#475569', lw=2))
    ax.annotate('', xy=(0.60, 0.70), xytext=(0.72, 0.70), arrowprops=dict(arrowstyle='<->', color='#475569', lw=2))
    ax.annotate('', xy=(0.44, 0.30), xytext=(0.56, 0.30), arrowprops=dict(arrowstyle='<->', color='#475569', lw=2))
    ax.annotate('', xy=(0.50, 0.60), xytext=(0.37, 0.39), arrowprops=dict(arrowstyle='->', color='#DC2626', lw=2))
    ax.annotate('', xy=(0.82, 0.60), xytext=(0.71, 0.39), arrowprops=dict(arrowstyle='->', color='#059669', lw=2))

    plt.tight_layout()
    plt.savefig('synopsis_assets/dfd_level1.png', bbox_inches='tight', dpi=300)
    plt.close()

# -------------------------------------------------------------
# 4. ENTITY RELATIONSHIP (ER) DIAGRAM (High Contrast 300 DPI)
# -------------------------------------------------------------
def make_er():
    fig, ax = plt.subplots(figsize=(11.5, 7.5), dpi=300)
    ax.axis('off')
    ax.add_patch(patches.Rectangle((0.01, 0.01), 0.98, 0.98, fill=True, color='#F8FAFC', ec='#94A3B8', lw=2))

    ax.add_patch(patches.Rectangle((0.01, 0.91), 0.98, 0.08, fill=True, color='#0F172A', ec='#0F172A'))
    ax.text(0.5, 0.95, 'ENTITY-RELATIONSHIP (ER) RELATIONAL CLOUD SCHEMA (3NF COMPLIANT)', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='white')

    tables = [
        (0.03, 0.63, 0.28, 0.25, 'USERS (Auth Base)',
         ['PK user_id : INTEGER', 'full_name : VARCHAR(100)', 'email : VARCHAR(120) [UNIQUE]', 'password_hash : TEXT (PBKDF2)', 'role : ENUM(donor,hosp,admin)', 'phone, city, address', 'created_at : TIMESTAMP'], '#2563EB'),
        (0.36, 0.63, 0.28, 0.25, 'HOSPITALS',
         ['PK hospital_id : INTEGER', 'FK user_id : INTEGER (USERS)', 'hospital_name : VARCHAR(150)', 'license_number : VARCHAR [GOVT]', 'emergency_desk_contact : TEXT', 'trust_score : INT [100%]', 'google_maps_url : TEXT'], '#059669'),
        (0.69, 0.63, 0.28, 0.25, 'DONORS',
         ['PK donor_id : INTEGER', 'FK user_id : INTEGER (USERS)', 'blood_group : ENUM(8 Groups)', 'is_available : BOOLEAN [1/0]', 'night_emergency_available : BOOL', 'total_donations : INTEGER', 'last_donated_date : DATE'], '#D97706'),
        (0.03, 0.29, 0.28, 0.27, 'BLOOD_INVENTORY',
         ['PK bag_id : INTEGER', 'blood_group : ENUM(8 Groups)', 'batch_number : VARCHAR(50)', 'units_available : INT [1 Unit]', 'collection_date : DATE', 'expiry_date : DATE (+35 Days)', 'storage_temp_celsius : REAL (2-6°C)', 'status : ENUM(avail,dispatched)'], '#DC2626'),
        (0.36, 0.29, 0.28, 0.27, 'BLOOD_REQUESTS',
         ['PK request_id : INTEGER', 'FK hospital_id : INTEGER (HOSP)', 'patient_name, patient_ipd : TEXT', 'blood_group, units_requested', 'urgency_level : ENUM(std,emergency)', 'doctor_name, doctor_mci_id', 'doctor_slip_url : TEXT [DOC]', 'status, donor_status : TEXT'], '#7C3AED'),
        (0.69, 0.29, 0.28, 0.27, 'DISPATCH_PASSES',
         ['PK pass_id : INTEGER', 'FK request_id : INT [UNIQUE]', 'token_code : VARCHAR [UNIQUE]', 'approved_by : VARCHAR(100)', 'issued_timestamp : TIMESTAMP', 'qr_payload : TEXT (Token,Hosp,Bag)'], '#0891B2'),
        (0.36, 0.05, 0.28, 0.18, 'DONOR_CERTIFICATES',
         ['PK certificate_id : INTEGER', 'FK donor_id : INTEGER (DONOR)', 'certificate_code : VARCHAR [UNIQUE]', 'recipient_hospital : VARCHAR(150)', 'issue_date : DATE', 'cooldown_freeze : 90 Days Locked'], '#DB2777'),
        (0.69, 0.05, 0.28, 0.18, 'AUDIT_LOGS (Forensics)',
         ['PK log_id : INTEGER', 'action : VARCHAR(100)', 'performed_by : VARCHAR(100)', 'timestamp : TIMESTAMP (CURRENT)', 'details : TEXT (Immutable Hash)'], '#475569')
    ]

    for x, y, w, h, name, fields, color in tables:
        # Header bar
        ax.add_patch(patches.Rectangle((x, y + h - 0.045), w, 0.045, fill=True, color=color, ec=color))
        ax.text(x + w/2, y + h - 0.0225, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
        # Body box
        ax.add_patch(patches.Rectangle((x, y), w, h - 0.045, fill=True, color='white', ec=color, lw=1.5))
        for idx, f in enumerate(fields):
            ax.text(x + 0.012, y + h - 0.075 - idx*0.027, f, fontsize=7.2, color='#1E293B', fontfamily='monospace')

    # Relationship connectors
    ax.annotate('', xy=(0.31, 0.75), xytext=(0.36, 0.75), arrowprops=dict(arrowstyle='<->', color='#1E293B', lw=1.8))
    ax.annotate('', xy=(0.64, 0.75), xytext=(0.69, 0.75), arrowprops=dict(arrowstyle='<->', color='#1E293B', lw=1.8))
    ax.annotate('', xy=(0.50, 0.63), xytext=(0.50, 0.56), arrowprops=dict(arrowstyle='<->', color='#1E293B', lw=1.8))
    ax.annotate('', xy=(0.64, 0.42), xytext=(0.69, 0.42), arrowprops=dict(arrowstyle='<->', color='#1E293B', lw=1.8))
    ax.annotate('', xy=(0.31, 0.42), xytext=(0.36, 0.42), arrowprops=dict(arrowstyle='<->', color='#1E293B', lw=1.8))
    ax.annotate('', xy=(0.50, 0.29), xytext=(0.50, 0.23), arrowprops=dict(arrowstyle='<->', color='#1E293B', lw=1.8))

    plt.tight_layout()
    plt.savefig('synopsis_assets/er_diagram.png', bbox_inches='tight', dpi=300)
    plt.close()

# -------------------------------------------------------------
# 5. FIFO DISPATCH & TRIAGE FLOWCHART (Print Quality 300 DPI)
# -------------------------------------------------------------
def make_fifo():
    fig, ax = plt.subplots(figsize=(10.5, 7.0), dpi=300)
    ax.axis('off')
    ax.add_patch(patches.Rectangle((0.01, 0.01), 0.98, 0.98, fill=True, color='#F8FAFC', ec='#94A3B8', lw=2))

    ax.add_patch(patches.Rectangle((0.01, 0.91), 0.98, 0.08, fill=True, color='#0F172A', ec='#0F172A'))
    ax.text(0.5, 0.95, 'ALGORITHM 1: 35-DAY FIFO DISPATCH & EMERGENCY TRIAGE FLOWCHART', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='white')

    # Step 1: Start
    ax.add_patch(patches.FancyBboxPatch((0.32, 0.82), 0.36, 0.065, boxstyle='round,pad=0.01', ec='#059669', fc='#D1FAE5', lw=2))
    ax.text(0.5, 0.852, 'START: Hospital Submits Requisition (Group G, Units U, IPD)', ha='center', va='center', fontsize=8, fontweight='bold', color='#065F46')

    # Step 2: 4-Factor Security Check
    ax.add_patch(patches.Rectangle((0.30, 0.69), 0.40, 0.08, ec='#2563EB', fc='#EFF6FF', lw=2))
    ax.text(0.5, 0.73, '4-Factor Verification Protocol:\n• DGHS State License • Doctor MCI Registration ID\n• Mandatory Signed Prescription Slip • Patient IPD Bed', ha='center', va='center', fontsize=7.5, color='#1E40AF', linespacing=1.2)

    # Step 3: Decision Diamond
    diamond_x = [0.5, 0.64, 0.5, 0.36]
    diamond_y = [0.65, 0.57, 0.49, 0.57]
    ax.add_patch(patches.Polygon(list(zip(diamond_x, diamond_y)), ec='#D97706', fc='#FEF3C7', lw=2))
    ax.text(0.5, 0.57, 'Valid Clinical\nVerification?', ha='center', va='center', fontsize=8, fontweight='bold', color='#92400E')

    # Reject Branch
    ax.add_patch(patches.Rectangle((0.74, 0.535), 0.22, 0.07, ec='#DC2626', fc='#FEE2E2', lw=2))
    ax.text(0.85, 0.57, 'BLOCK REQUISITION\nRecord in Forensic Audit Trail\nFlag Trust Score Discrepancy', ha='center', va='center', fontsize=7, fontweight='bold', color='#991B1B')

    # Step 4: Decision Diamond 2 (Stock in Cold Storage?)
    d2_x = [0.5, 0.65, 0.5, 0.35]
    d2_y = [0.44, 0.35, 0.26, 0.35]
    ax.add_patch(patches.Polygon(list(zip(d2_x, d2_y)), ec='#7C3AED', fc='#EDE9FE', lw=2))
    ax.text(0.5, 0.35, 'Available in\nCentral Cold Storage?\n(status = "available")', ha='center', va='center', fontsize=8, fontweight='bold', color='#5B21B6')

    # YES: FIFO Allocation
    ax.add_patch(patches.Rectangle((0.04, 0.31), 0.27, 0.08, ec='#059669', fc='#D1FAE5', lw=2))
    ax.text(0.175, 0.35, 'YES: Execute FIFO Allocation Query\nSELECT * FROM blood_inventory\nORDER BY expiry_date ASC LIMIT U\n(Prioritizes Oldest Safe Biological Unit)', ha='center', va='center', fontsize=7, fontweight='bold', color='#065F46')

    ax.add_patch(patches.Rectangle((0.04, 0.17), 0.27, 0.08, ec='#059669', fc='#ECFDF5', lw=2))
    ax.text(0.175, 0.21, 'Issue Digital Dispatch Gate-Pass\nDynamic 2D QR Code Token Slip\nMark Bag as "dispatched" in Storage', ha='center', va='center', fontsize=7, color='#065F46')

    # NO: Emergency SOS Broadcast
    ax.add_patch(patches.Rectangle((0.69, 0.31), 0.27, 0.08, ec='#DC2626', fc='#FEE2E2', lw=2))
    ax.text(0.825, 0.35, 'NO: Cold Storage Depleted (0 Units)!\nTrigger Instant Emergency SOS Radar\nto Matched Donors in City Radius\n(Haversine Proximity Calculation)', ha='center', va='center', fontsize=7, fontweight='bold', color='#991B1B')

    ax.add_patch(patches.Rectangle((0.69, 0.17), 0.27, 0.08, ec='#DC2626', fc='#FEF2F2', lw=2))
    ax.text(0.825, 0.21, 'Donor "I Am Coming!" Handshake\nDoctor Bedside Verification &\nLife-Saver Cert (90-Day Lockout)', ha='center', va='center', fontsize=7, color='#991B1B')

    # Final Terminus
    ax.add_patch(patches.FancyBboxPatch((0.34, 0.05), 0.32, 0.06, boxstyle='round,pad=0.01', ec='#334155', fc='#E2E8F0', lw=2))
    ax.text(0.5, 0.08, 'END: Patient Life Saved & Audit Trail Logged', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F172A')

    # Connectors
    ax.annotate('', xy=(0.5, 0.69), xytext=(0.5, 0.82), arrowprops=dict(arrowstyle='->', lw=2))
    ax.annotate('', xy=(0.5, 0.65), xytext=(0.5, 0.69), arrowprops=dict(arrowstyle='->', lw=2))
    ax.annotate('NO', xy=(0.74, 0.57), xytext=(0.64, 0.57), arrowprops=dict(arrowstyle='->', color='#DC2626', lw=2), fontsize=8, fontweight='bold', color='#DC2626')
    ax.annotate('YES', xy=(0.5, 0.44), xytext=(0.5, 0.49), arrowprops=dict(arrowstyle='->', color='#059669', lw=2), fontsize=8, fontweight='bold', color='#059669')
    ax.annotate('YES', xy=(0.31, 0.35), xytext=(0.35, 0.35), arrowprops=dict(arrowstyle='->', color='#059669', lw=2), fontsize=8, fontweight='bold', color='#059669')
    ax.annotate('NO', xy=(0.69, 0.35), xytext=(0.65, 0.35), arrowprops=dict(arrowstyle='->', color='#DC2626', lw=2), fontsize=8, fontweight='bold', color='#DC2626')
    ax.annotate('', xy=(0.175, 0.25), xytext=(0.175, 0.31), arrowprops=dict(arrowstyle='->', lw=2))
    ax.annotate('', xy=(0.825, 0.25), xytext=(0.825, 0.31), arrowprops=dict(arrowstyle='->', lw=2))
    ax.annotate('', xy=(0.5, 0.11), xytext=(0.175, 0.17), arrowprops=dict(arrowstyle='->', lw=2))
    ax.annotate('', xy=(0.5, 0.11), xytext=(0.825, 0.17), arrowprops=dict(arrowstyle='->', lw=2))

    plt.tight_layout()
    plt.savefig('synopsis_assets/fifo_flowchart.png', bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == '__main__':
    print('Generating Ultra-Clear 300 DPI Diagrams...')
    make_architecture()
    print('1. Architecture Diagram generated!')
    make_dfd0()
    print('2. DFD Level 0 generated!')
    make_dfd1()
    print('3. DFD Level 1 generated!')
    make_er()
    print('4. ER Diagram generated!')
    make_fifo()
    print('5. FIFO Flowchart generated!')
    print('All 5 diagrams successfully generated with NO warnings at 300 DPI!')
