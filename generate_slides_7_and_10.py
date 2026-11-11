import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import shutil

def generate_slide7():
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
        (0.9, 8.12), 2.8, 0.42,
        boxstyle="round,pad=0.08,rounding_size=0.2",
        fc='#EFF6FF', ec='#1D4ED8', lw=1.5
    )
    ax.add_patch(badge)
    ax.text(2.3, 8.33, "OPERATIONAL FLOW", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#1D4ED8', fontfamily='sans-serif')

    # Main Title & Subtitle
    ax.text(0.9, 7.55, "System Operational Workflow",
            fontsize=28, fontweight='bold', color=DARK_TEXT, fontfamily='sans-serif')
    ax.text(0.9, 7.10, "End-to-end automated emergency pipeline connecting doctors, inventory, and donors in real time",
            fontsize=13, color=MUTED_TEXT, fontfamily='sans-serif')

    # Subtle divider
    ax.plot([0.9, 15.1], [6.75, 6.75], color='#E2E8F0', lw=1.5)

    # 4 Sequential Milestones along a Connected Horizontal Pipeline
    steps = [
        {
            "num": "01",
            "title": "Emergency Request",
            "tag": "Hospital Doctor",
            "color": "#1D4ED8",
            "soft_bg": "#EFF6FF",
            "points": [
                "Doctor logs in via secure portal",
                "Submits required blood group & units",
                "Sets urgency level (Critical / Normal)",
                "System initiates immediate cloud triage"
            ]
        },
        {
            "num": "02",
            "title": "Cloud Stock Query",
            "tag": "FIFO Algorithm",
            "color": "#059669",
            "soft_bg": "#ECFDF5",
            "points": [
                "Scans city-wide blood bank inventory",
                "Applies FIFO: Oldest safe unit selected",
                "If available: Digitally reserves unit (<100ms)",
                "If empty: Triggers Emergency SOS fallback"
            ]
        },
        {
            "num": "03",
            "title": "GPS SOS Broadcast",
            "tag": "Emergency Triage",
            "color": "#DC2626",
            "soft_bg": "#FEF2F2",
            "points": [
                "Scans active donors within 5-10 km radius",
                "Blasts instant SMS & WhatsApp triage alerts",
                "Donors accept via 1-click response link",
                "Provides live Google Maps route to hospital"
            ]
        },
        {
            "num": "04",
            "title": "Safe Delivery & Audit",
            "tag": "Complete Cycle",
            "color": "#7C3AED",
            "soft_bg": "#F5F3FF",
            "points": [
                "Real-time delivery tracking with ETA",
                "Doctor verifies handover via digital OTP",
                "Blood bank inventory auto-decremented",
                "Complete transaction logged in audit ledger"
            ]
        }
    ]

    card_w = 3.3
    gap = 0.35
    start_x = 0.9

    # Draw horizontal connecting track between all 4 milestones
    ax.plot([2.55, 13.45], [5.9, 5.9], color='#CBD5E1', lw=4, zorder=1)

    for i, st in enumerate(steps):
        cx = start_x + i * (card_w + gap)
        center_x = cx + card_w / 2
        c = st["color"]

        # Milestone Node Circle on the pipeline track
        node_circle = patches.Circle((center_x, 5.9), 0.38, fc='#FFFFFF', ec=c, lw=3, zorder=3)
        ax.add_patch(node_circle)
        node_inner = patches.Circle((center_x, 5.9), 0.28, fc=c, ec=c, zorder=4)
        ax.add_patch(node_inner)
        ax.text(center_x, 5.9, st["num"], ha='center', va='center',
                fontsize=13, fontweight='bold', color='#FFFFFF', zorder=5)

        # Directional Arrow indicator between nodes
        if i < 3:
            arrow_x = center_x + card_w / 2 + gap / 2
            ax.annotate("", xy=(arrow_x + 0.15, 5.9), xytext=(arrow_x - 0.15, 5.9),
                        arrowprops=dict(arrowstyle="-|>", color='#64748B', lw=2.5, mutation_scale=15),
                        zorder=2)

        # Milestone Title below node
        ax.text(center_x, 5.25, st["title"], ha='center', va='center',
                fontsize=14, fontweight='bold', color=DARK_TEXT, zorder=3)

        # Small Role Pill Tag
        tag_w = len(st["tag"]) * 0.11 + 0.35
        tag_box = patches.FancyBboxPatch(
            (center_x - tag_w/2, 4.70), tag_w, 0.32,
            boxstyle="round,pad=0.02,rounding_size=0.1",
            fc=st["soft_bg"], ec=c, lw=1.2, zorder=3
        )
        ax.add_patch(tag_box)
        ax.text(center_x, 4.86, st["tag"], ha='center', va='center',
                fontsize=9.5, fontweight='bold', color=c, zorder=4)

        # Floating Card with Bullet Points (Open, clean styling)
        card_box = patches.FancyBboxPatch(
            (cx, 1.85), card_w, 2.65,
            boxstyle="round,pad=0.04,rounding_size=0.2",
            fc='#FFFFFF', ec=c, lw=1.5, zorder=2
        )
        ax.add_patch(card_box)

        # Top colored accent border line inside card
        ax.plot([cx + 0.2, cx + card_w - 0.2], [4.40, 4.40], color=c, lw=2.5, solid_capstyle='round', zorder=3)

        # 4 Points inside card
        pt_start_y = 3.95
        pt_spacing = 0.55
        for p_idx, pt in enumerate(st["points"]):
            py = pt_start_y - p_idx * pt_spacing
            dot = patches.Circle((cx + 0.25, py), 0.05, fc=c, ec=c, zorder=3)
            ax.add_patch(dot)
            ax.text(cx + 0.40, py, pt, ha='left', va='center',
                    fontsize=10.2, color=DARK_TEXT, fontfamily='sans-serif', zorder=3)

    # Bottom Highlight Banner
    ribbon = patches.FancyBboxPatch(
        (0.9, 1.05), 14.2, 0.50,
        boxstyle="round,pad=0.04,rounding_size=0.2",
        fc='#EFF6FF', ec='#1D4ED8', lw=1.4
    )
    ax.add_patch(ribbon)
    ax.text(8.0, 1.30, "⚡ Complete Emergency Triage Cycle: Hospital Request to Nearby Donor Alerts in Under 2 Seconds",
            ha='center', va='center', fontsize=12, fontweight='bold', color='#1D4ED8', fontfamily='sans-serif')

    # Footer
    ax.plot([0.9, 15.1], [0.65, 0.65], color='#E2E8F0', lw=1.2)
    ax.text(0.9, 0.35, "RV Institute of Technology, Bijnor  •  B.Tech Computer Science & Engineering (2026-27)",
            fontsize=10, color=MUTED_TEXT, fontfamily='sans-serif')
    ax.text(15.1, 0.35, "Cloud-Based Online Blood Bank & Emergency Triage System",
            ha='right', fontsize=10, fontweight='bold', color=DARK_TEXT, fontfamily='sans-serif')

    out_path = "Slide_7_System_Workflow.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print("Slide 7 generated successfully:", out_path)

    for dt in ["C:/Users/rajpu/OneDrive/Desktop", "C:/Users/rajpu/Desktop"]:
        if os.path.exists(dt):
            dest = os.path.join(dt, "Slide_7_System_Workflow.png")
            shutil.copyfile(out_path, dest)
            print("Copied Slide 7 to Desktop:", dest)


def generate_slide10():
    # 16:9 Widescreen aspect ratio at 200 DPI (3200 x 1800 px)
    # Dark Slate Theme for Dramatic Keynote Conclusion!
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Top Crimson Glow Strip
    top_glow = patches.Rectangle((0, 8.88), 16, 0.12, fc='#DC2626', ec='none')
    ax.add_patch(top_glow)

    # Top Category Pill
    badge = patches.FancyBboxPatch(
        (0.9, 8.15), 3.0, 0.42,
        boxstyle="round,pad=0.08,rounding_size=0.2",
        fc='#1E293B', ec='#DC2626', lw=1.4
    )
    ax.add_patch(badge)
    ax.text(2.4, 8.36, "CONCLUSION & ROADMAP", ha='center', va='center',
            fontsize=11.5, fontweight='bold', color='#FCA5A5', fontfamily='sans-serif')

    # Main Title & Subtitle
    ax.text(0.9, 7.55, "Project Conclusion & Future Horizons",
            fontsize=28, fontweight='bold', color='#FFFFFF', fontfamily='sans-serif')
    ax.text(0.9, 7.10, "Transforming emergency blood supply with cloud automation, zero wastage, and instant triage",
            fontsize=13, color='#94A3B8', fontfamily='sans-serif')

    # Divider line
    ax.plot([0.9, 15.1], [6.75, 6.75], color='#334155', lw=1.2)

    # Left Section: 3 Core Project Achievements + Future Roadmap (Width: 8.0)
    achievements = [
        ("Response Speed: Under 2 Seconds", "Replaced 45 minutes of panic phone calls with instant automated cloud broadcasting.", "#DC2626"),
        ("Wastage Elimination: 90% Reduction", "Smart FIFO algorithm ensures older safe blood packets are dispatched before expiry.", "#059669"),
        ("Zero Hosting Cost: 100% Free Cloud", "Scalable, production-ready cloud deployment running on zero maintenance cost.", "#2563EB")
    ]

    for a_idx, (title, desc, a_col) in enumerate(achievements):
        ay = 5.75 - a_idx * 1.05
        acard = patches.FancyBboxPatch(
            (0.9, ay), 8.0, 0.88,
            boxstyle="round,pad=0.03,rounding_size=0.18",
            fc='#1E293B', ec='#334155', lw=1.2, zorder=2
        )
        ax.add_patch(acard)

        # Left color bar
        ax.plot([1.08, 1.08], [ay + 0.15, ay + 0.73], color=a_col, lw=4, solid_capstyle='round', zorder=3)

        # Title & Desc
        ax.text(1.30, ay + 0.56, title, fontsize=13, fontweight='bold', color='#FFFFFF', zorder=3)
        ax.text(1.30, ay + 0.25, desc, fontsize=10.5, color='#CBD5E1', zorder=3)

    # Future Roadmap Sub-Header
    ax.text(0.9, 2.25, "Future Scope & Innovations:",
            fontsize=15, fontweight='bold', color='#FCA5A5', fontfamily='sans-serif')

    roadmap_items = [
        ("AI Demand Forecasting", "Predict blood shortages 7 days ahead using machine learning models", "#38BDF8"),
        ("Drone Emergency Transit", "Fast aerial delivery of rare blood units to remote rural health clinics", "#34D399"),
        ("Native Mobile App", "Cross-platform iOS and Android app with real-time GPS ambulance tracking", "#A78BFA")
    ]

    for r_idx, (r_title, r_desc, r_col) in enumerate(roadmap_items):
        ry = 1.65 - r_idx * 0.46
        # Small indicator dot
        r_dot = patches.Circle((1.1, ry + 0.05), 0.06, fc=r_col, ec=r_col, zorder=3)
        ax.add_patch(r_dot)
        ax.text(1.3, ry + 0.05, f"{r_title}:", fontsize=11, fontweight='bold', color=r_col, zorder=3)
        ax.text(3.6, ry + 0.05, r_desc, fontsize=10.5, color='#CBD5E1', zorder=3)

    # Right Section: Big "THANK YOU" & Team Card (Width: 5.7)
    ty_card = patches.FancyBboxPatch(
        (9.4, 1.15), 5.7, 5.45,
        boxstyle="round,pad=0.05,rounding_size=0.25",
        fc='#1E293B', ec='#DC2626', lw=2, zorder=2
    )
    ax.add_patch(ty_card)

    # Thank you header
    ax.text(12.25, 6.05, "THANK YOU!", ha='center', va='center',
            fontsize=30, fontweight='bold', color='#FFFFFF', zorder=3)
    ax.text(12.25, 5.55, "Any Questions or Suggestions?", ha='center', va='center',
            fontsize=14, fontweight='bold', color='#93C5FD', zorder=3)

    ax.plot([10.0, 14.5], [5.20, 5.20], color='#334155', lw=1.5, zorder=3)

    # Team Members
    ax.text(10.0, 4.80, "PRESENTED BY (TEAM MEMBERS):",
            fontsize=11.5, fontweight='bold', color='#FCA5A5', zorder=3)

    members = [
        ("Khyati Rajput", "2305010100024"),
        ("Kashish Tyagi", "2305010100023"),
        ("Aksha Parveen", "2305010100005"),
        ("Aaditya Yadav", "2305010100001")
    ]

    for m_idx, (m_name, m_roll) in enumerate(members):
        my = 4.35 - m_idx * 0.42
        dot = patches.Circle((10.2, my), 0.05, fc='#DC2626', ec='#DC2626', zorder=3)
        ax.add_patch(dot)
        ax.text(10.45, my, f"{m_name}   ({m_roll})",
                fontsize=12, fontweight='bold', color='#FFFFFF', zorder=3)

    ax.plot([10.0, 14.5], [2.50, 2.50], color='#334155', lw=1.5, zorder=3)

    # Guide Details
    ax.text(10.0, 2.15, "PROJECT GUIDE:",
            fontsize=10.5, fontweight='bold', color='#94A3B8', zorder=3)
    ax.text(10.0, 1.80, "Mr. Manish Kumar",
            fontsize=16, fontweight='bold', color='#FFFFFF', zorder=3)
    ax.text(10.0, 1.45, "Trainer & Project Guide  •  Department of CSE",
            fontsize=10, color='#CBD5E1', zorder=3)

    # Footer
    ax.plot([0.9, 15.1], [0.65, 0.65], color='#334155', lw=1.2)
    ax.text(0.9, 0.35, "RV Institute of Technology, Bijnor  •  B.Tech Computer Science & Engineering (2026-27)",
            fontsize=10, color='#64748B', fontfamily='sans-serif')
    ax.text(15.1, 0.35, "Affiliated to AKTU, Lucknow",
            ha='right', fontsize=10, color='#64748B', fontfamily='sans-serif')

    out_path = "Slide_10_Conclusion_Roadmap.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='#0F172A')
    plt.close()
    print("Slide 10 generated successfully:", out_path)

    for dt in ["C:/Users/rajpu/OneDrive/Desktop", "C:/Users/rajpu/Desktop"]:
        if os.path.exists(dt):
            dest = os.path.join(dt, "Slide_10_Conclusion_Roadmap.png")
            shutil.copyfile(out_path, dest)
            print("Copied Slide 10 to Desktop:", dest)

if __name__ == "__main__":
    generate_slide7()
    generate_slide10()
