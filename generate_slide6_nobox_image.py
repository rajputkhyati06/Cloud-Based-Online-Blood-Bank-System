import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import shutil

def generate_slide6_nobox():
    # 16:9 Widescreen aspect ratio at 200 DPI (3200 x 1800 px)
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    DARK_TEXT  = '#0F172A'
    MUTED_TEXT = '#64748B'
    BORDER_COL = '#F1F5F9'

    # Top Category Pill
    badge = patches.FancyBboxPatch(
        (0.9, 8.12), 2.5, 0.42,
        boxstyle="round,pad=0.08,rounding_size=0.2",
        fc='#EFF6FF', ec='#1D4ED8', lw=1.5
    )
    ax.add_patch(badge)
    ax.text(2.15, 8.33, "TECH STACK", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#1D4ED8', fontfamily='sans-serif')

    # Main Title & Subtitle (Open, Clean)
    ax.text(0.9, 7.55, "Technologies & Tools Used",
            fontsize=28, fontweight='bold', color=DARK_TEXT, fontfamily='sans-serif')
    ax.text(0.9, 7.10, "Built with modern, open-source frameworks and production-ready free cloud services",
            fontsize=13, color=MUTED_TEXT, fontfamily='sans-serif')

    # Subtle horizontal divider below header
    ax.plot([0.9, 15.1], [6.75, 6.75], color='#E2E8F0', lw=1.2)

    # 4 Open Horizontal Tiers (NO BOXES, NO ENCLOSING BORDERS!)
    # Each tier has:
    # 1. Left Section: Category Name + Color Indicator Bar
    # 2. Middle Section: Floating Colorful Tech Badges (Pills)
    # 3. Right Section: 3 Quick Keywords (Zero Heavy Theory!)

    tiers = [
        {
            "y": 5.45,
            "category": "FRONTEND",
            "role": "Client User Interface",
            "color": "#1D4ED8",
            "soft_bg": "#EFF6FF",
            "pills": [
                ("React.js 18", "#1D4ED8", "#DBEAFE"),
                ("Tailwind CSS", "#0284C7", "#E0F2FE"),
                ("Axios HTTP", "#4338CA", "#EEF2FF"),
                ("PWA Mobile", "#2563EB", "#DBEAFE")
            ],
            "keywords": ["• Responsive UI on all devices", "• Real-Time stock dashboards", "• 1-Click SOS emergency buttons"]
        },
        {
            "y": 4.05,
            "category": "BACKEND",
            "role": "Server & API Engine",
            "color": "#DC2626",
            "soft_bg": "#FEF2F2",
            "pills": [
                ("Node.js", "#DC2626", "#FEE2E2"),
                ("Express API", "#B91C1C", "#FEE2E2"),
                ("JWT Security", "#E11D48", "#FFE4E6"),
                ("Haversine GPS", "#C026D3", "#FAE8FF")
            ],
            "keywords": ["• High-Speed RESTful endpoints", "• 5-10 KM GPS radius matching", "• Secure role-based tokens"]
        },
        {
            "y": 2.65,
            "category": "DATABASE",
            "role": "Cloud Relational Storage",
            "color": "#059669",
            "soft_bg": "#ECFDF5",
            "pills": [
                ("PostgreSQL 16", "#059669", "#D1FAE5"),
                ("Supabase Cloud", "#047857", "#D1FAE5"),
                ("3NF Normalization", "#0D9488", "#CCFBF1"),
                ("Daily Backups", "#16A34A", "#DCFCE7")
            ],
            "keywords": ["• 6 Normalized relational tables", "• ACID concurrency locking", "• Sub-100ms emergency queries"]
        },
        {
            "y": 1.25,
            "category": "APIs & CLOUD",
            "role": "Third-Party Services",
            "color": "#7C3AED",
            "soft_bg": "#F5F3FF",
            "pills": [
                ("Google Maps API", "#7C3AED", "#EDE9FE"),
                ("Twilio SMS", "#6D28D9", "#EDE9FE"),
                ("WhatsApp API", "#25D366", "#DCFCE7"),
                ("Render Hosting", "#4F46E5", "#EEF2FF")
            ],
            "keywords": ["• Turn-by-turn hospital route", "• < 2s Priority SMS alerts", "• 100% Free-tier deployment"]
        }
    ]

    for tier in tiers:
        y = tier["y"]
        c = tier["color"]

        # Left Vertical Color Accent Strip
        ax.plot([0.9, 0.9], [y - 0.35, y + 0.35], color=c, lw=5, solid_capstyle='round')

        # Left Column: Category & Subtitle (No box!)
        ax.text(1.15, y + 0.12, tier["category"],
                fontsize=15, fontweight='bold', color=c, fontfamily='sans-serif')
        ax.text(1.15, y - 0.16, tier["role"],
                fontsize=11, color=MUTED_TEXT, fontfamily='sans-serif')

        # Middle Column: Floating Colorful Badges (Pills)
        pill_x = 4.2
        for p_text, p_col, p_bg in tier["pills"]:
            p_len = len(p_text) * 0.12 + 0.40
            p_box = patches.FancyBboxPatch(
                (pill_x, y - 0.22), p_len, 0.44,
                boxstyle="round,pad=0.03,rounding_size=0.18",
                fc=p_bg, ec=p_col, lw=1.4, zorder=2
            )
            ax.add_patch(p_box)
            ax.text(pill_x + p_len/2, y, p_text,
                    ha='center', va='center', fontsize=11, fontweight='bold', color=p_col, zorder=3)
            pill_x += p_len + 0.22

        # Right Column: 3 Short Clean Keywords (Zero Heavy Theory!)
        kw_x = 10.6
        ax.text(kw_x, y + 0.18, tier["keywords"][0],
                fontsize=11.5, color=DARK_TEXT, fontfamily='sans-serif')
        ax.text(kw_x, y - 0.04, tier["keywords"][1],
                fontsize=11.5, color=DARK_TEXT, fontfamily='sans-serif')
        ax.text(kw_x, y - 0.26, tier["keywords"][2],
                fontsize=11.5, color=DARK_TEXT, fontfamily='sans-serif')

        # Subtle separator line between tiers
        if tier["category"] != "APIs & CLOUD":
            ax.plot([0.9, 15.1], [y - 0.52, y - 0.52], color='#F1F5F9', lw=1.5)

    # Bottom Footer Divider & Text
    ax.plot([0.9, 15.1], [0.65, 0.65], color='#E2E8F0', lw=1.2)
    ax.text(0.9, 0.35, "RV Institute of Technology, Bijnor  •  B.Tech Computer Science & Engineering (2026-27)",
            fontsize=10, color=MUTED_TEXT, fontfamily='sans-serif')
    ax.text(15.1, 0.35, "Cloud-Based Online Blood Bank & Emergency Triage System",
            ha='right', fontsize=10, fontweight='bold', color=DARK_TEXT, fontfamily='sans-serif')

    out_path = "Slide_6_Technology_Stack_Tools.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print("Slide 6 (No-Box) generated successfully:", out_path)

    # Copy to Desktops
    for dt in ["C:/Users/rajpu/OneDrive/Desktop", "C:/Users/rajpu/Desktop"]:
        if os.path.exists(dt):
            dest = os.path.join(dt, "Slide_6_Technology_Stack_Tools.png")
            shutil.copyfile(out_path, dest)
            print("Copied to Desktop:", dest)

if __name__ == "__main__":
    generate_slide6_nobox()
