import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import shutil

def generate_slide5():
    # 16:9 Widescreen aspect ratio at 200 DPI (3200 x 1800 px)
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Color definitions
    DARK_TEXT  = '#0F172A'
    MUTED_TEXT = '#64748B'
    BORDER_COL = '#E2E8F0'

    # Top Category Pill
    badge = patches.FancyBboxPatch(
        (0.9, 8.1), 2.5, 0.42,
        boxstyle="round,pad=0.08,rounding_size=0.2",
        fc='#FEF2F2', ec='#DC2626', lw=1.5
    )
    ax.add_patch(badge)
    ax.text(2.15, 8.31, "SYSTEM MODULES", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#DC2626', fontfamily='sans-serif')

    # Main Title & Subtitle
    ax.text(0.9, 7.55, "Core User Roles & System Modules",
            fontsize=26, fontweight='bold', color=DARK_TEXT, fontfamily='sans-serif')
    ax.text(0.9, 7.05, "Dedicated role-based dashboards engineered for fast coordination, zero wastage, and high security",
            fontsize=13, color=MUTED_TEXT, fontfamily='sans-serif')

    # 4 Modules Data
    modules = [
        {
            "num": "01",
            "title": "Donor Portal",
            "role": "Citizens & Volunteers",
            "theme_col": "#DC2626",
            "soft_col": "#FEF2F2",
            "badge_col": "#FEE2E2",
            "icon_type": "blood",
            "bullets": [
                "Profile & Blood Group Registration",
                "Instant Emergency SOS Alerts",
                "Donation History & 90-Day Tracker",
                "1-Click Donation Acceptance",
                "Google Maps Route to Hospital"
            ],
            "tag": "Active Life-Saver"
        },
        {
            "num": "02",
            "title": "Hospital Portal",
            "role": "Doctors & ICU Staff",
            "theme_col": "#1D4ED8",
            "soft_col": "#EFF6FF",
            "badge_col": "#DBEAFE",
            "icon_type": "cross",
            "bullets": [
                "Post Urgent Blood Requisitions",
                "Filter Urgency (Critical / Normal)",
                "Live City-Wide Stock Availability",
                "Track Blood Delivery in Real Time",
                "Secure Digital Handover Receipt"
            ],
            "tag": "Emergency Triage"
        },
        {
            "num": "03",
            "title": "Blood Bank",
            "role": "Certified Storage Centers",
            "theme_col": "#059669",
            "soft_col": "#ECFDF5",
            "badge_col": "#D1FAE5",
            "icon_type": "bank",
            "bullets": [
                "Manage Live Blood Inventory",
                "Automated Expiration Date Alerts",
                "Smart FIFO Unit Dispatch Rule",
                "Maintain Emergency Buffer Stock",
                "Donor Verification & Logging"
            ],
            "tag": "90% Less Wastage"
        },
        {
            "num": "04",
            "title": "Super Admin",
            "role": "Healthcare Governance",
            "theme_col": "#7C3AED",
            "soft_col": "#F5F3FF",
            "badge_col": "#EDE9FE",
            "icon_type": "shield",
            "bullets": [
                "Hospital & Bank License Approval",
                "Anti-Fraud Requisition Auditing",
                "City-Wide Blood Analytics & Reports",
                "User Access & Role Permissions",
                "Tamper-Proof System Audit Logs"
            ],
            "tag": "100% Compliance"
        }
    ]

    card_w = 3.3
    gap = 0.35
    start_x = 0.9
    card_h = 5.5
    start_y = 1.15

    for i, mod in enumerate(modules):
        cx = start_x + i * (card_w + gap)

        # Card Shadow (subtle offset rectangle)
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
            fc='#FFFFFF', ec=mod["theme_col"], lw=2, zorder=2
        )
        ax.add_patch(card)

        # Top Header Box inside Card
        header_box = patches.FancyBboxPatch(
            (cx + 0.1, start_y + card_h - 1.25), card_w - 0.2, 1.15,
            boxstyle="round,pad=0.04,rounding_size=0.18",
            fc=mod["soft_col"], ec=mod["theme_col"], lw=1.2, zorder=3
        )
        ax.add_patch(header_box)

        # Icon Circle Badge
        icon_bg = patches.Circle((cx + 0.42, start_y + card_h - 0.55), 0.22,
                                 fc=mod["theme_col"], ec=mod["theme_col"], zorder=4)
        ax.add_patch(icon_bg)

        # Draw clean vector icons inside circle
        if mod["icon_type"] == "cross":
            # Medical Cross
            ax.plot([cx + 0.33, cx + 0.51], [start_y + card_h - 0.55, start_y + card_h - 0.55],
                    color='#FFFFFF', lw=3, zorder=5)
            ax.plot([cx + 0.42, cx + 0.42], [start_y + card_h - 0.64, start_y + card_h - 0.46],
                    color='#FFFFFF', lw=3, zorder=5)
        elif mod["icon_type"] == "blood":
            # Blood drop circle dot
            inner_dot = patches.Circle((cx + 0.42, start_y + card_h - 0.55), 0.11,
                                       fc='#FFFFFF', ec='#FFFFFF', zorder=5)
            ax.add_patch(inner_dot)
        elif mod["icon_type"] == "bank":
            # Storage lines
            ax.plot([cx + 0.33, cx + 0.51], [start_y + card_h - 0.49, start_y + card_h - 0.49],
                    color='#FFFFFF', lw=2.2, zorder=5)
            ax.plot([cx + 0.33, cx + 0.51], [start_y + card_h - 0.55, start_y + card_h - 0.55],
                    color='#FFFFFF', lw=2.2, zorder=5)
            ax.plot([cx + 0.33, cx + 0.51], [start_y + card_h - 0.61, start_y + card_h - 0.61],
                    color='#FFFFFF', lw=2.2, zorder=5)
        else: # shield / admin
            inner_dot = patches.RegularPolygon((cx + 0.42, start_y + card_h - 0.55), 3, radius=0.12,
                                               fc='#FFFFFF', ec='#FFFFFF', zorder=5)
            ax.add_patch(inner_dot)

        # Module Number Badge (Top Right of Header)
        num_badge = patches.FancyBboxPatch(
            (cx + card_w - 0.62, start_y + card_h - 0.52), 0.42, 0.32,
            boxstyle="round,pad=0.02,rounding_size=0.1",
            fc=mod["theme_col"], ec=mod["theme_col"], lw=1, zorder=4
        )
        ax.add_patch(num_badge)
        ax.text(cx + card_w - 0.41, start_y + card_h - 0.36, mod["num"],
                ha='center', va='center', fontsize=10.5, fontweight='bold', color='#FFFFFF', zorder=5)

        # Card Title & Role
        ax.text(cx + 0.75, start_y + card_h - 0.45, mod['title'],
                ha='left', va='center', fontsize=14, fontweight='bold', color=DARK_TEXT, zorder=4)
        ax.text(cx + 0.75, start_y + card_h - 0.82, mod["role"],
                ha='left', va='center', fontsize=10.5, fontweight='bold', color=mod["theme_col"], zorder=4)

        # Bullets
        bullet_start_y = start_y + card_h - 1.6
        spacing = 0.62
        for b_idx, bullet in enumerate(mod["bullets"]):
            by = bullet_start_y - b_idx * spacing
            b_dot = patches.Circle((cx + 0.3, by), 0.065, fc=mod["theme_col"], ec=mod["theme_col"], zorder=3)
            ax.add_patch(b_dot)
            ax.text(cx + 0.48, by, bullet,
                    ha='left', va='center', fontsize=10.5, color=DARK_TEXT,
                    fontfamily='sans-serif', zorder=3)

        # Bottom Feature Tag Pill
        tag_box = patches.FancyBboxPatch(
            (cx + 0.2, start_y + 0.25), card_w - 0.4, 0.45,
            boxstyle="round,pad=0.03,rounding_size=0.15",
            fc=mod["badge_col"], ec=mod["theme_col"], lw=1, zorder=3
        )
        ax.add_patch(tag_box)
        ax.text(cx + card_w/2, start_y + 0.475, mod["tag"],
                ha='center', va='center', fontsize=11, fontweight='bold', color=mod["theme_col"], zorder=4)

    # Bottom Footer Divider & Text
    ax.plot([0.9, 15.1], [0.65, 0.65], color=BORDER_COL, lw=1.5)
    ax.text(0.9, 0.35, "RV Institute of Technology, Bijnor  •  B.Tech Computer Science & Engineering (2026-27)",
            fontsize=10, color=MUTED_TEXT, fontfamily='sans-serif')
    ax.text(15.1, 0.35, "Cloud-Based Online Blood Bank & Emergency Triage System",
            ha='right', fontsize=10, fontweight='bold', color=DARK_TEXT, fontfamily='sans-serif')

    out_path = "Slide_5_Core_User_Modules.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print("Slide 5 generated successfully:", out_path)

    # Copy to Desktop
    for dt in ["C:/Users/rajpu/OneDrive/Desktop", "C:/Users/rajpu/Desktop"]:
        if os.path.exists(dt):
            dest = os.path.join(dt, "Slide_5_Core_User_Modules.png")
            shutil.copyfile(out_path, dest)
            print("Copied to Desktop:", dest)

if __name__ == "__main__":
    generate_slide5()
