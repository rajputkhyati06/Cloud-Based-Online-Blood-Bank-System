import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import shutil

def generate_slide8():
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
        (0.9, 8.1), 2.7, 0.42,
        boxstyle="round,pad=0.08,rounding_size=0.2",
        fc='#FEF2F2', ec='#DC2626', lw=1.5
    )
    ax.add_patch(badge)
    ax.text(2.25, 8.31, "CORE ALGORITHM", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#DC2626', fontfamily='sans-serif')

    # Main Title & Subtitle
    ax.text(0.9, 7.55, "Smart FIFO Blood Dispatch Logic",
            fontsize=26, fontweight='bold', color=DARK_TEXT, fontfamily='sans-serif')
    ax.text(0.9, 7.05, "Automated First-In, First-Out triage workflow designed to eliminate expiration wastage and ensure rapid emergency supply",
            fontsize=13, color=MUTED_TEXT, fontfamily='sans-serif')

    # 4 Steps of the Algorithm
    steps = [
        {
            "num": "01",
            "title": "Query & Triage",
            "subtitle": "Emergency Request",
            "theme_col": "#1D4ED8",
            "soft_col": "#EFF6FF",
            "badge_col": "#DBEAFE",
            "icon_type": "search",
            "bullets": [
                "Doctor inputs required blood group",
                "Flags triage level (Critical / Normal)",
                "System queries cloud blood stock",
                "Checks ABO & Rh compatibility",
                "Validates doctor & hospital license"
            ],
            "tag": "Instant Query Validation"
        },
        {
            "num": "02",
            "title": "Smart FIFO Rule",
            "subtitle": "When Stock Available",
            "theme_col": "#059669",
            "soft_col": "#ECFDF5",
            "badge_col": "#D1FAE5",
            "icon_type": "check",
            "bullets": [
                "Scans expiration dates of safe units",
                "Selects OLDEST safe packet first",
                "Prevents blood expiring on shelves",
                "Reserves unit digitally in 100ms",
                "Decrements live inventory counter"
            ],
            "tag": "90% Wastage Eliminated"
        },
        {
            "num": "03",
            "title": "SOS Fallback",
            "subtitle": "When Out of Stock",
            "theme_col": "#DC2626",
            "soft_col": "#FEF2F2",
            "badge_col": "#FEE2E2",
            "icon_type": "alert",
            "bullets": [
                "Triggers automatically if stock is 0",
                "GPS scans eligible donors in 5-10 km",
                "Broadcasts priority SMS & WhatsApp alerts",
                "Donors accept with single tap",
                "Provides Google Maps hospital route"
            ],
            "tag": "Broadcast in < 2 Seconds"
        },
        {
            "num": "04",
            "title": "Safe Handover",
            "subtitle": "Dispatch & Audit",
            "theme_col": "#7C3AED",
            "soft_col": "#F5F3FF",
            "badge_col": "#EDE9FE",
            "icon_type": "handover",
            "bullets": [
                "Delivery tracked with live ETA",
                "Digital OTP validation at hospital",
                "Doctor confirms safe unit receipt",
                "Logs timestamp in audit ledger",
                "Notifies donor with appreciation badge"
            ],
            "tag": "100% Traceability"
        }
    ]

    card_w = 3.3
    gap = 0.35
    start_x = 0.9
    card_h = 5.5
    start_y = 1.15

    for i, st in enumerate(steps):
        cx = start_x + i * (card_w + gap)

        # Card Shadow
        shadow = patches.FancyBboxPatch(
            (cx + 0.04, start_y - 0.04), card_w, card_h,
            boxstyle="round,pad=0.05,rounding_size=0.25",
            fc='#E2E8F0', ec='#E2E8F0', lw=1, zorder=1
        )
        ax.add_patch(shadow)

        # Main Card Body
        card = patches.FancyBboxPatch(
            (cx, start_y), card_w, card_h,
            boxstyle="round,pad=0.05,rounding_size=0.25",
            fc='#FFFFFF', ec=st["theme_col"], lw=2, zorder=2
        )
        ax.add_patch(card)

        # Top Header Box
        header_box = patches.FancyBboxPatch(
            (cx + 0.1, start_y + card_h - 1.25), card_w - 0.2, 1.15,
            boxstyle="round,pad=0.04,rounding_size=0.18",
            fc=st["soft_col"], ec=st["theme_col"], lw=1.2, zorder=3
        )
        ax.add_patch(header_box)

        # Icon Circle Badge
        icon_bg = patches.Circle((cx + 0.42, start_y + card_h - 0.55), 0.22,
                                 fc=st["theme_col"], ec=st["theme_col"], zorder=4)
        ax.add_patch(icon_bg)

        # Vector Icon Geometry
        if st["icon_type"] == "search":
            # Magnifying Glass / Query Icon
            c_glass = patches.Circle((cx + 0.40, start_y + card_h - 0.53), 0.09,
                                     fc='none', ec='#FFFFFF', lw=2.2, zorder=5)
            ax.add_patch(c_glass)
            ax.plot([cx + 0.47, cx + 0.53], [start_y + card_h - 0.60, start_y + card_h - 0.66],
                    color='#FFFFFF', lw=2.5, zorder=5)
        elif st["icon_type"] == "check":
            # Checkmark Icon
            ax.plot([cx + 0.32, cx + 0.40, cx + 0.53],
                    [start_y + card_h - 0.56, start_y + card_h - 0.64, start_y + card_h - 0.46],
                    color='#FFFFFF', lw=3, zorder=5)
        elif st["icon_type"] == "alert":
            # Exclamation / Alert Icon
            ax.plot([cx + 0.42, cx + 0.42], [start_y + card_h - 0.46, start_y + card_h - 0.57],
                    color='#FFFFFF', lw=3, zorder=5)
            dot = patches.Circle((cx + 0.42, start_y + card_h - 0.64), 0.03,
                                 fc='#FFFFFF', ec='#FFFFFF', zorder=5)
            ax.add_patch(dot)
        else: # handover
            # Shield / Lock Icon
            poly = patches.RegularPolygon((cx + 0.42, start_y + card_h - 0.55), 3, radius=0.12,
                                          fc='#FFFFFF', ec='#FFFFFF', zorder=5)
            ax.add_patch(poly)

        # Number Badge (Top Right)
        num_badge = patches.FancyBboxPatch(
            (cx + card_w - 0.62, start_y + card_h - 0.52), 0.42, 0.32,
            boxstyle="round,pad=0.02,rounding_size=0.1",
            fc=st["theme_col"], ec=st["theme_col"], lw=1, zorder=4
        )
        ax.add_patch(num_badge)
        ax.text(cx + card_w - 0.41, start_y + card_h - 0.36, st["num"],
                ha='center', va='center', fontsize=10.5, fontweight='bold', color='#FFFFFF', zorder=5)

        # Card Title & Subtitle
        ax.text(cx + 0.75, start_y + card_h - 0.45, st['title'],
                ha='left', va='center', fontsize=14, fontweight='bold', color=DARK_TEXT, zorder=4)
        ax.text(cx + 0.75, start_y + card_h - 0.82, st["subtitle"],
                ha='left', va='center', fontsize=10.5, fontweight='bold', color=st["theme_col"], zorder=4)

        # Bullets
        bullet_start_y = start_y + card_h - 1.6
        spacing = 0.62
        for b_idx, bullet in enumerate(st["bullets"]):
            by = bullet_start_y - b_idx * spacing
            b_dot = patches.Circle((cx + 0.3, by), 0.065, fc=st["theme_col"], ec=st["theme_col"], zorder=3)
            ax.add_patch(b_dot)
            ax.text(cx + 0.48, by, bullet,
                    ha='left', va='center', fontsize=10.5, color=DARK_TEXT,
                    fontfamily='sans-serif', zorder=3)

        # Bottom Feature Tag Pill
        tag_box = patches.FancyBboxPatch(
            (cx + 0.2, start_y + 0.25), card_w - 0.4, 0.45,
            boxstyle="round,pad=0.03,rounding_size=0.15",
            fc=st["badge_col"], ec=st["theme_col"], lw=1, zorder=3
        )
        ax.add_patch(tag_box)
        ax.text(cx + card_w/2, start_y + 0.475, st["tag"],
                ha='center', va='center', fontsize=11, fontweight='bold', color=st["theme_col"], zorder=4)

    # Bottom Footer
    ax.plot([0.9, 15.1], [0.65, 0.65], color=BORDER_COL, lw=1.5)
    ax.text(0.9, 0.35, "RV Institute of Technology, Bijnor  •  B.Tech Computer Science & Engineering (2026-27)",
            fontsize=10, color=MUTED_TEXT, fontfamily='sans-serif')
    ax.text(15.1, 0.35, "Cloud-Based Online Blood Bank & Emergency Triage System",
            ha='right', fontsize=10, fontweight='bold', color=DARK_TEXT, fontfamily='sans-serif')

    out_path = "Slide_8_Smart_FIFO_Dispatch_Logic.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print("Slide 8 generated successfully:", out_path)

    # Copy to Desktops
    for dt in ["C:/Users/rajpu/OneDrive/Desktop", "C:/Users/rajpu/Desktop"]:
        if os.path.exists(dt):
            dest = os.path.join(dt, "Slide_8_Smart_FIFO_Dispatch_Logic.png")
            shutil.copyfile(out_path, dest)
            print("Copied to Desktop:", dest)

if __name__ == "__main__":
    generate_slide8()
