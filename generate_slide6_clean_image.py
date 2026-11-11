import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import shutil

def generate_slide6_clean():
    # 16:9 Widescreen aspect ratio at 200 DPI (3200 x 1800 px)
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    DARK_TEXT  = '#0F172A'
    MUTED_TEXT = '#64748B'

    # Top Category Pill
    badge = patches.FancyBboxPatch(
        (0.9, 8.12), 2.5, 0.42,
        boxstyle="round,pad=0.08,rounding_size=0.2",
        fc='#EFF6FF', ec='#1D4ED8', lw=1.5
    )
    ax.add_patch(badge)
    ax.text(2.15, 8.33, "TECH STACK", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#1D4ED8', fontfamily='sans-serif')

    # Main Title & Subtitle
    ax.text(0.9, 7.55, "Technologies & Tools Used",
            fontsize=28, fontweight='bold', color=DARK_TEXT, fontfamily='sans-serif')
    ax.text(0.9, 7.10, "Core developer frameworks and cloud services powering the platform",
            fontsize=13, color=MUTED_TEXT, fontfamily='sans-serif')

    # Subtle divider
    ax.plot([0.9, 15.1], [6.75, 6.75], color='#E2E8F0', lw=1.5)

    # 4 Open Vertical Columns (NO BOXES! Pure floating pills and clean typography)
    columns = [
        {
            "num": "01",
            "category": "FRONTEND",
            "subtitle": "Client Web App",
            "color": "#1D4ED8",
            "soft_bg": "#EFF6FF",
            "icon_type": "frontend",
            "tools": [
                ("React.js 18", "Single Page UI Framework", "#1D4ED8", "#DBEAFE"),
                ("Tailwind CSS", "Utility-First Responsive Styling", "#0284C7", "#E0F2FE"),
                ("Axios Client", "Asynchronous HTTP Requests", "#4338CA", "#EEF2FF"),
                ("PWA Mobile", "Installable Web App Experience", "#2563EB", "#DBEAFE")
            ]
        },
        {
            "num": "02",
            "category": "BACKEND",
            "subtitle": "Server & API Engine",
            "color": "#DC2626",
            "soft_bg": "#FEF2F2",
            "icon_type": "backend",
            "tools": [
                ("Node.js v20", "High-Concurrency JavaScript Engine", "#DC2626", "#FEE2E2"),
                ("Express.js", "RESTful API Routing Framework", "#B91C1C", "#FEE2E2"),
                ("JWT Security", "Stateless Token Authentication", "#E11D48", "#FFE4E6"),
                ("Haversine GPS", "5-10 KM Donor Radius Algorithm", "#C026D3", "#FAE8FF")
            ]
        },
        {
            "num": "03",
            "category": "DATABASE",
            "role": "Cloud Storage",
            "color": "#059669",
            "soft_bg": "#ECFDF5",
            "icon_type": "database",
            "tools": [
                ("PostgreSQL 16", "ACID Relational SQL Database", "#059669", "#D1FAE5"),
                ("Supabase Cloud", "Managed Real-Time PostgreSQL", "#047857", "#D1FAE5"),
                ("3NF Schema", "Zero Data Redundancy Design", "#0D9488", "#CCFBF1"),
                ("Indexed Queries", "Sub-100ms Search Speed", "#16A34A", "#DCFCE7")
            ]
        },
        {
            "num": "04",
            "category": "APIs & CLOUD",
            "role": "Third-Party Services",
            "color": "#7C3AED",
            "soft_bg": "#F5F3FF",
            "icon_type": "api",
            "tools": [
                ("Google Maps API", "Turn-by-Turn Donor Routing", "#7C3AED", "#EDE9FE"),
                ("Twilio SMS", "Instant Emergency SOS Alerts", "#6D28D9", "#EDE9FE"),
                ("WhatsApp API", "Direct Donor Notification Links", "#25D366", "#DCFCE7"),
                ("Render Hosting", "Free-Tier Cloud Server Deployment", "#4F46E5", "#EEF2FF")
            ]
        }
    ]

    col_w = 3.3
    gap = 0.35
    start_x = 0.9

    for i, col in enumerate(columns):
        cx = start_x + i * (col_w + gap)
        c = col["color"]

        # Category Header (Open, no box border!)
        # Small colored pill badge on top
        cat_badge = patches.FancyBboxPatch(
            (cx, 6.10), 1.8, 0.38,
            boxstyle="round,pad=0.03,rounding_size=0.15",
            fc=col["soft_bg"], ec=c, lw=1.2
        )
        ax.add_patch(cat_badge)
        ax.text(cx + 0.9, 6.29, f"{col['num']}  {col['category']}",
                ha='center', va='center', fontsize=11, fontweight='bold', color=c)

        # Floating Stack of 4 Tech Tools
        tool_start_y = 5.25
        tool_h = 0.85
        spacing = 1.02

        for t_idx, (t_name, t_desc, t_col, t_bg) in enumerate(col["tools"]):
            ty = tool_start_y - t_idx * spacing

            # Floating Tool Pill (Soft Background, NO enclosing box on the column!)
            pill = patches.FancyBboxPatch(
                (cx, ty), col_w, tool_h,
                boxstyle="round,pad=0.05,rounding_size=0.2",
                fc='#FFFFFF', ec=t_bg, lw=1.5, zorder=2
            )
            ax.add_patch(pill)

            # Left colored accent line inside tool pill
            ax.plot([cx + 0.12, cx + 0.12], [ty + 0.15, ty + tool_h - 0.15],
                    color=t_col, lw=3.5, solid_capstyle='round', zorder=3)

            # Tool Name (Bold & Crisp)
            ax.text(cx + 0.30, ty + tool_h - 0.28, t_name,
                    fontsize=13, fontweight='bold', color=DARK_TEXT, fontfamily='sans-serif', zorder=3)

            # Tool 1-Line Role (Short, Minimal Theory)
            ax.text(cx + 0.30, ty + 0.22, t_desc,
                    fontsize=9.5, color=MUTED_TEXT, fontfamily='sans-serif', zorder=3)

    # Bottom Single-Line Highlight Ribbon
    ribbon = patches.FancyBboxPatch(
        (0.9, 1.05), 14.2, 0.48,
        boxstyle="round,pad=0.04,rounding_size=0.2",
        fc='#EFF6FF', ec='#1D4ED8', lw=1.2
    )
    ax.add_patch(ribbon)
    ax.text(8.0, 1.29, "⚡ 100% Free-Tier Architecture  •  Sub-100ms Query Execution  •  Zero Cloud Maintenance Cost",
            ha='center', va='center', fontsize=12, fontweight='bold', color='#1D4ED8', fontfamily='sans-serif')

    # Bottom Footer Divider & Text
    ax.plot([0.9, 15.1], [0.65, 0.65], color='#E2E8F0', lw=1.2)
    ax.text(0.9, 0.35, "RV Institute of Technology, Bijnor  •  B.Tech Computer Science & Engineering (2026-27)",
            fontsize=10, color=MUTED_TEXT, fontfamily='sans-serif')
    ax.text(15.1, 0.35, "Cloud-Based Online Blood Bank & Emergency Triage System",
            ha='right', fontsize=10, fontweight='bold', color=DARK_TEXT, fontfamily='sans-serif')

    out_path = "Slide_6_Technology_Stack_Tools.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print("Slide 6 Clean generated successfully:", out_path)

    # Copy to Desktop
    for dt in ["C:/Users/rajpu/OneDrive/Desktop", "C:/Users/rajpu/Desktop"]:
        if os.path.exists(dt):
            dest = os.path.join(dt, "Slide_6_Technology_Stack_Tools.png")
            shutil.copyfile(out_path, dest)
            print("Copied to Desktop:", dest)

if __name__ == "__main__":
    generate_slide6_clean()
