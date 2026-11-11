import matplotlib.pyplot as plt
import numpy as np
import shutil
import os

def create_formal_blood_compatibility_chart(filename):
    blood_types = ['O-', 'O+', 'B-', 'B+', 'A-', 'A+', 'AB-', 'AB+']
    n = len(blood_types)
    
    # Compatibility matrix: 1 if donor can give to recipient, 0 otherwise
    matrix = np.zeros((n, n), dtype=int)
    
    rules = {
        'O-': ['O-', 'O+', 'B-', 'B+', 'A-', 'A+', 'AB-', 'AB+'],
        'O+': ['O+', 'B+', 'A+', 'AB+'],
        'B-': ['B-', 'B+', 'AB-', 'AB+'],
        'B+': ['B+', 'AB+'],
        'A-': ['A-', 'A+', 'AB-', 'AB+'],
        'A+': ['A+', 'AB+'],
        'AB-': ['AB-', 'AB+'],
        'AB+': ['AB+']
    }
    
    for i, donor in enumerate(blood_types):
        for j, recip in enumerate(blood_types):
            if recip in rules[donor]:
                matrix[i, j] = 1
                
    fig, ax = plt.subplots(figsize=(10.5, 8.2), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#FFFFFF')
    
    # Custom color map: crisp white/slate for non-compatible, emerald green for compatible
    cmap = plt.matplotlib.colors.ListedColormap(['#F1F5F9', '#10B981'])
    ax.imshow(matrix, cmap=cmap, aspect='auto')
    
    # Ticks and Labels
    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(blood_types, fontsize=12, fontweight='bold', color='#0F172A')
    ax.set_yticklabels(blood_types, fontsize=12, fontweight='bold', color='#0F172A')
    
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.set_xlabel('RECIPIENT BLOOD TYPE (Patient Receiving Transfusion)', fontsize=13, fontweight='bold', color='#B91C1C', labelpad=14)
    ax.set_ylabel('DONOR BLOOD TYPE (Transfusion Source)', fontsize=13, fontweight='bold', color='#0F172A', labelpad=14)
    
    # Grid lines
    ax.set_xticks(np.arange(-.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-.5, n, 1), minor=True)
    ax.grid(which='minor', color='#CBD5E1', linestyle='-', linewidth=1.5)
    ax.tick_params(which='minor', size=0)
    
    # Annotations inside matrix cells
    for i in range(n):
        for j in range(n):
            if matrix[i, j] == 1:
                ax.text(j, i, '✔ YES', ha='center', va='center', color='#065F46', fontweight='bold', fontsize=11)
            else:
                ax.text(j, i, '—', ha='center', va='center', color='#94A3B8', fontsize=12)
                
    # Formal Title & Subtitle
    plt.title('CLINICAL BLOOD COMPATIBILITY MATRIX\nRed Blood Cell (RBC) Transfusion Compatibility Standards',
              fontsize=15, fontweight='bold', color='#0F172A', pad=42)
    
    # Formal Clinical Notes
    plt.figtext(0.10, 0.04, 
                "• O-NEGATIVE (O-): UNIVERSAL DONOR — Compatible with all red blood cell recipient types.\n"
                "• AB-POSITIVE (AB+): UNIVERSAL RECIPIENT — Safely receives red blood cells from all certified blood types.",
                fontsize=10.5, fontweight='bold', color='#991B1B', 
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#FEF2F2', edgecolor='#FCA5A5', linewidth=1.2))
                
    plt.figtext(0.72, 0.04, 
                "Standard Transfusion Protocol:\nRows: Donor Source Group\nColumns: Recipient Patient Group",
                fontsize=9.5, fontstyle='italic', color='#475569',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#F1F5F9', edgecolor='#CBD5E1', linewidth=1))

    plt.tight_layout(rect=[0.05, 0.11, 0.95, 0.93])
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Formal chart generated successfully at: {filename}")

if __name__ == "__main__":
    out1 = r"c:\Users\rajpu\OneDrive\Desktop\Training\blood_compatibility_chart.png"
    out2 = r"c:\Users\rajpu\OneDrive\Desktop\Training\static\images\blood_compatibility_chart.png"
    
    create_formal_blood_compatibility_chart(out1)
    
    os.makedirs(os.path.dirname(out2), exist_ok=True)
    shutil.copyfile(out1, out2)
    print(f"Chart copied to static folder: {out2}")
