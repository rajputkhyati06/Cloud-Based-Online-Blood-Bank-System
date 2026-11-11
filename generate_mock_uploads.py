import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

styles = getSampleStyleSheet()

# 1. Sample Doctor Prescription Slip
slip_path = os.path.join(UPLOAD_DIR, "slip_emg_402.pdf")
doc1 = SimpleDocTemplate(slip_path, pagesize=letter)
story1 = [
    Paragraph("<b>INDRAPRASTHA APOLLO HOSPITAL - EMERGENCY TRAUMA REQUISITION</b>", styles['Heading2']),
    Spacer(1, 15),
    Paragraph("<b>Patient Name:</b> Aniket Choudhary | <b>Age:</b> 28 | <b>Gender:</b> Male", styles['Normal']),
    Paragraph("<b>IPD / Bed Number:</b> IPD-TRAUMA-402 | <b>Ward:</b> Acute Trauma ICU", styles['Normal']),
    Paragraph("<b>Clinical Diagnosis:</b> Severe Hemorrhagic Shock post-RTA (Road Traffic Accident)", styles['Normal']),
    Spacer(1, 10),
    Paragraph("<b>Blood Requisition:</b> 2 Units of Packed Red Blood Cells (PRBC) - <b>O-NEGATIVE (O-)</b>", styles['Heading3']),
    Paragraph("<b>Urgency:</b> STAT / Critical Immediate Resuscitation", styles['Normal']),
    Spacer(1, 20),
    Paragraph("<b>Attending Surgeon:</b> Dr. V. K. Sharma, MS (Ortho), MCh (Trauma)", styles['Normal']),
    Paragraph("<b>Medical Council Registration ID:</b> MCI-DL-2015-77291 [VERIFIED]", styles['Normal']),
    Paragraph("<i>Digital Signed & Uploaded to Cloud Storage</i>", styles['Italic'])
]
doc1.build(story1)

# 2. Sample Donor Certificate
cert_path = os.path.join(UPLOAD_DIR, "cert_donor_1.pdf")
doc2 = SimpleDocTemplate(cert_path, pagesize=letter)
story2 = [
    Paragraph("<b>NATIONAL BLOOD TRANSFUSION COUNCIL - MEDICAL FITNESS CERTIFICATE</b>", styles['Heading2']),
    Spacer(1, 15),
    Paragraph("<b>Donor Name:</b> Pooja Sharma | <b>Blood Group:</b> A-Positive", styles['Normal']),
    Paragraph("<b>Hemoglobin Level:</b> 13.8 g/dL (Normal Range > 12.5 g/dL)", styles['Normal']),
    Paragraph("<b>Blood Pressure:</b> 120/80 mmHg | <b>Pulse:</b> 72 bpm", styles['Normal']),
    Paragraph("<b>Serology Screening (HIV, HBV, HCV, Syphilis, Malaria):</b> NON-REACTIVE (CLEAR)", styles['Normal']),
    Spacer(1, 15),
    Paragraph("<b>Medical Officer:</b> Dr. S. K. Gupta, Pathologist | <b>Status:</b> FIT TO DONATE", styles['Heading3'])
]
doc2.build(story2)

print("Sample mock medical documents generated in uploads/ folder.")
