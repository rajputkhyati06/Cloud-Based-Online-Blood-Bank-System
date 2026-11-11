import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
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
            self.drawString(54, 750, "Cloud Based Online Blood Bank & Emergency Triage System — Final Blueprint")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 30, footer_text)
        self.drawString(54, 30, "ACADEMIC CLOUD COMPUTING PROJECT — ALL ADD-ONS & PHASE ROADMAP INCLUDED")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 42, 558, 42)
        self.restoreState()

def build_complete_hinglish_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#B91C1C")   # Crimson Red
    navy_color = colors.HexColor("#0F172A")      # Slate Dark
    text_dark = colors.HexColor("#334155")       # Charcoal
    bg_light = colors.HexColor("#F8FAFC")
    accent_green = colors.HexColor("#065F46")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=navy_color,
        spaceAfter=10
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=4
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=navy_color,
        spaceBefore=6,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=text_dark,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=text_dark,
        leftIndent=10,
        spaceAfter=2.5
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=text_dark
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    story = []
    
    # Title Banner
    story.append(Paragraph("COMPLETE FINAL PROJECT BLUEPRINT (HINGLISH)", subtitle_style))
    story.append(Paragraph("Cloud Based Online Blood Bank & Emergency Triage System", title_style))
    story.append(Paragraph("<b>Domain:</b> Cloud Computing (DBaaS, STaaS, PaaS) &nbsp;|&nbsp; <b>Features:</b> All Smart Add-Ons & Phase-wise Development Plan", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))
    
    # Section 1: Real-Life Story & Blood Location Hierarchy
    story.append(Paragraph("1. Real-Life Kahani Aur Blood Sourcing Ka Rule", h1_style))
    story_box = [[
        Paragraph(
            "<b>A. Critical Accident Scenario:</b><br/>"
            "Ek critical accident patient ko 60 minute ke andar rare <b>O-negative (O-) blood</b> ki 2 units chahiye hoti hain.<br/><br/>"
            "<b>B. Blood Kahan Hota Hai? (The 2-Tier Rule):</b><br/>"
            "• <b>Tier 1: Pre-Stored Inventory (Fridge / Cold Storage 2°C - 6°C):</b> Pehle se tested aur certified blood bags blood bank ke cold storage mein hote hain. Jab hospital ko blood chahiye, toh pehla check Cloud Inventory par hota hai. Agar stock hai, toh wahi se dispatch hota hai — <b>is stage par donors ko disturb NAHI kiya jata</b> taaki unhe spam na ho.<br/>"
            "• <b>Tier 2: Emergency Alert (Stock = 0 Hone Par):</b> Agar shahar ke kisi bhi blood bank mein required blood group ka stock 0 ho jata hai, tab Cloud system turant shahar ke registered donors ko <b>Emergency Broadcast (SMS/Email)</b> trigger karta hai. Donor aakar fresh blood donate karta hai aur jaan bach jati hai!",
            body_style
        )
    ]]
    t_story = Table(story_box, colWidths=[512])
    t_story.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF2F2")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FCA5A5")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_story)
    story.append(Spacer(1, 6))

    # Section 2: Comparison with Existing Portals
    story.append(Paragraph("2. Purane Systems (e-RaktKosh) Se Hamara System Kaise Behtar Hai?", h1_style))
    comp_table = [
        [
            Paragraph("<b>Feature / Problem</b>", table_header_style),
            Paragraph("<b>Purane Systems (e-RaktKosh / Local Apps)</b>", table_header_style),
            Paragraph("<b>Hamara Cloud-Native Solution</b>", table_header_style)
        ],
        [
            Paragraph("<b>Data Updates</b>", table_cell_style),
            Paragraph("Hafte mein 1 baar manual update. Hospital jakar pata chalta hai ki blood khatam hai.", table_cell_style),
            Paragraph("<b>Real-Time Cloud Database:</b> Har transaction par live stock 1 second mein sync hota hai.", table_cell_style)
        ],
        [
            Paragraph("<b>Blood Expiry / Wastage</b>", table_cell_style),
            Paragraph("Expiry tracking na hone ki wajah se hazaron bags fridge mein expire ho kar waste hote hain.", table_cell_style),
            Paragraph("<b>FIFO Expiry Engine:</b> Jo bag pehle expire hoga, system use pehle dispatch karega.", table_cell_style)
        ],
        [
            Paragraph("<b>Emergency Broadcast</b>", table_cell_style),
            Paragraph("Koi automated verified alert nahi. WhatsApp par fake forwards bhatakte hain.", table_cell_style),
            Paragraph("<b>Doctor-Verified Cloud Alert:</b> Doctor ka parcha upload hone par hi targetted alert jata hai.", table_cell_style)
        ]
    ]
    t_comp = Table(comp_table, colWidths=[110, 192, 210])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light])
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 6))

    # Section 3: The 3 Users Workflow
    story.append(Paragraph("3. Teeno Users Ka Workflow (Kaam Kaise Hoga)", h1_style))
    story.append(Paragraph("• <b>User 1 (Donor):</b> Register karega → <i>'Available to Donate: YES/NO'</i> toggle karega → Health Certificate Cloud Storage par upload karega → Emergency alert aane par blood donate karega → <b>Life-Saver Certificate PDF</b> download karega.", bullet_style))
    story.append(Paragraph("• <b>User 2 (Hospital / Recipient):</b> City aur Blood Group search karega → Compatibility checker se alternative group dekhega → Emergency Request raise karke Doctor ka signed parcha upload karega → Approval ke baad <b>Digital Delivery Gate-Pass PDF</b> download karega.", bullet_style))
    story.append(Paragraph("• <b>User 3 (Blood Bank Manager):</b> 8-grid live stock meters dekhega → Incoming emergency request aur doctor slip verify karke Approve karega (Cloud DB se stock auto-deduct hoga) → FIFO order follow karega → Analytics dashboard check karega.", bullet_style))

    story.append(PageBreak())

    # Section 4: All Smart Add-Ons Included
    story.append(Paragraph("4. Project Mein Shamil Kiye Gaye Saare Smart Add-Ons", h1_style))
    story.append(Paragraph("Yeh features humare project ko dusre ordinary projects se bohot aage le aate hain:", body_style))

    addons_table = [
        [
            Paragraph("<b>Add-On Feature</b>", table_header_style),
            Paragraph("<b>Yeh Kya Karta Hai? (Function)</b>", table_header_style),
            Paragraph("<b>Examiner / Viva Impact</b>", table_header_style)
        ],
        [
            Paragraph("<b>1. Smart Compatibility Checker</b>", table_cell_style),
            Paragraph("RBC match matrix: Agar AB+ patient ko khoon chahiye, toh system batayega ki wo A+, B+, O+ bhi le sakta hai. O- Universal Donor aur AB+ Universal Recipient logic.", table_cell_style),
            Paragraph("Dikhata hai ki system mein medical domain intelligence dali gayi hai.", table_cell_style)
        ],
        [
            Paragraph("<b>2. FIFO Blood Expiry Engine (35-Day Rule)</b>", table_cell_style),
            Paragraph("Blood cells 35 din baad expire hote hain aur unhe incinerator mein jalana padta hai. System pehle un bags ko release karta hai jinki expiry paas ho.", table_cell_style),
            Paragraph("Zero wastage logic; real-world bio-medical logistics problem ko solve karta hai.", table_cell_style)
        ],
        [
            Paragraph("<b>3. Doctor Verification & Abuse Prevention</b>", table_cell_style),
            Paragraph("Doctor Registration ID aur signed Emergency Slip upload karna compulsory hai. Fake emergency daalne par hospital flag hota hai.", table_cell_style),
            Paragraph("Examiner ko batata hai ki aapne system fraud aur queue jumping par deeply socha hai.", table_cell_style)
        ],
        [
            Paragraph("<b>4. Hospital Digital Gate-Pass (PDF)</b>", table_cell_style),
            Paragraph("Approval ke baad hospital ke liye ek token number aur dispatch details ke sath official delivery receipt generate hoti hai.", table_cell_style),
            Paragraph("Complete end-to-end supply chain loop dikhata hai.", table_cell_style)
        ],
        [
            Paragraph("<b>5. Donor Life-Saver Certificate (PDF)</b>", table_cell_style),
            Paragraph("Donation complete hone par donor ko Cloud-automated appreciation certificate download karne ka option milta hai.", table_cell_style),
            Paragraph("Donor motivation aur Cloud Document Generation ka live proof.", table_cell_style)
        ],
        [
            Paragraph("<b>6. Executive Analytics Dashboard</b>", table_cell_style),
            Paragraph("PowerBI-style visual charts: Stock shortage warnings, monthly consumption, aur city-wise demand.", table_cell_style),
            Paragraph("Data Analytics aur Business Intelligence skills ka direct demonstration.", table_cell_style)
        ]
    ]
    t_addons = Table(addons_table, colWidths=[120, 242, 150])
    t_addons.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light])
    ]))
    story.append(t_addons)
    story.append(Spacer(1, 8))

    # Section 5: Development Phases (Kaise aur Kitne Phase Mein Banega)
    story.append(Paragraph("5. Project Development Roadmap (Kaise Aur Kitne Phase Mein Banega)", h1_style))
    story.append(Paragraph(
        "Kal ke submission ke hisaab se hum is project ko <b>4 clear, structured phases</b> mein build karenge:",
        body_style
    ))

    phase_table = [
        [
            Paragraph("<b>Phase</b>", table_header_style),
            Paragraph("<b>Kaam (Tasks)</b>", table_header_style),
            Paragraph("<b>Output / Deliverable</b>", table_header_style)
        ],
        [
            Paragraph("<b>Phase 1:<br/>Database & Cloud Backend</b>", table_cell_style),
            Paragraph("• SQL Schema design (Users, Blood_Stock, Requests, Donors, Logs)<br/>• Python connection engine aur sample initial inventory data insert karna.", table_cell_style),
            Paragraph("Working Centralized Database ready jisme saara blood stock store hoga.", table_cell_style)
        ],
        [
            Paragraph("<b>Phase 2:<br/>UI Screens & Modern Design</b>", table_cell_style),
            Paragraph("• Login & Sign-up page (Donor, Hospital, Admin roles)<br/>• HTML/CSS styled modern cards aur red emergency themes.", table_cell_style),
            Paragraph("Sundar, interactive screens jahan har user type login kar sakega.", table_cell_style)
        ],
        [
            Paragraph("<b>Phase 3:<br/>Core Logic & Cloud Operations</b>", table_cell_style),
            Paragraph("• Inventory search aur direct reservation<br/>• Emergency broadcast engine (jab stock=0 ho)<br/>• Doctor prescription slip upload to Cloud Storage.", table_cell_style),
            Paragraph("End-to-end data flow aur automated alerts kaam karne lagenge.", table_cell_style)
        ],
        [
            Paragraph("<b>Phase 4:<br/>Smart Add-Ons & PDF Generators</b>", table_cell_style),
            Paragraph("• Compatibility checker matrix<br/>• FIFO Expiry tracking tags<br/>• Hospital Gate-Pass PDF aur Donor Life-Saver Certificate PDF generation.", table_cell_style),
            Paragraph("Dono PDF dynamic download honge aur FIFO wastage prevent karega.", table_cell_style)
        ],
        [
            Paragraph("<b>Phase 5:<br/>Analytics Dashboard & Final Testing</b>", table_cell_style),
            Paragraph("• PowerBI-style charts (Shortage warnings, demand trends)<br/>• End-to-end demo testing aur Viva preparation guide.", table_cell_style),
            Paragraph("100% complete, submission-ready project aapke system par live chalega!", table_cell_style)
        ]
    ]
    t_phase = Table(phase_table, colWidths=[100, 242, 170])
    t_phase.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light])
    ]))
    story.append(t_phase)
    story.append(Spacer(1, 8))

    # Section 6: Viva Ready Checklist
    story.append(Paragraph("6. Viva & Presentation Checklist (Examiner Ko Impress Karne Ke Liye)", h1_style))
    story.append(Paragraph("<b>Q: Isme Cloud Computing kahan hai?</b><br/>"
                           "<i>Ans:</i> DBaaS (Centralized Cloud Database for real-time multi-hospital sync), STaaS (Cloud Object Storage for prescriptions and certificates), Event-Driven Cloud Notification (Alerts when stock=0), and PaaS (Cloud Web Hosting).", bullet_style))
    story.append(Paragraph("<b>Q: Blood expiry par aapka system kya karta hai?</b><br/>"
                           "<i>Ans:</i> Humne FIFO (First-In, First-Out) algorithm lagaya hai jo sabse pehle un bags ko dispatch karta hai jinki 35-day shelf-life khatam hone wali ho, taaki bio-hazard wastage na ho.", bullet_style))
    story.append(Paragraph("<b>Q: Fake emergency ko kaise roka?</b><br/>"
                           "<i>Ans:</i> Doctor Registration ID aur signed emergency slip upload karna mandatory hai, jise admin verify karta hai.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Complete Final Hinglish PDF successfully generated at: {filename}")

if __name__ == "__main__":
    output_path = r"c:\Users\rajpu\OneDrive\Desktop\Training\Cloud_Blood_Bank_Project_Proposal_Hinglish.pdf"
    build_complete_hinglish_pdf(output_path)
