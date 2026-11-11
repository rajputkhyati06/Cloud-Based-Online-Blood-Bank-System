import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import shutil

def generate_linkedin_showcase_1():
    # 16:9 Widescreen aspect ratio (2400 x 1350 px at 150 DPI)
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor('#0F172A') # Dark Slate background for high-tech premium feel
    ax.set_facecolor('#0F172A')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Top Red Accent Glow
    top_glow = patches.Rectangle((0, 8.88), 16, 0.12, fc='#DC2626', ec='none')
    ax.add_patch(top_glow)

    # Top Header Banner
    badge = patches.FancyBboxPatch(
        (0.8, 8.15), 3.2, 0.42,
        boxstyle="round,pad=0.08,rounding_size=0.2",
        fc='#1E293B', ec='#DC2626', lw=1.5
    )
    ax.add_patch(badge)
    ax.text(2.4, 8.36, "FULL-STACK PROJECT SHOWCASE", ha='center', va='center',
            fontsize=11.5, fontweight='bold', color='#FCA5A5', fontfamily='sans-serif')

    ax.text(0.8, 7.55, "Cloud-Based Online Blood Bank & Emergency Triage System",
            fontsize=26, fontweight='bold', color='#FFFFFF', fontfamily='sans-serif')
    ax.text(0.8, 7.10, "A real-time life-saving web application connecting Hospitals, Donors, and Blood Banks in under 2 seconds",
            fontsize=12.5, color='#94A3B8', fontfamily='sans-serif')

    # =========================================================================
    # BROWSER MOCKUP 1: HOSPITAL EMERGENCY DASHBOARD (Left)
    # =========================================================================
    bx1, by1, bw1, bh1 = 0.8, 1.8, 7.1, 4.9
    
    # Browser Window Container
    b_win1 = patches.FancyBboxPatch((bx1, by1), bw1, bh1, boxstyle="round,pad=0.04,rounding_size=0.2",
                                    fc='#FFFFFF', ec='#334155', lw=1.5, zorder=2)
    ax.add_patch(b_win1)
    
    # Browser Top Bar
    b_bar1 = patches.FancyBboxPatch((bx1, by1 + bh1 - 0.5), bw1, 0.5, boxstyle="round,pad=0.02,rounding_size=0.15",
                                    fc='#F1F5F9', ec='#CBD5E1', lw=1, zorder=3)
    ax.add_patch(b_bar1)
    
    # 3 Window Buttons (Red, Yellow, Green)
    for dot_idx, d_col in enumerate(['#EF4444', '#F59E0B', '#10B981']):
        c_dot = patches.Circle((bx1 + 0.3 + dot_idx * 0.22, by1 + bh1 - 0.25), 0.06, fc=d_col, ec='none', zorder=4)
        ax.add_patch(c_dot)
        
    # URL Pill Bar
    url_box1 = patches.FancyBboxPatch((bx1 + 1.2, by1 + bh1 - 0.38), 4.2, 0.26, boxstyle="round,pad=0.02,rounding_size=0.08",
                                      fc='#FFFFFF', ec='#CBD5E1', lw=0.8, zorder=4)
    ax.add_patch(url_box1)
    ax.text(bx1 + 1.35, by1 + bh1 - 0.25, "[SECURE] https://bloodtriage.cloud/hospital/emergency-request",
            fontsize=8.5, color='#64748B', va='center', zorder=5)

    # Content inside Browser 1 (Hospital UI)
    ax.text(bx1 + 0.35, by1 + bh1 - 0.85, "Hospital Emergency Blood Requisition",
            fontsize=13, fontweight='bold', color='#0F172A', zorder=3)
    ax.text(bx1 + 0.35, by1 + bh1 - 1.15, "Logged in as: City Trauma Care Center • Doctor ID: DOC-9042",
            fontsize=9, color='#64748B', zorder=3)

    # Form Fields Simulation
    # Field 1: Blood Group Required
    ax.text(bx1 + 0.35, by1 + bh1 - 1.55, "Required Blood Group:", fontsize=9.5, fontweight='bold', color='#1E293B', zorder=3)
    bg_selector = patches.FancyBboxPatch((bx1 + 0.35, by1 + bh1 - 2.0), 3.0, 0.38,
                                         boxstyle="round,pad=0.02,rounding_size=0.08", fc='#FEF2F2', ec='#DC2626', lw=1.2, zorder=3)
    ax.add_patch(bg_selector)
    ax.text(bx1 + 0.5, by1 + bh1 - 1.81, "O Negative (O-ve) — Universal", fontsize=10, fontweight='bold', color='#DC2626', va='center', zorder=4)

    # Field 2: Units & Urgency
    ax.text(bx1 + 3.65, by1 + bh1 - 1.55, "Triage Urgency Level:", fontsize=9.5, fontweight='bold', color='#1E293B', zorder=3)
    urg_selector = patches.FancyBboxPatch((bx1 + 3.65, by1 + bh1 - 2.0), 3.0, 0.38,
                                          boxstyle="round,pad=0.02,rounding_size=0.08", fc='#FEE2E2', ec='#B91C1C', lw=1.2, zorder=3)
    ax.add_patch(urg_selector)
    ax.text(bx1 + 3.8, by1 + bh1 - 1.81, "[CRITICAL] Priority Triage", fontsize=10, fontweight='bold', color='#991B1B', va='center', zorder=4)

    # Live Status Alert Box
    stat_card = patches.FancyBboxPatch((bx1 + 0.35, by1 + bh1 - 3.25), 6.4, 1.05,
                                       boxstyle="round,pad=0.03,rounding_size=0.12", fc='#EFF6FF', ec='#1D4ED8', lw=1.2, zorder=3)
    ax.add_patch(stat_card)
    ax.text(bx1 + 0.55, by1 + bh1 - 2.45, "Automated Cloud Triage Triggered:", fontsize=10, fontweight='bold', color='#1D4ED8', zorder=4)
    ax.text(bx1 + 0.55, by1 + bh1 - 2.75, "• Local Blood Bank Stock: 0 Units (Out of Stock)", fontsize=9, color='#0F172A', zorder=4)
    ax.text(bx1 + 0.55, by1 + bh1 - 3.00, "• Emergency SOS Broadcast: Sent to 14 active donors in 5.2 km radius", fontsize=9, color='#0F172A', zorder=4)

    # 1-Click Action Button
    btn = patches.FancyBboxPatch((bx1 + 0.35, by1 + 0.35), 6.4, 0.50, boxstyle="round,pad=0.03,rounding_size=0.1",
                                 fc='#DC2626', ec='#B91C1C', lw=1, zorder=3)
    ax.add_patch(btn)
    ax.text(bx1 + 3.55, by1 + 0.60, "DISPATCH EMERGENCY SOS TO DONORS (< 2s)", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color='#FFFFFF', zorder=4)


    # =========================================================================
    # BROWSER MOCKUP 2: LIVE BLOOD INVENTORY & FIFO (Right)
    # =========================================================================
    bx2, by2, bw2, bh2 = 8.2, 1.8, 7.0, 4.9

    b_win2 = patches.FancyBboxPatch((bx2, by2), bw2, bh2, boxstyle="round,pad=0.04,rounding_size=0.2",
                                    fc='#FFFFFF', ec='#334155', lw=1.5, zorder=2)
    ax.add_patch(b_win2)

    b_bar2 = patches.FancyBboxPatch((bx2, by2 + bh2 - 0.5), bw2, 0.5, boxstyle="round,pad=0.02,rounding_size=0.15",
                                    fc='#F1F5F9', ec='#CBD5E1', lw=1, zorder=3)
    ax.add_patch(b_bar2)

    for dot_idx, d_col in enumerate(['#EF4444', '#F59E0B', '#10B981']):
        c_dot = patches.Circle((bx2 + 0.3 + dot_idx * 0.22, by2 + bh2 - 0.25), 0.06, fc=d_col, ec='none', zorder=4)
        ax.add_patch(c_dot)

    url_box2 = patches.FancyBboxPatch((bx2 + 1.2, by2 + bh2 - 0.38), 4.2, 0.26, boxstyle="round,pad=0.02,rounding_size=0.08",
                                      fc='#FFFFFF', ec='#CBD5E1', lw=0.8, zorder=4)
    ax.add_patch(url_box2)
    ax.text(bx2 + 1.35, by2 + bh2 - 0.25, "[SECURE] https://bloodtriage.cloud/admin/inventory-fifo",
            fontsize=8.5, color='#64748B', va='center', zorder=5)

    # Content inside Browser 2 (Live Stock & FIFO)
    ax.text(bx2 + 0.35, by2 + bh2 - 0.85, "Blood Bank Central Inventory & FIFO Dispatch",
            fontsize=13, fontweight='bold', color='#0F172A', zorder=3)
    ax.text(bx2 + 0.35, by2 + bh2 - 1.15, "PostgreSQL Cloud Live Sync • Automatic Expiration Avoidance",
            fontsize=9, color='#64748B', zorder=3)

    # 4 Stock Quick Counter Cards
    stocks = [
        ("A+", "24 Units", "#1D4ED8", "#EFF6FF"),
        ("B+", "38 Units", "#059669", "#ECFDF5"),
        ("O+", "18 Units", "#D97706", "#FFFBEB"),
        ("AB-", "4 Units", "#DC2626", "#FEF2F2")
    ]
    for s_idx, (b_type, b_cnt, b_col, b_bg) in enumerate(stocks):
        sx = bx2 + 0.35 + s_idx * 1.6
        sc = patches.FancyBboxPatch((sx, by2 + bh2 - 2.0), 1.45, 0.70, boxstyle="round,pad=0.02,rounding_size=0.1",
                                    fc=b_bg, ec=b_col, lw=1.2, zorder=3)
        ax.add_patch(sc)
        ax.text(sx + 0.725, by2 + bh2 - 1.55, b_type, ha='center', va='center', fontsize=13, fontweight='bold', color=b_col, zorder=4)
        ax.text(sx + 0.725, by2 + bh2 - 1.82, b_cnt, ha='center', va='center', fontsize=9.5, color='#475569', zorder=4)

    # FIFO Dispatch Table Header
    ax.text(bx2 + 0.35, by2 + bh2 - 2.30, "Smart FIFO Queue (Oldest Safe Unit First):", fontsize=9.5, fontweight='bold', color='#1E293B', zorder=3)

    fifo_rows = [
        ("UNIT-4091", "A+", "Safe (Expires in 4d)", "Priority 1 (Dispatch Next)", "#059669", "#D1FAE5"),
        ("UNIT-4102", "B+", "Safe (Expires in 8d)", "Priority 2 (Queued)", "#2563EB", "#DBEAFE"),
        ("UNIT-4155", "O+", "Safe (Expires in 19d)", "Buffer Stock", "#64748B", "#F1F5F9")
    ]
    for r_idx, (u_id, u_grp, u_exp, u_stat, u_c, u_b) in enumerate(fifo_rows):
        ry = by2 + bh2 - 2.85 - r_idx * 0.48
        r_box = patches.FancyBboxPatch((bx2 + 0.35, ry), 6.3, 0.40, boxstyle="round,pad=0.02,rounding_size=0.08",
                                       fc=u_b, ec=u_c, lw=0.8, zorder=3)
        ax.add_patch(r_box)
        ax.text(bx2 + 0.5, ry + 0.20, f"• {u_id} ({u_grp})", fontsize=9, fontweight='bold', color='#0F172A', va='center', zorder=4)
        ax.text(bx2 + 2.5, ry + 0.20, u_exp, fontsize=8.5, color='#475569', va='center', zorder=4)
        ax.text(bx2 + 4.6, ry + 0.20, u_stat, fontsize=8.5, fontweight='bold', color=u_c, va='center', zorder=4)

    # Bottom Tag in Browser 2
    b2_tag = patches.FancyBboxPatch((bx2 + 0.35, by2 + 0.35), 6.3, 0.45, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc='#ECFDF5', ec='#059669', lw=1, zorder=3)
    ax.add_patch(b2_tag)
    ax.text(bx2 + 3.5, by2 + 0.57, "⚡ 90% Wastage Reduced via Automated Expiry Tracking",
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#059669', zorder=4)

    # Bottom Footer
    ax.plot([0.8, 15.2], [0.95, 0.95], color='#334155', lw=1.2)
    ax.text(0.8, 0.55, "RV Institute of Technology, Bijnor • 4th Year B.Tech CSE (2026-27)",
            fontsize=10.5, color='#94A3B8', fontfamily='sans-serif')
    ax.text(15.2, 0.55, "Team: Khyati Rajput • Kashish Tyagi • Aksha Parveen • Aaditya Yadav | Guide: Mr. Manish Kumar",
            ha='right', fontsize=10.5, color='#FCA5A5', fontfamily='sans-serif')

    out_path = "LinkedIn_Project_Showcase_Overview.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='#0F172A')
    plt.close()
    print("Showcase 1 generated successfully:", out_path)

    for dt in ["C:/Users/rajpu/OneDrive/Desktop", "C:/Users/rajpu/Desktop"]:
        if os.path.exists(dt):
            dest = os.path.join(dt, "LinkedIn_Project_Showcase_Overview.png")
            shutil.copyfile(out_path, dest)
            print("Copied to Desktop:", dest)

if __name__ == "__main__":
    generate_linkedin_showcase_1()
