import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml
import os
import shutil

def create_presentation():
    prs = pptx.Presentation()
    # 16:9 Widescreen dimensions (13.333" x 7.5")
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Definitions
    DARK_BG       = RGBColor(15, 23, 42)      # Slate 900
    LIGHT_BG      = RGBColor(248, 250, 252)  # Slate 50
    CARD_BG       = RGBColor(255, 255, 255)  # Pure White
    BORDER_COL    = RGBColor(226, 232, 240)  # Slate 200
    
    PRIMARY_RED   = RGBColor(220, 38, 38)    # Crimson 600
    DARK_RED      = RGBColor(185, 28, 28)    # Red 700
    SOFT_RED      = RGBColor(254, 242, 242)  # Red 50
    
    NAVY_BLUE     = RGBColor(29, 78, 216)    # Blue 700
    SOFT_BLUE     = RGBColor(239, 246, 255)  # Blue 50
    
    EMERALD_GREEN = RGBColor(5, 150, 105)    # Emerald 600
    SOFT_GREEN    = RGBColor(236, 253, 245)  # Emerald 50
    
    VIOLET        = RGBColor(124, 58, 237)   # Violet 600
    SOFT_VIOLET   = RGBColor(245, 243, 255)  # Violet 50

    AMBER         = RGBColor(217, 119, 6)    # Amber 600
    SOFT_AMBER    = RGBColor(255, 251, 235)  # Amber 50

    TEXT_DARK     = RGBColor(15, 23, 42)     # Slate 900
    TEXT_MUTED    = RGBColor(100, 116, 139)  # Slate 500
    TEXT_LIGHT    = RGBColor(255, 255, 255)  # White

    def add_slide_transition(slide, trans_type="push"):
        """Hardware-accelerated smooth slide transitions"""
        try:
            if trans_type == "push":
                trans_xml = parse_xml(
                    '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med">'
                    '<p:push dir="l"/>'
                    '</p:transition>'
                )
            elif trans_type == "fade":
                trans_xml = parse_xml(
                    '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med">'
                    '<p:fade/>'
                    '</p:transition>'
                )
            else:
                trans_xml = parse_xml(
                    '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med">'
                    '<p:push dir="l"/>'
                    '</p:transition>'
                )
            slide._element.append(trans_xml)
        except Exception as e:
            print("Transition error:", e)

    def add_clean_header(slide, badge_text, main_title):
        """Header with large title and category badge"""
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = LIGHT_BG
        bg.line.fill.background()

        # Category Pill Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.38), Inches(2.6), Inches(0.32))
        badge.fill.solid()
        badge.fill.fore_color.rgb = SOFT_RED
        badge.line.color.rgb = PRIMARY_RED
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = badge_text.upper()
        p_b.alignment = PP_ALIGN.CENTER
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = PRIMARY_RED

        # Main Title (Large, Bold, Clean)
        title_box = slide.shapes.add_textbox(Inches(0.75), Inches(0.75), Inches(11.8), Inches(0.55))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = main_title
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_DARK

        # Footer
        foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.18), Inches(11.733), Inches(0.25))
        tf_f = foot_box.text_frame
        tf_f.margin_top = tf_f.margin_bottom = tf_f.margin_left = tf_f.margin_right = 0
        pf = tf_f.paragraphs[0]
        pf.text = "RV Institute of Technology, Bijnor  •  B.Tech CSE (2026-27)"
        pf.font.size = Pt(9.5)
        pf.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Modern Dark Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_slide_transition(s1, "fade")

    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_BG
    bg1.line.fill.background()

    top_glow = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.1))
    top_glow.fill.solid()
    top_glow.fill.fore_color.rgb = PRIMARY_RED
    top_glow.line.fill.background()

    # College Logo
    logo_path = "synopsis_assets/rvit_logo.png"
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(0.8), Inches(0.55), width=Inches(1.2))

    col_box = s1.shapes.add_textbox(Inches(2.2), Inches(0.55), Inches(10.3), Inches(0.8))
    tf_c = col_box.text_frame
    p_c1 = tf_c.paragraphs[0]
    p_c1.text = "RV INSTITUTE OF TECHNOLOGY, BIJNOR"
    p_c1.font.size = Pt(15)
    p_c1.font.bold = True
    p_c1.font.color.rgb = RGBColor(226, 232, 240)

    p_c2 = tf_c.add_paragraph()
    p_c2.text = "Affiliated to Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow"
    p_c2.font.size = Pt(11)
    p_c2.font.color.rgb = RGBColor(148, 163, 184)

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.733), Inches(1.5))
    tf_t1 = t_box.text_frame
    tf_t1.word_wrap = True
    p_proj = tf_t1.paragraphs[0]
    p_proj.text = "Cloud-Based Online Blood Bank &\nEmergency Triage System"
    p_proj.font.size = Pt(30)
    p_proj.font.bold = True
    p_proj.font.color.rgb = TEXT_LIGHT

    p_sub1 = tf_t1.add_paragraph()
    p_sub1.text = "A Smart Life-Saving Platform Connecting Donors & Hospitals in Real Time"
    p_sub1.font.size = Pt(14)
    p_sub1.font.color.rgb = RGBColor(252, 165, 165)

    # Team Card
    team_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.75), Inches(7.2), Inches(3.1))
    team_card.fill.solid()
    team_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    team_card.line.color.rgb = RGBColor(51, 65, 85)
    team_card.line.width = Pt(1)

    tf_tc = team_card.text_frame
    tf_tc.word_wrap = True
    tf_tc.margin_left = tf_tc.margin_top = Inches(0.28)
    p_tc_h = tf_tc.paragraphs[0]
    p_tc_h.text = "SUBMITTED BY:"
    p_tc_h.font.size = Pt(11)
    p_tc_h.font.bold = True
    p_tc_h.font.color.rgb = RGBColor(252, 165, 165)

    members = [
        ("Khyati Rajput", "2305010100024"),
        ("Kashish Tyagi", "2305010100023"),
        ("Aksha Parveen", "2305010100005"),
        ("Aaditya Yadav", "2305010100001")
    ]
    for name, roll in members:
        p_m = tf_tc.add_paragraph()
        p_m.text = f"•  {name}   ({roll})"
        p_m.font.size = Pt(13)
        p_m.font.color.rgb = TEXT_LIGHT

    p_deg = tf_tc.add_paragraph()
    p_deg.text = "B.Tech Computer Science & Engineering (4th Year, 2026-27)"
    p_deg.font.size = Pt(10)
    p_deg.font.color.rgb = RGBColor(148, 163, 184)

    # Guide Card
    guide_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(3.75), Inches(4.2), Inches(3.1))
    guide_card.fill.solid()
    guide_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    guide_card.line.color.rgb = RGBColor(51, 65, 85)
    guide_card.line.width = Pt(1)

    tf_gc = guide_card.text_frame
    tf_gc.word_wrap = True
    tf_gc.margin_left = tf_gc.margin_top = Inches(0.28)
    p_gc_h = tf_gc.paragraphs[0]
    p_gc_h.text = "UNDER THE GUIDANCE OF:"
    p_gc_h.font.size = Pt(11)
    p_gc_h.font.bold = True
    p_gc_h.font.color.rgb = RGBColor(147, 197, 253)

    p_gname = tf_gc.add_paragraph()
    p_gname.text = "Mr. Manish Kumar"
    p_gname.font.size = Pt(18)
    p_gname.font.bold = True
    p_gname.font.color.rgb = TEXT_LIGHT

    p_gdes = tf_gc.add_paragraph()
    p_gdes.text = "Trainer & Project Guide\nDepartment of CSE\nRV Institute of Technology, Bijnor"
    p_gdes.font.size = Pt(11.5)
    p_gdes.font.color.rgb = RGBColor(203, 213, 225)


    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT (Current Challenges)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_transition(s2, "push")
    add_clean_header(s2, "Problem Statement", "Current Challenges in Blood Banking")

    problems = [
        ("📞 1. Manual Phone Calls", "30 - 45 Mins Delay", 
         ["• Calling donors manually during surgery", "• Time lost in critical golden hour", "• High stress on patient families"],
         PRIMARY_RED, SOFT_RED),
        ("📦 2. Blood Expiration", "Severe Wastage", 
         ["• No automated expiry tracking", "• Safe blood packets expire on shelves", "• Shortage despite willing donors"],
         AMBER, SOFT_AMBER),
        ("📍 3. Zero Live Tracking", "Panic & Confusion", 
         ["• No real-time stock visibility", "• Blind visits hospital to hospital", "• No GPS matching for nearest donors"],
         NAVY_BLUE, SOFT_BLUE)
    ]

    card_w = Inches(3.7)
    gap = Inches(0.3)
    for i, (title, tag, points, color, soft_bg) in enumerate(problems):
        cx = Inches(0.8) + i * (card_w + gap)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.5), card_w, Inches(4.5))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tb = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.25), Inches(1.75), card_w - Inches(0.5), Inches(0.4))
        tb.fill.solid()
        tb.fill.fore_color.rgb = soft_bg
        tb.line.color.rgb = color
        tb.line.width = Pt(1)
        tf_tb = tb.text_frame
        p_tb = tf_tb.paragraphs[0]
        p_tb.text = tag.upper()
        p_tb.alignment = PP_ALIGN.CENTER
        p_tb.font.size = Pt(11)
        p_tb.font.bold = True
        p_tb.font.color.rgb = color

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.85)
        tf.margin_left = tf.margin_right = Inches(0.25)

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_DARK

        tf.add_paragraph()

        for pt in points:
            p_pt = tf.add_paragraph()
            p_pt.text = pt
            p_pt.font.size = Pt(13)
            p_pt.font.color.rgb = TEXT_DARK

    b_strip = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.2), Inches(11.733), Inches(0.75))
    b_strip.fill.solid()
    b_strip.fill.fore_color.rgb = SOFT_GREEN
    b_strip.line.color.rgb = EMERALD_GREEN
    b_strip.line.width = Pt(1)
    tf_bs = b_strip.text_frame
    p_bs = tf_bs.paragraphs[0]
    p_bs.text = "🎯 OUR GOAL: Broadcast alerts & locate matching blood in UNDER 2 SECONDS!"
    p_bs.alignment = PP_ALIGN.CENTER
    p_bs.font.size = Pt(14)
    p_bs.font.bold = True
    p_bs.font.color.rgb = EMERALD_GREEN


    # =========================================================================
    # SLIDE 3: PROPOSED SOLUTION (4 Key Pillars)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_transition(s3, "push")
    add_clean_header(s3, "Proposed Solution", "Our Solution: 4 Smart Pillars")

    sol_cards = [
        ("🚨 1. Real-Time Emergency SOS", "Broadcasts in < 2 seconds",
         ["• 1-Click urgent broadcast", "• Direct SMS & WhatsApp alerts", "• Priority emergency triage"],
         PRIMARY_RED, SOFT_RED),
        ("📍 2. Live GPS Donor Matching", "5 - 10 KM Radius",
         ["• Hyper-local donor search", "• Google Maps directions", "• Fastest response time"],
         NAVY_BLUE, SOFT_BLUE),
        ("⏱️ 3. Smart FIFO Blood Tracking", "Stops Expiration Wastage",
         ["• Dispenses oldest safe unit first", "• Real-time stock dashboard", "• 90%+ wastage reduction"],
         EMERALD_GREEN, SOFT_GREEN),
        ("🔒 4. Verified & Safe Network", "Zero Fraud Requisitions",
         ["• Hospital license verification", "• Donor OTP authentication", "• Tamper-proof audit logs"],
         VIOLET, SOFT_VIOLET)
    ]

    col_w = Inches(5.7)
    row_h = Inches(2.55)
    coords3 = [
        (Inches(0.8), Inches(1.5)),
        (Inches(6.8), Inches(1.5)),
        (Inches(0.8), Inches(4.3)),
        (Inches(6.8), Inches(4.3))
    ]

    for (title, tag, pts, acc_c, soft_c), (x, y) in zip(sol_cards, coords3):
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, col_w, row_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = acc_c
        card.line.width = Pt(1.5)

        strip = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), row_h)
        strip.fill.solid()
        strip.fill.fore_color.rgb = acc_c
        strip.line.fill.background()

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_right = tf.margin_top = Inches(0.18)

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = acc_c

        p_tag = tf.add_paragraph()
        p_tag.text = "⚡ " + tag
        p_tag.font.size = Pt(12)
        p_tag.font.bold = True
        p_tag.font.color.rgb = TEXT_MUTED

        for pt in pts:
            pb = tf.add_paragraph()
            pb.text = pt
            pb.font.size = Pt(12.5)
            pb.font.color.rgb = TEXT_DARK


    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE (Cloud 3-Tier)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_transition(s4, "push")
    add_clean_header(s4, "Technical Design", "System Architecture (3-Tier Cloud)")

    arch_img = "synopsis_assets/architecture_diagram.png"
    if os.path.exists(arch_img):
        s4.shapes.add_picture(arch_img, Inches(0.8), Inches(1.5), width=Inches(7.6))

    layers = [
        ("💻 Layer 1: Frontend", "React.js Web App", "• Donors, Hospitals & Admin Portals\n• Works smoothly on Mobile & Desktop", NAVY_BLUE),
        ("⚙️ Layer 2: Backend API", "Node.js / Python REST API", "• Real-time GPS radius search\n• Instant SMS / WhatsApp broadcast", PRIMARY_RED),
        ("☁️ Layer 3: Cloud Database", "PostgreSQL Cloud", "• Real-time blood inventory counters\n• Secure 3NF normalized tables", EMERALD_GREEN)
    ]

    for i, (layer_name, tech, bullets, color) in enumerate(layers):
        ly = Inches(1.5) + i * Inches(1.75)
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.7), ly, Inches(3.8), Inches(1.55))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.18)

        p1 = tf.paragraphs[0]
        p1.text = layer_name
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = tech
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_DARK

        p3 = tf.add_paragraph()
        p3.text = bullets
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_MUTED


    # =========================================================================
    # SLIDE 5: USER MODULES & ROLES
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_transition(s5, "push")
    add_clean_header(s5, "System Modules", "Core User Roles & Portals")

    roles = [
        ("🩸 1. Donors", "Citizens & Volunteers",
         ["• Profile & Blood Group", "• Donation History", "• Live SOS Alerts", "• Accept / Decline Request"],
         PRIMARY_RED, SOFT_RED),
        ("🏥 2. Hospitals", "Doctors & ICU Staff",
         ["• Post Emergency Requests", "• View Live Stock Map", "• Track Blood Delivery", "• Confirm Unit Receipt"],
         NAVY_BLUE, SOFT_BLUE),
        ("🏢 3. Blood Banks", "Certified Centers",
         ["• Manage Blood Inventory", "• Expiration Date Alerts", "• FIFO Unit Dispatch", "• Maintain Buffer Stock"],
         EMERALD_GREEN, SOFT_GREEN),
        ("🛡️ 4. Admin", "Healthcare Authority",
         ["• Hospital Verification", "• License Approval", "• Fraud Prevention", "• City-Wide Analytics"],
         VIOLET, SOFT_VIOLET)
    ]

    r_w = Inches(2.7)
    r_gap = Inches(0.28)
    for i, (title, sub, bullets, color, soft_c) in enumerate(roles):
        rx = Inches(0.8) + i * (r_w + r_gap)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, Inches(1.5), r_w, Inches(5.3))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.22)

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED

        tf.add_paragraph()

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = b
            pb.font.size = Pt(12.5)
            pb.font.color.rgb = TEXT_DARK


    # =========================================================================
    # SLIDE 6: TECHNOLOGY STACK & TOOLS (Replaces DFD/ER)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_transition(s6, "push")
    add_clean_header(s6, "Technology Stack", "Technologies & Tools Used")

    tech_cards = [
        ("💻 Frontend", "Modern Web Interface",
         ["• React.js (Component UI)", "• Tailwind CSS (Responsive Design)", "• Axios (High-Speed API Calls)", "• Progressive Web App (Mobile)"],
         NAVY_BLUE, SOFT_BLUE),
        ("⚙️ Backend API", "Server-Side Engine",
         ["• Node.js & Express / Python", "• RESTful API Endpoints", "• JWT Token Authentication", "• Geolib (Radius Matching)"],
         PRIMARY_RED, SOFT_RED),
        ("☁️ Database & Cloud", "Reliable Data Storage",
         ["• PostgreSQL Relational DB", "• Supabase Cloud Hosting", "• Encrypted Password Hashing", "• Real-Time Stock Webhooks"],
         EMERALD_GREEN, SOFT_GREEN),
        ("🔌 Third-Party APIs", "Services & Deployment",
         ["• Google Maps API (Routing)", "• Twilio SMS / WhatsApp API", "• GitHub (Version Control)", "• Render / AWS Free-Tier"],
         VIOLET, SOFT_VIOLET)
    ]

    for (title, tag, pts, acc_c, soft_c), (x, y) in zip(tech_cards, coords3):
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, col_w, row_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = acc_c
        card.line.width = Pt(1.5)

        strip = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), row_h)
        strip.fill.solid()
        strip.fill.fore_color.rgb = acc_c
        strip.line.fill.background()

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_right = tf.margin_top = Inches(0.18)

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = acc_c

        p_tag = tf.add_paragraph()
        p_tag.text = "⚡ " + tag
        p_tag.font.size = Pt(12)
        p_tag.font.bold = True
        p_tag.font.color.rgb = TEXT_MUTED

        for pt in pts:
            pb = tf.add_paragraph()
            pb.text = pt
            pb.font.size = Pt(12.5)
            pb.font.color.rgb = TEXT_DARK


    # =========================================================================
    # SLIDE 7: WORKING WORKFLOW (Step-by-Step Operation)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_transition(s7, "push")
    add_clean_header(s7, "System Operation", "Working Workflow: How System Operates")

    workflow_steps = [
        ("Step 1: Emergency Blood Request", "Hospital Portal",
         ["• Doctor logs in with credentials", "• Inputs patient blood group & units", "• Flags urgency (Critical / High / Normal)"],
         PRIMARY_RED, SOFT_RED),
        ("Step 2: Automated Smart Triage", "Cloud Engine",
         ["• Scans live blood bank inventory", "• Checks oldest safe blood unit (FIFO)", "• Scans active donors in 5-10 km radius"],
         NAVY_BLUE, SOFT_BLUE),
        ("Step 3: Instant Dispatch or SOS", "Action Trigger",
         ["• If Available: Reserves unit immediately", "• If Shortage: Triggers SMS SOS to donors", "• Donors accept via 1-click mobile link"],
         EMERALD_GREEN, SOFT_GREEN),
        ("Step 4: Delivery & Confirmation", "Complete Loop",
         ["• Live GPS route link shared", "• Safe handover confirmed by doctor", "• Inventory updated automatically"],
         VIOLET, SOFT_VIOLET)
    ]

    for (title, tag, pts, acc_c, soft_c), (x, y) in zip(workflow_steps, coords3):
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, col_w, row_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = acc_c
        card.line.width = Pt(1.5)

        strip = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.12), row_h)
        strip.fill.solid()
        strip.fill.fore_color.rgb = acc_c
        strip.line.fill.background()

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_right = tf.margin_top = Inches(0.18)

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = acc_c

        p_tag = tf.add_paragraph()
        p_tag.text = "📍 " + tag
        p_tag.font.size = Pt(12)
        p_tag.font.bold = True
        p_tag.font.color.rgb = TEXT_MUTED

        for pt in pts:
            pb = tf.add_paragraph()
            pb.text = pt
            pb.font.size = Pt(12.5)
            pb.font.color.rgb = TEXT_DARK


    # =========================================================================
    # SLIDE 8: SMART FIFO DISPATCH FLOWCHART
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_transition(s8, "push")
    add_clean_header(s8, "Smart Algorithm", "Smart FIFO Blood Dispatch Flowchart")

    fifo_img = "synopsis_assets/fifo_flowchart.png"
    if os.path.exists(fifo_img):
        s8.shapes.add_picture(fifo_img, Inches(0.8), Inches(1.5), width=Inches(7.6))

    fifo_pts = [
        ("1️⃣ Check Stock", "System checks if requested blood group is in storage.", NAVY_BLUE),
        ("2️⃣ If Available (FIFO)", "Dispenses OLDEST safe unit first to completely avoid expiration.", EMERALD_GREEN),
        ("3️⃣ If Out of Stock (SOS)", "Automatically broadcasts SOS alerts to matching nearby donors.", PRIMARY_RED)
    ]

    for i, (title, desc, color) in enumerate(fifo_pts):
        fy = Inches(1.5) + i * Inches(1.75)
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.7), fy, Inches(3.8), Inches(1.55))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.18)

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_DARK


    # =========================================================================
    # SLIDE 9: KEY RESULTS & IMPACT (HUGE NUMBERS!)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_transition(s9, "push")
    add_clean_header(s9, "Key Achievements", "Project Results & Real-World Impact")

    metrics = [
        ("⚡ < 2 SECONDS", "Emergency Alert Speed", "Traditional calls took 30-45 mins. Our broadcast takes under 2 seconds.", PRIMARY_RED),
        ("📉 90% REDUCTION", "Blood Expiry Wastage", "FIFO algorithm ensures older safe units are used before they expire.", EMERALD_GREEN),
        ("📍 5 - 10 KM", "Hyper-Local Donor Radius", "Locates closest donors first, cutting travel time and traffic delays.", NAVY_BLUE),
        ("💰 ₹0 COST", "Free-Tier Cloud Ready", "Runs 100% on free-tier cloud services with zero maintenance cost.", VIOLET)
    ]

    for (stat, label, desc, color), (x, y) in zip(metrics, coords9):
        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, c_w, c_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_right = tf.margin_top = Inches(0.2)

        p1 = tf.paragraphs[0]
        p1.text = stat
        p1.font.size = Pt(26)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_DARK

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(12)
        p3.font.color.rgb = TEXT_MUTED


    # =========================================================================
    # SLIDE 10: CONCLUSION & FUTURE SCOPE (Modern Dark Theme)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_transition(s10, "fade")

    bg10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg10.fill.solid()
    bg10.fill.fore_color.rgb = DARK_BG
    bg10.line.fill.background()

    top_glow10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.1))
    top_glow10.fill.solid()
    top_glow10.fill.fore_color.rgb = PRIMARY_RED
    top_glow10.line.fill.background()

    c_box = s10.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(6.5), Inches(5.8))
    tf_c10 = c_box.text_frame
    tf_c10.word_wrap = True

    p_c_head = tf_c10.paragraphs[0]
    p_c_head.text = "Conclusion"
    p_c_head.font.size = Pt(24)
    p_c_head.font.bold = True
    p_c_head.font.color.rgb = TEXT_LIGHT

    p_c_body = tf_c10.add_paragraph()
    p_c_body.text = ("• Bridges the gap between Donors & Hospitals in real time.\n"
                     "• Replaces slow phone calls with instant 2-second cloud triage.\n"
                     "• Eliminates blood wastage with smart FIFO dispatch.")
    p_c_body.font.size = Pt(13)
    p_c_body.font.color.rgb = RGBColor(203, 213, 225)

    tf_c10.add_paragraph()

    p_f_head = tf_c10.add_paragraph()
    p_f_head.text = "🚀 Future Roadmap:"
    p_f_head.font.size = Pt(16)
    p_f_head.font.bold = True
    p_f_head.font.color.rgb = RGBColor(252, 165, 165)

    future_pts = [
        "🤖 AI Blood Shortage Forecasting",
        "🛸 Drone Delivery for Rural Emergency Clinics",
        "📱 Native Mobile App (iOS / Android)"
    ]
    for pt in future_pts:
        p_pt = tf_c10.add_paragraph()
        p_pt.text = "•  " + pt
        p_pt.font.size = Pt(13)
        p_pt.font.color.rgb = RGBColor(226, 232, 240)

    # Right: Thank You Card
    ty_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.7), Inches(0.8), Inches(4.8), Inches(5.8))
    ty_card.fill.solid()
    ty_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    ty_card.line.color.rgb = PRIMARY_RED
    ty_card.line.width = Pt(1.5)

    tf_ty = ty_card.text_frame
    tf_ty.word_wrap = True
    tf_ty.margin_left = tf_ty.margin_right = Inches(0.4)
    tf_ty.margin_top = Inches(0.5)

    p_ty = tf_ty.paragraphs[0]
    p_ty.text = "THANK YOU!"
    p_ty.alignment = PP_ALIGN.CENTER
    p_ty.font.size = Pt(30)
    p_ty.font.bold = True
    p_ty.font.color.rgb = TEXT_LIGHT

    p_qa = tf_ty.add_paragraph()
    p_qa.text = "Any Questions or Suggestions?"
    p_qa.alignment = PP_ALIGN.CENTER
    p_qa.font.size = Pt(14)
    p_qa.font.color.rgb = RGBColor(147, 197, 253)

    tf_ty.add_paragraph()

    p_tm_h = tf_ty.add_paragraph()
    p_tm_h.text = "Presented By:"
    p_tm_h.font.size = Pt(11)
    p_tm_h.font.bold = True
    p_tm_h.font.color.rgb = RGBColor(252, 165, 165)

    for name, roll in members:
        p_m = tf_ty.add_paragraph()
        p_m.text = f"• {name} ({roll})"
        p_m.font.size = Pt(12)
        p_m.font.color.rgb = TEXT_LIGHT

    tf_ty.add_paragraph()
    p_g_h = tf_ty.add_paragraph()
    p_g_h.text = "Guide: Mr. Manish Kumar (Trainer)"
    p_g_h.font.size = Pt(11)
    p_g_h.font.bold = True
    p_g_h.font.color.rgb = RGBColor(148, 163, 184)

    p_rvit = tf_ty.add_paragraph()
    p_rvit.text = "RV Institute of Technology, Bijnor (AKTU)"
    p_rvit.font.size = Pt(10)
    p_rvit.font.color.rgb = RGBColor(100, 116, 139)


    # =========================================================================
    # SAVE PRESENTATION
    # =========================================================================
    os.makedirs("presentation", exist_ok=True)
    ws_pptx = "presentation/Cloud_Blood_Bank_Simple_10_Slides.pptx"
    prs.save(ws_pptx)
    print("Saved to workspace:", ws_pptx)

    onedrive_desktop = "C:/Users/rajpu/OneDrive/Desktop"
    local_desktop = "C:/Users/rajpu/Desktop"

    for dt in [onedrive_desktop, local_desktop]:
        if os.path.exists(dt):
            dest1 = os.path.join(dt, "Cloud_Blood_Bank_Simple_10_Slides.pptx")
            try:
                shutil.copyfile(ws_pptx, dest1)
                print(f"Saved: {dest1}")
            except Exception as e:
                print(f"Notice saving {dest1}:", e)

            dest2 = os.path.join(dt, "Cloud_Blood_Bank_Presentation_RVIT.pptx")
            try:
                shutil.copyfile(ws_pptx, dest2)
                print(f"Saved: {dest2}")
            except Exception as e:
                print(f"Notice saving {dest2}:", e)

if __name__ == "__main__":
    create_presentation()
