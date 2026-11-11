import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import shutil

def generate_slide6():
    # 16:9 Widescreen aspect ratio at 200 DPI (3200 x 1800 px)
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    DARK_TEXT  = '#0F172A'
    MUTED_TEXT = '#64748B'
    BORDER_COL = '#E2E8F0'

    # Top Category Pill
    badge = patches.FancyBboxPatch(
        (0.9, 8.12), 2.8, 0.42,
        boxstyle="round,pad=0.08,rounding_size=0.2",
        fc='#EFF6FF', ec='#1D4ED8', lw=1.5
    )
    ax.add_patch(badge)
    ax.text(2.3, 8.33, "TECH ECOSYSTEM", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#1D4ED8', fontfamily='sans-serif')

    # Main Title & Subtitle
    ax.text(0.9, 7.55, "Technology Stack & Developer Tools",
            fontsize=26, fontweight='bold', color=DARK_TEXT, fontfamily='sans-serif')
    ax.text(0.9, 7.08, "Modular, production-ready stack built with modern frameworks and 100% free-tier cloud infrastructure",
            fontsize=13, color=MUTED_TEXT, fontfamily='sans-serif')

    # Bento Box 2x2 Layout Coordinates
    # Row 1 (Top): y = 4.15, height = 2.65
    # Row 2 (Bottom): y = 1.15, height = 2.65
    # Col 1 (Left): x = 0.9, width = 6.85
    # Col 2 (Right): x = 8.25, width = 6.85

    bento_data = [
        # Box 1: Frontend (Top Left)
        {
            "x": 0.9, "y": 4.15, "w": 6.85, "h": 2.7,
            "title": "Frontend Client Interface",
            "subtitle": "Responsive Single Page Application",
            "color": "#1D4ED8", "soft_bg": "#EFF6FF", "tag_bg": "#DBEAFE",
            "icon_type": "frontend",
            "pills": ["React.js 18", "Tailwind CSS", "Axios HTTP", "PWA Mobile"],
            "features": [
                "Responsive UI tailored for desktop laptops, tablets & smartphones.",
                "Live real-time inventory dashboards with color-coded stock alerts.",
                "1-click SOS broadcast trigger & interactive Google Maps routing."
            ]
        },
        # Box 2: Backend (Top Right)
        {
            "x": 8.25, "y": 4.15, "w": 6.85, "h": 2.7,
            "title": "Backend Application Engine",
            "subtitle": "High-Concurrency RESTful Server",
            "color": "#DC2626", "soft_bg": "#FEF2F2", "tag_bg": "#FEE2E2",
            "icon_type": "backend",
            "pills": ["Node.js", "Express API", "JWT Security", "Haversine GPS"],
            "features": [
                "High-speed REST API endpoints processing emergency triage requests.",
                "Mathematical Haversine formula for 5-10 km radius donor matching.",
                "Stateless JWT token authentication with role-based access control."
            ]
        },
        # Box 3: Database & Cloud (Bottom Left)
        {
            "x": 0.9, "y": 1.15, "w": 6.85, "h": 2.7,
            "title": "Cloud Database & Storage",
            "subtitle": "ACID-Compliant Relational Data",
            "color": "#059669", "soft_bg": "#ECFDF5", "tag_bg": "#D1FAE5",
            "icon_type": "database",
            "pills": ["PostgreSQL 16", "Supabase Cloud", "3NF Schema", "Daily Backups"],
            "features": [
                "6 fully normalized relational tables ensuring zero data redundancy.",
                "ACID transaction locking to prevent double-booking of blood units.",
                "Sub-100ms indexing on blood group, expiry dates, and city locations."
            ]
        },
        # Box 4: APIs & DevOps (Bottom Right)
        {
            "x": 8.25, "y": 1.15, "w": 6.85, "h": 2.7,
            "title": "Third-Party APIs & Cloud DevOps",
            "subtitle": "Real-Time Communications & Hosting",
            "color": "#7C3AED", "soft_bg": "#F5F3FF", "tag_bg": "#EDE9FE",
            "icon_type": "api",
            "pills": ["Google Maps", "Twilio SMS", "WhatsApp API", "Render Cloud"],
            "features": [
                "Turn-by-turn navigation link sent directly to responding donors.",
                "Automated high-priority emergency SMS broadcast in under 2 seconds.",
                "Continuous integration via GitHub and scalable free-tier hosting."
            ]
        }
    ]

    for item in bento_data:
        x, y, w, h = item["x"], item["y"], item["w"], item["h"]
        c, s_bg, t_bg = item["color"], item["soft_bg"], item["tag_bg"]

        # Subtle Shadow
        shadow = patches.FancyBboxPatch(
            (x + 0.05, y - 0.05), w, h,
            boxstyle="round,pad=0.06,rounding_size=0.25",
            fc='#E2E8F0', ec='#E2E8F0', lw=1, zorder=1
        )
        ax.add_patch(shadow)

        # Main Bento Card
        card = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.06,rounding_size=0.25",
            fc='#FFFFFF', ec=c, lw=2, zorder=2
        )
        ax.add_patch(card)

        # Header Ribbon
        ribbon = patches.FancyBboxPatch(
            (x + 0.15, y + h - 0.72), w - 0.3, 0.60,
            boxstyle="round,pad=0.04,rounding_size=0.15",
            fc=s_bg, ec=c, lw=1, zorder=3
        )
        ax.add_patch(ribbon)

        # Icon Circle
        icon_circle = patches.Circle((x + 0.45, y + h - 0.42), 0.20, fc=c, ec=c, zorder=4)
        ax.add_patch(icon_circle)

        # Geometric Icon inside circle
        if item["icon_type"] == "frontend":
            # Laptop screen / window icon
            rect = patches.Rectangle((x + 0.35, y + h - 0.50), 0.20, 0.14,
                                     fc='#FFFFFF', ec='#FFFFFF', lw=1, zorder=5)
            ax.add_patch(rect)
            ax.plot([x + 0.32, x + 0.58], [y + h - 0.52, y + h - 0.52], color='#FFFFFF', lw=2, zorder=5)
        elif item["icon_type"] == "backend":
            # Server gear / brackets icon
            ax.plot([x + 0.38, x + 0.35, x + 0.38], [y + h - 0.36, y + h - 0.42, y + h - 0.48],
                    color='#FFFFFF', lw=2.2, zorder=5)
            ax.plot([x + 0.52, x + 0.55, x + 0.52], [y + h - 0.36, y + h - 0.42, y + h - 0.48],
                    color='#FFFFFF', lw=2.2, zorder=5)
            ax.plot([x + 0.48, x + 0.42], [y + h - 0.35, y + h - 0.49],
                    color='#FFFFFF', lw=2, zorder=5)
        elif item["icon_type"] == "database":
            # Database cylinders icon
            ax.plot([x + 0.35, x + 0.55], [y + h - 0.36, y + h - 0.36], color='#FFFFFF', lw=2.2, zorder=5)
            ax.plot([x + 0.35, x + 0.55], [y + h - 0.42, y + h - 0.42], color='#FFFFFF', lw=2.2, zorder=5)
            ax.plot([x + 0.35, x + 0.55], [y + h - 0.48, y + h - 0.48], color='#FFFFFF', lw=2.2, zorder=5)
        else: # API
            # Cloud / Connection icon
            dot1 = patches.Circle((x + 0.40, y + h - 0.42), 0.05, fc='#FFFFFF', ec='#FFFFFF', zorder=5)
            dot2 = patches.Circle((x + 0.50, y + h - 0.42), 0.05, fc='#FFFFFF', ec='#FFFFFF', zorder=5)
            ax.add_patch(dot1)
            ax.add_patch(dot2)
            ax.plot([x + 0.40, x + 0.50], [y + h - 0.42, y + h - 0.42], color='#FFFFFF', lw=2, zorder=5)

        # Card Title & Subtitle
        ax.text(x + 0.75, y + h - 0.34, item["title"],
                ha='left', va='center', fontsize=13.5, fontweight='bold', color=DARK_TEXT, zorder=4)
        ax.text(x + 0.75, y + h - 0.54, item["subtitle"],
                ha='left', va='center', fontsize=10, fontweight='bold', color=c, zorder=4)

        # Horizontal Row of Tech Tag Pills (Uniformly distributed inside card)
        num_pills = len(item["pills"])
        gap_pills = 0.14
        margin_pills = 0.30
        avail_w = w - (2 * margin_pills) - ((num_pills - 1) * gap_pills)
        pill_w = avail_w / num_pills
        pill_y = y + h - 1.08

        for p_idx, pill in enumerate(item["pills"]):
            px = x + margin_pills + p_idx * (pill_w + gap_pills)
            p_box = patches.FancyBboxPatch(
                (px, pill_y), pill_w, 0.32,
                boxstyle="round,pad=0.02,rounding_size=0.1",
                fc=t_bg, ec=c, lw=1, zorder=3
            )
            ax.add_patch(p_box)
            ax.text(px + pill_w/2, pill_y + 0.16, pill,
                    ha='center', va='center', fontsize=9.2, fontweight='bold', color=c, zorder=4)

        # Bullet Features
        bullet_y_start = y + h - 1.48
        spacing = 0.38
        for b_idx, feat in enumerate(item["features"]):
            by = bullet_y_start - b_idx * spacing
            b_dot = patches.Circle((x + 0.4, by), 0.05, fc=c, ec=c, zorder=3)
            ax.add_patch(b_dot)
            ax.text(x + 0.56, by, feat,
                    ha='left', va='center', fontsize=10.5, color=DARK_TEXT,
                    fontfamily='sans-serif', zorder=3)

    # Bottom Footer
    ax.plot([0.9, 15.1], [0.65, 0.65], color=BORDER_COL, lw=1.5)
    ax.text(0.9, 0.35, "RV Institute of Technology, Bijnor  •  B.Tech Computer Science & Engineering (2026-27)",
            fontsize=10, color=MUTED_TEXT, fontfamily='sans-serif')
    ax.text(15.1, 0.35, "Cloud-Based Online Blood Bank & Emergency Triage System",
            ha='right', fontsize=10, fontweight='bold', color=DARK_TEXT, fontfamily='sans-serif')

    out_path = "Slide_6_Technology_Stack_Tools.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print("Slide 6 generated successfully:", out_path)

    # Copy to Desktop
    for dt in ["C:/Users/rajpu/OneDrive/Desktop", "C:/Users/rajpu/Desktop"]:
        if os.path.exists(dt):
            dest = os.path.join(dt, "Slide_6_Technology_Stack_Tools.png")
            shutil.copyfile(out_path, dest)
            print("Copied to Desktop:", dest)

if __name__ == "__main__":
    generate_slide6()
