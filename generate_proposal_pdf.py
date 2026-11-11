import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Cloud-Based Online Blood Bank System — Team Proposal")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 35, footer_text)
        self.drawString(54, 35, "CONFIDENTIAL & PROPRIETARY — ACADEMIC CLOUD COMPUTING PROJECT")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    primary_color = colors.HexColor("#B91C1C")   # Crimson Red
    navy_color = colors.HexColor("#1E293B")      # Slate Dark
    text_dark = colors.HexColor("#334155")       # Charcoal
    bg_light = colors.HexColor("#F8FAFC")        # Soft Gray
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        alignment=0,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=navy_color,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=navy_color,
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=text_dark,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=text_dark,
        leftIndent=15,
        spaceAfter=4
    )
    
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#991B1B")
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=text_dark
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.white
    )

    story = []
    
    # Title Banner
    story.append(Paragraph("PROJECT PROPOSAL & ARCHITECTURE", subtitle_style))
    story.append(Paragraph("Cloud-Based Online Blood Bank & Emergency Triage System", title_style))
    story.append(Paragraph("<b>Domain:</b> Cloud Computing (DBaaS, STaaS, PaaS) & Healthcare Analytics &nbsp;|&nbsp; <b>Target:</b> Team Alignment & Final Submission", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=15))
    
    # Section 1: Executive Summary & Story Walkthrough
    story.append(Paragraph("1. Project Concept — The Real-World Story", h1_style))
    story.append(Paragraph(
        "To understand the absolute power of this project, imagine a real-world critical scenario in any metro city:",
        body_style
    ))
    
    story_box_data = [[
        Paragraph(
            "<b>The Scenario:</b> A patient meets with a severe road accident and is rushed to Apollo Hospital. "
            "The trauma surgeon urgently requires <b>2 units of rare O-Negative (O-) blood</b> within 60 minutes to perform life-saving surgery.<br/><br/>"
            "<b>The Traditional Dilemma:</b> Without a centralized cloud system, the patient's family panics, making frantic phone calls to multiple independent blood banks, traveling across traffic, only to find the blood group is out of stock. Crucial golden hours are lost.<br/><br/>"
            "<b>How Our Cloud Platform Saves the Day:</b><br/>"
            "• <b>Real-Time Cloud Inventory Scan:</b> The hospital triage desk logs in and searches for O- stock across the city. Within 1 second, the system queries the <b>Cloud Database</b> and displays that Red Cross Blood Bank has 1 unit available. The hospital reserves it immediately.<br/>"
            "• <b>Emergency Broadcast Trigger:</b> For the 2nd missing unit, the doctor raises a verified <b>Emergency Blood Request</b> on the portal.<br/>"
            "• <b>Automated Cloud Alert:</b> The cloud backend immediately dispatches an urgent broadcast (Email/SMS) to all pre-registered O- donors in the city who have toggled their status to <i>'Available to Donate'</i>.<br/>"
            "• <b>Rapid Response:</b> A nearby registered donor accepts the notification, reports to the facility, donates blood, and their medical test fitness certificate is securely archived into <b>Cloud Object Storage</b>.<br/>"
            "• <b>Impact:</b> The life is saved in under 30 minutes, turning what would have been a logistics tragedy into a streamlined, automated success.",
            body_style
        )
    ]]
    t_story = Table(story_box_data, colWidths=[504])
    t_story.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF2F2")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FCA5A5")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_story)
    story.append(Spacer(1, 10))

    # Section 2: Three User Roles & Workflows
    story.append(Paragraph("2. System Users & Their End-to-End Workflows", h1_style))
    story.append(Paragraph(
        "The system has exactly <b>three distinct authenticated user personas</b>, ensuring clear role-based access control (RBAC):",
        body_style
    ))
    
    # User 1: Donor
    story.append(Paragraph("A. User Role 1: Blood Donor (Khoon Dene Wala)", h2_style))
    story.append(Paragraph("• <b>Registration & Profile:</b> Signs up with basic demographic details, city, contact info, and certified Blood Group (A+, A-, B+, B-, AB+, AB-, O+, O-).", bullet_style))
    story.append(Paragraph("• <b>Availability Toggle (Smart Privacy):</b> A real-time toggle switch: <i>'Available to Donate: YES / NO'</i>. If the donor is sick or traveling, they flip to 'NO' to avoid spam notifications.", bullet_style))
    story.append(Paragraph("• <b>Cloud Certificate Upload:</b> Uploads recent blood fitness reports or health certificates (automatically pushed to Cloud Storage).", bullet_style))
    story.append(Paragraph("• <b>Emergency Broadcast Feed:</b> Receives real-time urgent blood shortage alerts in their city with one-click acceptance.", bullet_style))
    
    # User 2: Hospital / Recipient
    story.append(Paragraph("B. User Role 2: Hospital / Patient Recipient (Khoon Lene Wala)", h2_style))
    story.append(Paragraph("• <b>Live Multi-Branch Inventory Search:</b> Selects City & Required Blood Group to instantly see available units across registered blood banks.", bullet_style))
    story.append(Paragraph("• <b>Standard vs. Emergency Blood Request:</b> Raises standard requests for scheduled surgeries, or triggers urgent priority requests for immediate trauma cases.", bullet_style))
    story.append(Paragraph("• <b>Verification Mandatory:</b> Must submit Doctor Registration Number (MCI/NMC ID) and upload Doctor's signed Emergency Slip.", bullet_style))
    story.append(Paragraph("• <b>Request Status Tracking:</b> Real-time status updates: <i>Pending → Approved → Dispatched</i>.", bullet_style))

    # User 3: Admin / Blood Bank Manager
    story.append(Paragraph("C. User Role 3: Blood Bank Manager / Administrator", h2_style))
    story.append(Paragraph("• <b>Live Inventory Control Board:</b> 8 dynamic metric meters showing live unit counts for every blood type.", bullet_style))
    story.append(Paragraph("• <b>Stock Inflow / Outflow Management:</b> Add newly collected blood bags with batch numbers and expiry dates.", bullet_style))
    story.append(Paragraph("• <b>Request Verification & Instant Deduction:</b> Reviews incoming hospital requests and attached doctor slips; approving automatically decrements units in the Cloud Database.", bullet_style))
    story.append(Paragraph("• <b>Executive Analytics Dashboard:</b> Visual PowerBI-style charts showing consumption trends, low-stock warnings, and donor demographics.", bullet_style))

    story.append(PageBreak())

    # Section 3: Solving Abuse & False Emergencies
    story.append(Paragraph("3. Smart Abuse Prevention & Verification Mechanism", h1_style))
    story.append(Paragraph(
        "<b>Critical Problem Addressed:</b> What prevents a hospital from falsely labeling every routine request as 'Emergency' to jump the queue?<br/>"
        "Our cloud platform incorporates a multi-tier verification and audit triage system:",
        body_style
    ))
    
    abuse_data = [
        [
            Paragraph("<b>Verification Feature</b>", table_header_style),
            Paragraph("<b>How It Works in the System</b>", table_header_style),
            Paragraph("<b>Real-World Protection</b>", table_header_style)
        ],
        [
            Paragraph("<b>1. Mandatory Doctor Slip & Medical ID</b>", table_cell_style),
            Paragraph("Hospital must provide attending Doctor's Medical Registration ID and upload the official Emergency Requisition Slip to Cloud Storage.", table_cell_style),
            Paragraph("Eliminates casual or non-clinical requests; creates medical accountability.", table_cell_style)
        ],
        [
            Paragraph("<b>2. Admin Verification Gatekeeper</b>", table_cell_style),
            Paragraph("Emergency requests appear highlighted in Crimson Red on the Admin Dashboard with a one-click proof viewer before stock release.", table_cell_style),
            Paragraph("Prevents unauthorized stock depletion without human authorization.", table_cell_style)
        ],
        [
            Paragraph("<b>3. Cloud Audit Trail & Hospital Trust Score</b>", table_cell_style),
            Paragraph("The cloud database logs every request timestamp, urgency tag, and post-surgery reconciliation reports.", table_cell_style),
            Paragraph("Hospitals that abuse emergency flags are automatically penalized and demoted in queue priority.", table_cell_style)
        ]
    ]
    t_abuse = Table(abuse_data, colWidths=[140, 214, 150])
    t_abuse.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light])
    ]))
    story.append(t_abuse)
    story.append(Spacer(1, 12))

    # Section 4: Cloud Computing Architecture
    story.append(Paragraph("4. Core Cloud Computing Architecture (Viva Defense)", h1_style))
    story.append(Paragraph(
        "When the academic evaluators or teachers ask: <i>'Where is the Cloud in your project?'</i>, "
        "the team has 4 concrete, technically rigorous pillars to present:",
        body_style
    ))

    cloud_pillars = [
        [
            Paragraph("<b>Cloud Service Pillar</b>", table_header_style),
            Paragraph("<b>Implementation Details</b>", table_header_style),
            Paragraph("<b>Evaluation Keyword for Viva</b>", table_header_style)
        ],
        [
            Paragraph("<b>1. Database-as-a-Service<br/>(DBaaS)</b>", table_cell_style),
            Paragraph("Centralized Cloud Database (PostgreSQL / Supabase / AWS RDS). Enables multi-facility synchronization in real-time.", table_cell_style),
            Paragraph("<i>High Availability, Consistency, Real-Time Sync</i>", table_cell_style)
        ],
        [
            Paragraph("<b>2. Storage-as-a-Service<br/>(STaaS)</b>", table_cell_style),
            Paragraph("Cloud Object Storage (AWS S3 / Cloud Bucket) for securely storing non-relational binary assets: Donor fitness PDFs and Doctor slips.", table_cell_style),
            Paragraph("<i>Unstructured Object Storage, Secure Signed URLs</i>", table_cell_style)
        ],
        [
            Paragraph("<b>3. Cloud Event Alerts<br/>(Notification API)</b>", table_cell_style),
            Paragraph("Automated event-triggered email/SMS notification system for critical blood shortages and emergency triage.", table_cell_style),
            Paragraph("<i>Event-Driven Architecture (EDA)</i>", table_cell_style)
        ],
        [
            Paragraph("<b>4. Platform-as-a-Service<br/>(PaaS Hosting)</b>", table_cell_style),
            Paragraph("Web application containerized/hosted on Cloud infrastructure (Streamlit Cloud / AWS Elastic Beanstalk / Render) with SSL encryption.", table_cell_style),
            Paragraph("<i>Scalability, Zero-Server Maintenance</i>", table_cell_style)
        ]
    ]
    t_cloud = Table(cloud_pillars, colWidths=[130, 234, 140])
    t_cloud.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light])
    ]))
    story.append(t_cloud)
    story.append(Spacer(1, 12))

    # Section 5: Team Skillset & Technology Stack
    story.append(Paragraph("5. Technology Stack & Skillset Mapping", h1_style))
    story.append(Paragraph(
        "The project perfectly utilizes existing core competencies while introducing cutting-edge cloud skills:",
        body_style
    ))

    skills_data = [
        [
            Paragraph("<b>Technology / Layer</b>", table_header_style),
            Paragraph("<b>Specific Tool Used</b>", table_header_style),
            Paragraph("<b>Role in the System</b>", table_header_style)
        ],
        [
            Paragraph("<b>Frontend & UI</b>", table_cell_style),
            Paragraph("HTML5, CSS3, Streamlit", table_cell_style),
            Paragraph("Interactive user dashboards, responsive design, urgency indicators.", table_cell_style)
        ],
        [
            Paragraph("<b>Backend Engine</b>", table_cell_style),
            Paragraph("Python (v3.10+)", table_cell_style),
            Paragraph("Business rules, triage routing, authentication, API orchestration.", table_cell_style)
        ],
        [
            Paragraph("<b>Database</b>", table_cell_style),
            Paragraph("SQL (Relational Schema)", table_cell_style),
            Paragraph("Inventory records, donor profiles, order audit trails, query optimization.", table_cell_style)
        ],
        [
            Paragraph("<b>Business Analytics</b>", table_cell_style),
            Paragraph("PowerBI / Python Data Visuals", table_cell_style),
            Paragraph("Executive graphs: Stock exhaustion forecasts, donor turnout rates.", table_cell_style)
        ],
        [
            Paragraph("<b>Cloud Infrastructure</b>", table_cell_style),
            Paragraph("Cloud SQL, S3 Object Storage", table_cell_style),
            Paragraph("Multi-site data replication, cloud file archiving, 24/7 web availability.", table_cell_style)
        ]
    ]
    t_skills = Table(skills_data, colWidths=[120, 150, 234])
    t_skills.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light])
    ]))
    story.append(t_skills)
    story.append(Spacer(1, 12))

    # Section 6: Key Viva & Defense Questions
    story.append(Paragraph("6. Quick Viva Preparation Checklist (For Team Defense)", h1_style))
    story.append(Paragraph("<b>Q1: Why did you not use a local database like MS Access or standard SQLite?</b><br/>"
                           "<i>Answer:</i> In a healthcare emergency system, multiple hospitals, blood banks, and donors access data simultaneously. A local DB is siloed on one machine; a Cloud Database ensures real-time ACID-compliant multi-branch concurrency.", bullet_style))
    story.append(Paragraph("<b>Q2: How is data privacy maintained for donors?</b><br/>"
                           "<i>Answer:</i> Donors can toggle availability off at any time. Phone numbers are protected, and health reports are stored in secure cloud buckets with access restricted to authenticated staff.", bullet_style))
    story.append(Paragraph("<b>Q3: What makes this superior to traditional blood bank projects?</b><br/>"
                           "<i>Answer:</i> Proof-based emergency prioritization, live multi-site cloud inventory, and automated alert broadcast mechanisms.", bullet_style))
    
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=10))
    story.append(Paragraph("<b>Summary:</b> This proposal represents a comprehensive, production-grade cloud computing solution designed for rapid presentation and top-tier academic evaluation.", callout_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {filename}")

if __name__ == "__main__":
    output_path = r"c:\Users\rajpu\OneDrive\Desktop\Training\Cloud_Blood_Bank_Project_Proposal.pdf"
    build_pdf(output_path)
