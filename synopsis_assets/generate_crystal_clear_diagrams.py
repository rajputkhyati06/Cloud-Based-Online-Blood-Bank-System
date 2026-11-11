import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil
import os

os.makedirs('synopsis_assets', exist_ok=True)

if os.path.exists('synopsis_assets/rvit_logo_hd.png'):
    shutil.copy('synopsis_assets/rvit_logo_hd.png', 'synopsis_assets/rvit_logo.png')

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['axes.linewidth'] = 1.2

# =============================================================================
# 1. ARCHITECTURE DIAGRAM (Figure 7.1)
# =============================================================================
def make_architecture():
    fig, ax = plt.subplots(figsize=(8.0, 5.0), dpi=300)
    ax.axis('off')
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, color='#F8FAFC', ec='#94A3B8', lw=1.5))

    # Header Bar
    ax.add_patch(patches.Rectangle((0, 0.90), 1, 0.10, color='#0F172A'))
    ax.text(0.5, 0.95, '3-TIER CLOUD SYSTEM ARCHITECTURE', ha='center', va='center',
            fontsize=13, fontweight='bold', color='white')

    # TIER 1: Presentation Layer
    ax.add_patch(patches.FancyBboxPatch((0.02, 0.63), 0.96, 0.25, boxstyle='round,pad=0.015', ec='#2563EB', fc='#EFF6FF', lw=1.5))
    ax.text(0.04, 0.85, 'TIER 1: PRESENTATION & CLIENT LAYER (Mobile & Web PWA)', fontsize=9.2, fontweight='bold', color='#1E40AF')

    t1_boxes = [
        (0.04, 'HERO DONORS PORTAL', '• Emergency SOS Radar Alerts\n• 1-Click "I Am Coming!" Ping\n• Turn-by-Turn GPS Routes\n• Life-Saver PDF Certificate', '#2563EB'),
        (0.36, 'TRAUMA HOSPITAL DESK', '• Emergency Blood SOS Triage\n• Attending Doctor MCI / NMC\n• Inpatient Bed IPD Binding\n• 2-Way Bedside Verification', '#059669'),
        (0.68, 'LOGISTICS COMMAND', '• 35-Day FIFO Queue Monitor\n• Cold Telemetry (2°C - 6°C)\n• Digital QR Gate-Pass Release\n• Forensic Audit Oversight', '#7C3AED')
    ]
    for x, title, txt, col in t1_boxes:
        ax.add_patch(patches.FancyBboxPatch((x, 0.65), 0.28, 0.175, boxstyle='round,pad=0.01', ec=col, fc='white', lw=1.3))
        ax.add_patch(patches.Rectangle((x, 0.785), 0.28, 0.04, color=col))
        ax.text(x + 0.14, 0.805, title, ha='center', va='center', fontsize=8.0, fontweight='bold', color='white')
        ax.text(x + 0.015, 0.715, txt, ha='left', va='center', fontsize=7.4, color='#0F172A', linespacing=1.25)

    # TIER 2: Logic Layer
    ax.add_patch(patches.FancyBboxPatch((0.02, 0.33), 0.96, 0.27, boxstyle='round,pad=0.015', ec='#DC2626', fc='#FEF2F2', lw=1.5))
    ax.text(0.04, 0.575, 'TIER 2: CLOUD APPLICATION & LOGIC LAYER (Python Flask 3.0 / WSGI)', fontsize=9.2, fontweight='bold', color='#991B1B')

    t2_boxes = [
        (0.04, 'CORE ENGINES', '• Deterministic 35-Day FIFO\n• Haversine Spatial Proximity\n• State-Machine Logic Engine\n• 90-Day Medical Donor Lock', '#DC2626'),
        (0.36, '4-FACTOR SECURITY', '• DGHS State License Check\n• Doctor MCI / NMC Validate\n• Mandatory Rx Slip Archiving\n• PBKDF2 Password Hashing', '#B91C1C'),
        (0.68, 'DOCUMENT & TELEMETRY', '• Dynamic 2D QR Generation\n• Vector PDF Gate-Pass Engine\n• Sub-5ms DB Connection Pool\n• Immutable Microsecond Logs', '#991B1B')
    ]
    for x, title, txt, col in t2_boxes:
        ax.add_patch(patches.FancyBboxPatch((x, 0.35), 0.28, 0.195, boxstyle='round,pad=0.01', ec=col, fc='white', lw=1.3))
        ax.add_patch(patches.Rectangle((x, 0.505), 0.28, 0.04, color=col))
        ax.text(x + 0.14, 0.525, title, ha='center', va='center', fontsize=8.0, fontweight='bold', color='white')
        ax.text(x + 0.015, 0.425, txt, ha='left', va='center', fontsize=7.4, color='#0F172A', linespacing=1.25)

    # TIER 3: Data Layer
    ax.add_patch(patches.FancyBboxPatch((0.02, 0.03), 0.96, 0.27, boxstyle='round,pad=0.015', ec='#059669', fc='#ECFDF5', lw=1.5))
    ax.text(0.04, 0.275, 'TIER 3: DATA PERSISTENCE LAYER (Relational Cloud DBaaS & Secure Storage)', fontsize=9.2, fontweight='bold', color='#065F46')

    t3_boxes = [
        (0.04, 0.44, 'RELATIONAL DATABASE (Cloud DBaaS)',
         '• USERS, HOSPITALS & DONORS Entities (3NF Normalized)\n• BLOOD_INVENTORY (Bags, 8 Phenotypes, 35-Day Expiry)\n• BLOOD_REQUESTS (IPD Bed, Doctor MCI ID, Severity)\n• DISPATCH_PASSES & DONOR_CERTIFICATES (Tokens)', '#059669'),
        (0.52, 0.44, 'ENCRYPTED STORAGE & AUDIT LEDGER',
         '• Encrypted Clinical Prescription Slips & Medical PDF Files\n• Tamper-Proof Audit Trail with Microsecond Timestamps & IP\n• High-Availability Connection Pool with Automatic Snapshots\n• Sub-5ms Low-Latency Query Execution Across Clusters', '#047857')
    ]
    for x, w, title, txt, col in t3_boxes:
        ax.add_patch(patches.FancyBboxPatch((x, 0.05), w, 0.195, boxstyle='round,pad=0.01', ec=col, fc='white', lw=1.3))
        ax.add_patch(patches.Rectangle((x, 0.205), w, 0.04, color=col))
        ax.text(x + w/2, 0.225, title, ha='center', va='center', fontsize=8.0, fontweight='bold', color='white')
        ax.text(x + 0.015, 0.125, txt, ha='left', va='center', fontsize=7.3, color='#0F172A', linespacing=1.25)

    # Connectors
    ax.annotate('', xy=(0.5, 0.60), xytext=(0.5, 0.63), arrowprops=dict(arrowstyle='<->', color='#0F172A', lw=2.2))
    ax.text(0.5, 0.615, 'HTTPS / TLS 1.3 / REST JSON API', ha='center', va='center', fontsize=7.2, fontweight='bold',
            color='#1E293B', bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='#CBD5E1', lw=0.8))

    ax.annotate('', xy=(0.5, 0.30), xytext=(0.5, 0.33), arrowprops=dict(arrowstyle='<->', color='#0F172A', lw=2.2))
    ax.text(0.5, 0.315, 'SQL Connection Pool / ACID Transactions', ha='center', va='center', fontsize=7.2, fontweight='bold',
            color='#1E293B', bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='#CBD5E1', lw=0.8))

    plt.tight_layout()
    plt.savefig('synopsis_assets/architecture_diagram.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Figure 7.1 ready!")

# =============================================================================
# 2. DFD LEVEL 0 (Figure 7.2) - Refined Triangular Flow
# =============================================================================
def make_dfd0():
    fig, ax = plt.subplots(figsize=(8.0, 5.0), dpi=300)
    ax.axis('off')
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, color='#F8FAFC', ec='#94A3B8', lw=1.5))

    # Header Bar
    ax.add_patch(patches.Rectangle((0, 0.90), 1, 0.10, color='#0F172A'))
    ax.text(0.5, 0.95, 'DATA FLOW DIAGRAM (DFD) - LEVEL 0 (CONTEXT LEVEL)', ha='center', va='center',
            fontsize=12.5, fontweight='bold', color='white')

    # Central Bubble
    central = patches.Circle((0.50, 0.45), 0.145, ec='#DC2626', fc='#FEF2F2', lw=2.5)
    ax.add_patch(central)
    ax.text(0.50, 0.505, '0.0', ha='center', va='center', fontsize=13, fontweight='bold', color='#991B1B')
    ax.text(0.50, 0.425, 'Cloud Blood Bank\n& Emergency Triage\nSystem',
            ha='center', va='center', fontsize=8.6, fontweight='bold', color='#0F172A', linespacing=1.2)

    # 1. TOP ENTITY: HOSPITALS
    ax.add_patch(patches.FancyBboxPatch((0.26, 0.70), 0.48, 0.17, boxstyle='round,pad=0.015', ec='#059669', fc='#ECFDF5', lw=1.8))
    ax.add_patch(patches.Rectangle((0.26, 0.82), 0.48, 0.05, color='#059669'))
    ax.text(0.50, 0.845, 'TRAUMA HOSPITALS (Emergency Clinicians)', ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
    ax.text(0.50, 0.76, '• Emergency Blood SOS Triage   • Attending Doctor MCI / NMC ID\n• Mandatory Rx Slip Archival       • Patient Inpatient Bed IPD Binding',
            ha='center', va='center', fontsize=7.4, color='#0F172A', linespacing=1.2)

    # 2. BOTTOM-LEFT ENTITY: DONORS (y=0.04 to 0.23)
    ax.add_patch(patches.FancyBboxPatch((0.03, 0.04), 0.42, 0.19, boxstyle='round,pad=0.015', ec='#2563EB', fc='#EFF6FF', lw=1.8))
    ax.add_patch(patches.Rectangle((0.03, 0.18), 0.42, 0.05, color='#2563EB'))
    ax.text(0.24, 0.205, 'HERO DONORS (Voluntary Registry)', ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
    ax.text(0.05, 0.11, '• Profile & Blood Phenotype (8 Groups)\n• Night & Day Geolocation Availability\n• 1-Click "I Am Coming!" Emergency Response',
            ha='left', va='center', fontsize=7.3, color='#0F172A', linespacing=1.25)

    # 3. BOTTOM-RIGHT ENTITY: CENTRAL ADMIN (y=0.04 to 0.23)
    ax.add_patch(patches.FancyBboxPatch((0.55, 0.04), 0.42, 0.19, boxstyle='round,pad=0.015', ec='#7C3AED', fc='#F5F3FF', lw=1.8))
    ax.add_patch(patches.Rectangle((0.55, 0.18), 0.42, 0.05, color='#7C3AED'))
    ax.text(0.76, 0.205, 'CENTRAL ADMIN (SBTC Command)', ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
    ax.text(0.57, 0.11, '• 35-Day FIFO Expiry Dispatch Policies\n• Real-Time Cold Storage Telemetry (2-6°C)\n• State-Wide Forensic Audit Trail Oversight',
            ha='left', va='center', fontsize=7.3, color='#0F172A', linespacing=1.25)

    # CONNECTORS & BADGES
    # Hospital <-> System (Vertical)
    ax.annotate('', xy=(0.44, 0.60), xytext=(0.44, 0.70), arrowprops=dict(arrowstyle='->', color='#059669', lw=2.0))
    ax.text(0.35, 0.65, 'SOS Requisition + MCI + Rx', ha='center', va='center', fontsize=6.8, fontweight='bold',
            color='#065F46', bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#A7F3D0', lw=0.8))

    ax.annotate('', xy=(0.56, 0.70), xytext=(0.56, 0.60), arrowprops=dict(arrowstyle='->', color='#059669', lw=2.0))
    ax.text(0.65, 0.65, 'FIFO Blood Release & Donor Ping', ha='center', va='center', fontsize=6.8, fontweight='bold',
            color='#065F46', bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#A7F3D0', lw=0.8))

    # Donor <-> System (Diagonal Left)
    ax.annotate('', xy=(0.38, 0.41), xytext=(0.28, 0.26), arrowprops=dict(arrowstyle='->', color='#2563EB', lw=2.0))
    ax.text(0.22, 0.35, 'Donor Availability & SOS Ping', ha='center', va='center', fontsize=6.8, fontweight='bold',
            color='#1E40AF', bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#93C5FD', lw=0.8))

    ax.annotate('', xy=(0.33, 0.25), xytext=(0.43, 0.35), arrowprops=dict(arrowstyle='->', color='#2563EB', lw=2.0))
    ax.text(0.40, 0.28, 'Emergency Alerts & Pass', ha='center', va='center', fontsize=6.8, fontweight='bold',
            color='#1E40AF', bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#93C5FD', lw=0.8))

    # Admin <-> System (Diagonal Right)
    ax.annotate('', xy=(0.62, 0.41), xytext=(0.72, 0.26), arrowprops=dict(arrowstyle='->', color='#7C3AED', lw=2.0))
    ax.text(0.78, 0.35, 'FIFO Policy & Intake Rules', ha='center', va='center', fontsize=6.8, fontweight='bold',
            color='#5B21B6', bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#DDD6FE', lw=0.8))

    ax.annotate('', xy=(0.67, 0.25), xytext=(0.57, 0.35), arrowprops=dict(arrowstyle='->', color='#7C3AED', lw=2.0))
    ax.text(0.60, 0.28, 'Cold Telemetry & Audits', ha='center', va='center', fontsize=6.8, fontweight='bold',
            color='#5B21B6', bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#DDD6FE', lw=0.8))

    plt.tight_layout()
    plt.savefig('synopsis_assets/dfd_level0.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Figure 7.2 ready!")

# =============================================================================
# 3. DFD LEVEL 1 (Figure 7.3) - Refined
# =============================================================================
def make_dfd1():
    fig, ax = plt.subplots(figsize=(8.0, 5.0), dpi=300)
    ax.axis('off')
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, color='#F8FAFC', ec='#94A3B8', lw=1.5))

    # Header Bar
    ax.add_patch(patches.Rectangle((0, 0.90), 1, 0.10, color='#0F172A'))
    ax.text(0.5, 0.95, 'DATA FLOW DIAGRAM (DFD) - LEVEL 1 (SUBSYSTEM PIPELINES)', ha='center', va='center',
            fontsize=12.5, fontweight='bold', color='white')

    # ROW 1 (y=0.74): 1.0 -> 2.0 -> 3.0
    procs_r1 = [
        (0.18, 0.74, '1.0\nRegistration &\nAuthentication', '#2563EB', '#EFF6FF'),
        (0.50, 0.74, '2.0\nEmergency Triage &\nDoctor Verification', '#DC2626', '#FEF2F2'),
        (0.82, 0.74, '3.0\n35-Day FIFO\nCold Dispatch Engine', '#D97706', '#FFFBEB')
    ]
    for x, y, name, ec, fc in procs_r1:
        ax.add_patch(patches.Circle((x, y), 0.10, ec=ec, fc=fc, lw=2.2))
        ax.text(x, y, name, ha='center', va='center', fontsize=7.6, fontweight='bold', color='#0F172A', linespacing=1.2)

    # ROW 2 (y=0.52): Data stores
    stores_r1 = [
        (0.06, 0.50, 0.24, 0.08, 'D1: Users & Hospitals DB'),
        (0.38, 0.50, 0.24, 0.08, 'D2: Requisitions & Slips Store'),
        (0.70, 0.50, 0.24, 0.08, 'D3: Cold Storage Inventory (FIFO)')
    ]
    for x, y, w, h, name in stores_r1:
        ax.add_patch(patches.Rectangle((x, y), w, h, ec='#334155', fc='white', lw=1.4))
        ax.plot([x, x], [y, y + h], color='#0F172A', lw=3.0)
        ax.plot([x + w, x + w], [y, y + h], color='#0F172A', lw=3.0)
        ax.text(x + w/2, y + h/2, name, ha='center', va='center', fontsize=7.4, fontweight='bold', color='#1E293B')

    # ROW 3 (y=0.26): 4.0 and 5.0
    procs_r2 = [
        (0.36, 0.26, '4.0\n2-Way Clinical\nBedside Handshake', '#059669', '#ECFDF5'),
        (0.76, 0.26, '5.0\nForensic Audit &\nSecurity Logging', '#7C3AED', '#F5F3FF')
    ]
    for x, y, name, ec, fc in procs_r2:
        ax.add_patch(patches.Circle((x, y), 0.10, ec=ec, fc=fc, lw=2.2))
        ax.text(x, y, name, ha='center', va='center', fontsize=7.6, fontweight='bold', color='#0F172A', linespacing=1.2)

    # ROW 4 (y=0.06): D4 and D5
    stores_r2 = [
        (0.24, 0.05, 0.24, 0.08, 'D4: Passes & Certificates DB'),
        (0.64, 0.05, 0.24, 0.08, 'D5: Forensic Security Audit Logs')
    ]
    for x, y, w, h, name in stores_r2:
        ax.add_patch(patches.Rectangle((x, y), w, h, ec='#334155', fc='white', lw=1.4))
        ax.plot([x, x], [y, y + h], color='#0F172A', lw=3.0)
        ax.plot([x + w, x + w], [y, y + h], color='#0F172A', lw=3.0)
        ax.text(x + w/2, y + h/2, name, ha='center', va='center', fontsize=7.4, fontweight='bold', color='#1E293B')

    # Connections
    ax.annotate('', xy=(0.40, 0.74), xytext=(0.28, 0.74), arrowprops=dict(arrowstyle='->', color='#2563EB', lw=2.0))
    ax.text(0.34, 0.765, 'Auth Token', fontsize=6.8, fontweight='bold', color='#1E40AF',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#93C5FD', lw=0.8))

    ax.annotate('', xy=(0.72, 0.74), xytext=(0.60, 0.74), arrowprops=dict(arrowstyle='->', color='#DC2626', lw=2.0))
    ax.text(0.66, 0.765, 'Verified SOS', fontsize=6.8, fontweight='bold', color='#991B1B',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#FCA5A5', lw=0.8))

    ax.annotate('', xy=(0.18, 0.58), xytext=(0.18, 0.64), arrowprops=dict(arrowstyle='<->', color='#2563EB', lw=1.8))
    ax.annotate('', xy=(0.50, 0.58), xytext=(0.50, 0.64), arrowprops=dict(arrowstyle='<->', color='#DC2626', lw=1.8))
    ax.annotate('', xy=(0.82, 0.58), xytext=(0.82, 0.64), arrowprops=dict(arrowstyle='<->', color='#D97706', lw=1.8))

    # 3.0 to 4.0
    ax.annotate('', xy=(0.46, 0.30), xytext=(0.75, 0.65), arrowprops=dict(arrowstyle='->', color='#059669', lw=2.0))
    ax.text(0.57, 0.44, 'Dispatch Token / Donor Ping', fontsize=6.8, fontweight='bold', color='#065F46',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#A7F3D0', lw=0.8))

    # 4.0 to D4
    ax.annotate('', xy=(0.36, 0.13), xytext=(0.36, 0.16), arrowprops=dict(arrowstyle='<->', color='#059669', lw=1.8))

    # 4.0 to 5.0
    ax.annotate('', xy=(0.66, 0.26), xytext=(0.46, 0.26), arrowprops=dict(arrowstyle='->', color='#7C3AED', lw=2.0))
    ax.text(0.56, 0.285, 'Audit Event', fontsize=6.8, fontweight='bold', color='#5B21B6',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#DDD6FE', lw=0.8))

    # 5.0 to D5
    ax.annotate('', xy=(0.76, 0.13), xytext=(0.76, 0.16), arrowprops=dict(arrowstyle='->', color='#7C3AED', lw=1.8))

    plt.tight_layout()
    plt.savefig('synopsis_assets/dfd_level1.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Figure 7.3 ready!")

# =============================================================================
# 4. ER DIAGRAM (Figure 7.4) - Perfect Cardinality Badges
# =============================================================================
def make_er():
    fig, ax = plt.subplots(figsize=(8.0, 5.0), dpi=300)
    ax.axis('off')
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, color='#F8FAFC', ec='#94A3B8', lw=1.5))

    # Header Bar
    ax.add_patch(patches.Rectangle((0, 0.90), 1, 0.10, color='#0F172A'))
    ax.text(0.5, 0.95, 'ENTITY-RELATIONSHIP (ER) RELATIONAL CLOUD SCHEMA', ha='center', va='center',
            fontsize=12.5, fontweight='bold', color='white')

    tables = [
        # ROW 1
        (0.04, 0.50, 0.28, 0.37, 'USERS (Authentication & Base)',
         ['[PK] user_id : INT (AUTO)',
          '• full_name : VARCHAR(100)',
          '• email : VARCHAR [UNIQUE]',
          '• password_hash : TEXT (PBKDF2)',
          '• role : ENUM(Donor, Hosp, Admin)',
          '• phone : VARCHAR(15)',
          '• city, state, address : TEXT'], '#1D4ED8'),

        (0.36, 0.50, 0.28, 0.37, 'HOSPITALS (Trauma Centers)',
         ['[PK] hospital_id : INT (AUTO)',
          '[FK] user_id -> USERS',
          '• hospital_name : VARCHAR(150)',
          '• license_no : GOVT DGHS ID',
          '• emergency_contact : VARCHAR',
          '• trust_score : INT (100%)',
          '• verification_status : ENUM'], '#059669'),

        (0.68, 0.50, 0.28, 0.37, 'DONORS (Voluntary Registry)',
         ['[PK] donor_id : INT (AUTO)',
          '[FK] user_id -> USERS',
          '• blood_group : ENUM(8 Types)',
          '• is_available : BOOLEAN',
          '• night_emergency : BOOLEAN',
          '• total_donations : INT',
          '• last_donation_date : DATE'], '#D97706'),

        # ROW 2
        (0.04, 0.05, 0.28, 0.38, 'BLOOD_INVENTORY (FIFO Cold)',
         ['[PK] bag_id : INT (AUTO)',
          '• blood_group : ENUM(8 Types)',
          '• batch_number : VARCHAR(50)',
          '• collection_date : DATE',
          '• expiry_date : +35 Days (FIFO)',
          '• storage_temp : FLOAT (2-6°C)',
          '• status : ENUM(avail, disp, exp)'], '#DC2626'),

        (0.36, 0.05, 0.28, 0.38, 'BLOOD_REQUESTS (SOS Triage)',
         ['[PK] request_id : INT (AUTO)',
          '[FK] hospital_id -> HOSPITALS',
          '• patient_name, bed_ipd : TEXT',
          '• blood_group : ENUM, units : INT',
          '• doctor_name, mci_number : TEXT',
          '• doctor_slip_url : DOC / PDF',
          '• status, donor_status : ENUM'], '#7C3AED'),

        (0.68, 0.05, 0.28, 0.38, 'DISPATCH & CERTIFICATES',
         ['[PK] pass_id : INT (AUTO)',
          '[FK] req_id -> REQUESTS',
          '[FK] donor_id -> DONORS',
          '• token_code : VARCHAR [UNIQUE]',
          '• qr_payload : TEXT (SHA-256)',
          '• issued_time : TIMESTAMP',
          '• cert_code : LIFE-SAVER TOKEN'], '#0891B2')
    ]

    for x, y, w, h, name, fields, color in tables:
        ax.add_patch(patches.Rectangle((x, y), w, h, color='white', ec=color, lw=1.5))
        ax.add_patch(patches.Rectangle((x, y + h - 0.06), w, 0.06, color=color))
        ax.text(x + w/2, y + h - 0.03, name, ha='center', va='center', fontsize=7.8, fontweight='bold', color='white')
        for idx, f in enumerate(fields):
            is_key = f.startswith('[PK]') or f.startswith('[FK]')
            fontweight = 'bold' if is_key else 'normal'
            txt_color = '#991B1B' if f.startswith('[PK]') else ('#1D4ED8' if f.startswith('[FK]') else '#0F172A')
            ax.text(x + 0.012, y + h - 0.095 - idx * 0.042, f, fontsize=7.2, fontweight=fontweight, color=txt_color)

    # Relationships with Clear Badges Floating Cleanly
    # USERS -> HOSPITALS (Horizontal)
    ax.annotate('', xy=(0.36, 0.68), xytext=(0.32, 0.68), arrowprops=dict(arrowstyle='<->', color='#0F172A', lw=1.8))
    ax.text(0.34, 0.71, '1:1', ha='center', va='bottom', fontsize=7.4, fontweight='bold', color='#1E293B')

    # USERS -> DONORS (Horizontal)
    ax.annotate('', xy=(0.68, 0.68), xytext=(0.64, 0.68), arrowprops=dict(arrowstyle='<->', color='#0F172A', lw=1.8))
    ax.text(0.66, 0.71, '1:1', ha='center', va='bottom', fontsize=7.4, fontweight='bold', color='#1E293B')

    # HOSPITALS -> BLOOD_REQUESTS (Vertical)
    ax.annotate('', xy=(0.50, 0.43), xytext=(0.50, 0.50), arrowprops=dict(arrowstyle='<->', color='#0F172A', lw=1.8))
    ax.text(0.525, 0.465, '1:N', ha='left', va='center', fontsize=7.4, fontweight='bold', color='#1E293B')

    # INVENTORY -> REQUESTS (Horizontal FIFO Matching)
    ax.annotate('', xy=(0.36, 0.22), xytext=(0.32, 0.22), arrowprops=dict(arrowstyle='<->', color='#DC2626', lw=1.8))
    ax.text(0.34, 0.25, 'FIFO', ha='center', va='bottom', fontsize=7.2, fontweight='bold', color='#DC2626')

    # REQUESTS -> DISPATCH (Horizontal)
    ax.annotate('', xy=(0.68, 0.22), xytext=(0.64, 0.22), arrowprops=dict(arrowstyle='<->', color='#0F172A', lw=1.8))
    ax.text(0.66, 0.25, '1:1', ha='center', va='bottom', fontsize=7.4, fontweight='bold', color='#1E293B')

    plt.tight_layout()
    plt.savefig('synopsis_assets/er_diagram.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Figure 7.4 ready!")

# =============================================================================
# 5. FIFO FLOWCHART (Figure 7.5) - Pristine Diamond Geometry
# =============================================================================
def make_fifo():
    fig, ax = plt.subplots(figsize=(8.0, 5.0), dpi=300)
    ax.axis('off')
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, color='#F8FAFC', ec='#94A3B8', lw=1.5))

    # Header Bar
    ax.add_patch(patches.Rectangle((0, 0.90), 1, 0.10, color='#0F172A'))
    ax.text(0.5, 0.95, 'ALGORITHM 1: 35-DAY FIFO DISPATCH & TRIAGE FLOWCHART', ha='center', va='center',
            fontsize=12.5, fontweight='bold', color='white')

    # START Pill
    ax.add_patch(patches.FancyBboxPatch((0.26, 0.81), 0.48, 0.065, boxstyle='round,pad=0.01', ec='#059669', fc='#D1FAE5', lw=1.8))
    ax.text(0.5, 0.842, 'START: Emergency Hospital Requisition (Group G, Units U, IPD)',
            ha='center', va='center', fontsize=7.8, fontweight='bold', color='#065F46')

    # 4-Factor Security Check Box
    ax.add_patch(patches.Rectangle((0.24, 0.67), 0.52, 0.09, ec='#2563EB', fc='#EFF6FF', lw=1.5))
    ax.text(0.5, 0.715, '4-Factor Anti-Fraud Verification Protocol:\n• DGHS State License • Attending Doctor MCI / NMC ID\n• Mandatory Rx Slip Archival • Patient Bed IPD Binding',
            ha='center', va='center', fontsize=7.4, fontweight='bold', color='#1E40AF', linespacing=1.2)

    # Decision 1: Clinical Check
    d1_x = [0.5, 0.62, 0.5, 0.38]
    d1_y = [0.63, 0.55, 0.47, 0.55]
    ax.add_patch(patches.Polygon(list(zip(d1_x, d1_y)), ec='#D97706', fc='#FEF3C7', lw=1.8))
    ax.text(0.5, 0.55, 'Valid Clinical\nVerification?', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#92400E')

    # Branch NO: Reject
    ax.add_patch(patches.Rectangle((0.76, 0.51), 0.21, 0.08, ec='#DC2626', fc='#FEE2E2', lw=1.5))
    ax.text(0.865, 0.55, 'REJECT REQUISITION\nFlag Audit Discrepancy\nLock Hospital Trust', ha='center', va='center', fontsize=7.2, fontweight='bold', color='#991B1B')

    # Decision 2: Cold Storage Check
    d2_x = [0.5, 0.62, 0.5, 0.38]
    d2_y = [0.43, 0.34, 0.25, 0.34]
    ax.add_patch(patches.Polygon(list(zip(d2_x, d2_y)), ec='#7C3AED', fc='#EDE9FE', lw=1.8))
    ax.text(0.5, 0.34, 'Units Available\nin Cold Storage?', ha='center', va='center', fontsize=7.6, fontweight='bold', color='#5B21B6')

    # Branch YES: FIFO Dispatch (Left)
    ax.add_patch(patches.Rectangle((0.04, 0.29), 0.27, 0.095, ec='#059669', fc='#D1FAE5', lw=1.5))
    ax.text(0.175, 0.337, 'YES: Execute 35-Day FIFO Query\nSELECT * FROM blood_inventory\nORDER BY expiry_date ASC\n(Dispatches Oldest Safe Unit)',
            ha='center', va='center', fontsize=7.1, fontweight='bold', color='#065F46', linespacing=1.2)

    ax.add_patch(patches.Rectangle((0.04, 0.15), 0.27, 0.09, ec='#059669', fc='#ECFDF5', lw=1.5))
    ax.text(0.175, 0.195, 'Issue Digital QR Gate-Pass\nDynamic QR Code Release Slip\nMark Bag as "dispatched"',
            ha='center', va='center', fontsize=7.1, fontweight='bold', color='#065F46', linespacing=1.2)

    # Branch NO: Emergency SOS (Right)
    ax.add_patch(patches.Rectangle((0.69, 0.29), 0.27, 0.095, ec='#DC2626', fc='#FEE2E2', lw=1.5))
    ax.text(0.825, 0.337, 'NO: Cold Storage Depleted (0)!\nBroadcast Emergency SOS Radar\nto Matched Donors in City Radius\n(Haversine Spatial Proximity)',
            ha='center', va='center', fontsize=7.1, fontweight='bold', color='#991B1B', linespacing=1.2)

    ax.add_patch(patches.Rectangle((0.69, 0.15), 0.27, 0.09, ec='#DC2626', fc='#FEF2F2', lw=1.5))
    ax.text(0.825, 0.195, 'Donor "I Am Coming!" Ping\nDoctor Bedside Verification &\nLife-Saver Cert (90D Cooldown)',
            ha='center', va='center', fontsize=7.1, fontweight='bold', color='#991B1B', linespacing=1.2)

    # END Terminus
    ax.add_patch(patches.FancyBboxPatch((0.28, 0.035), 0.44, 0.065, boxstyle='round,pad=0.01', ec='#334155', fc='#E2E8F0', lw=1.8))
    ax.text(0.5, 0.067, 'END: Patient Life Saved & Audit Hash Sealed', ha='center', va='center', fontsize=8.2, fontweight='bold', color='#0F172A')

    # Connections
    ax.annotate('', xy=(0.5, 0.76), xytext=(0.5, 0.81), arrowprops=dict(arrowstyle='->', lw=1.8, color='#0F172A'))
    ax.annotate('', xy=(0.5, 0.63), xytext=(0.5, 0.67), arrowprops=dict(arrowstyle='->', lw=1.8, color='#0F172A'))

    # NO branch to Reject
    ax.annotate('', xy=(0.76, 0.55), xytext=(0.62, 0.55), arrowprops=dict(arrowstyle='->', color='#DC2626', lw=2.0))
    ax.text(0.69, 0.575, 'NO', fontsize=7.2, fontweight='bold', color='#DC2626',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#FCA5A5', lw=0.8))

    # YES branch to Decision 2
    ax.annotate('', xy=(0.5, 0.43), xytext=(0.5, 0.47), arrowprops=dict(arrowstyle='->', color='#059669', lw=2.0))
    ax.text(0.53, 0.45, 'YES', fontsize=7.2, fontweight='bold', color='#059669',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#A7F3D0', lw=0.8))

    # D2 -> FIFO (Left)
    ax.annotate('', xy=(0.31, 0.34), xytext=(0.38, 0.34), arrowprops=dict(arrowstyle='->', color='#059669', lw=2.0))
    ax.text(0.345, 0.37, 'YES', fontsize=7.2, fontweight='bold', color='#059669',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#A7F3D0', lw=0.8))

    # D2 -> SOS (Right)
    ax.annotate('', xy=(0.69, 0.34), xytext=(0.62, 0.34), arrowprops=dict(arrowstyle='->', color='#DC2626', lw=2.0))
    ax.text(0.655, 0.37, 'NO', fontsize=7.2, fontweight='bold', color='#DC2626',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#FCA5A5', lw=0.8))

    # Vertical flow in branches
    ax.annotate('', xy=(0.175, 0.24), xytext=(0.175, 0.29), arrowprops=dict(arrowstyle='->', lw=1.8, color='#059669'))
    ax.annotate('', xy=(0.825, 0.24), xytext=(0.825, 0.29), arrowprops=dict(arrowstyle='->', lw=1.8, color='#DC2626'))

    # Convergence to END
    ax.annotate('', xy=(0.42, 0.10), xytext=(0.175, 0.15), arrowprops=dict(arrowstyle='->', lw=1.8, color='#059669'))
    ax.annotate('', xy=(0.58, 0.10), xytext=(0.825, 0.15), arrowprops=dict(arrowstyle='->', lw=1.8, color='#DC2626'))

    plt.tight_layout()
    plt.savefig('synopsis_assets/fifo_flowchart.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Figure 7.5 ready!")

if __name__ == '__main__':
    print("Regenerating all 5 diagrams...")
    make_architecture()
    make_dfd0()
    make_dfd1()
    make_er()
    make_fifo()
    print("All 5 diagrams successfully regenerated!")
