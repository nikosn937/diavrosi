import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Συντελεστές εδάφους και προστασίας
soil_types = {'Άμμος': 2.0, 'Πηλός': 1.0, 'Βράχος': 0.5, 'Χαλίκι': 0.8}
protection_factors = {
    'Καμία': 1.0,
    'Κυματοθραύστες': 0.4,
    'Τεχνητή παραλία': 0.5,
    'Αναχώματα': 0.3,
    'Βλάστηση': None  # Τιμή που θα ρυθμιστεί αργότερα
}
vegetation_levels = {
    "Αραιή Βλάστηση": 0.8,
    "Μέτρια Βλάστηση": 0.6,
    "Πυκνή Βλάστηση": 0.4
}

# Εικόνα παραλίας
st.image("https://www.patrisnews.com/wp-content/uploads/2014/11/diavrosh.jpg", caption="Παραλία υπό διάβρωση", use_container_width=True)

st.title("🌊 Εκπαιδευτικό Εργαλείο: Διάβρωση Παραλίας")
st.markdown("**Πειραματίσου με διαφορετικές παραμέτρους και δες πώς η παραλία αλλάζει με τα χρόνια!**")

# Επεξήγηση Γωνίας Πρόσκρουσης
with st.expander("❓ Τι είναι η Γωνία Πρόσκρουσης Κυμάτων;"):
    st.markdown("""
    Η **γωνία πρόσκρουσης** δείχνει από ποια κατεύθυνση έρχονται τα κύματα σε σχέση με τη γραμμή της ακτής:

    - 🟩 **0°** → Τα κύματα έρχονται **κάθετα** στην ακτή → **μέγιστη διάβρωση**
    - 🟧 **45°** → Τα κύματα έρχονται **λοξά** → διάβρωση και μεταφορά υλικών
    - 🟥 **90°** → Τα κύματα κινούνται **παράλληλα** με την ακτή → ελάχιστη κάθετη διάβρωση

    Παρακάτω βλέπεις ένα απλό σχήμα:
    """)

    # Διάγραμμα με matplotlib
    fig_angle, ax_angle = plt.subplots(figsize=(6, 4))
    ax_angle.plot([3, 3], [0, 3], color='saddlebrown', linewidth=5, label='Ακτή')
    ax_angle.annotate("0°", xy=(3, 1.5), xytext=(1.3, 1.5),
                      arrowprops=dict(arrowstyle='->', lw=2, color='green'), fontsize=10, color='green')
    ax_angle.annotate("45°", xy=(3, 2.5), xytext=(1.4, 3.2),
                      arrowprops=dict(arrowstyle='->', lw=2, color='orange'), fontsize=10, color='orange')
    ax_angle.annotate("90°", xy=(3.1, 0.5), xytext=(3.1, 1.5),
                      arrowprops=dict(arrowstyle='->', lw=2, color='red'), fontsize=10, color='red')
    ax_angle.set_xlim(0, 6)
    ax_angle.set_ylim(0, 3.5)
    ax_angle.axis('off')
    st.pyplot(fig_angle)

    st.markdown("""
    👉 Όταν **μειώνεται** η γωνία:
    - Τα κύματα χτυπούν **πιο κάθετα** την ακτή → **μεγαλύτερη διάβρωση**
    
    👉 Όταν **αυξάνεται** η γωνία:
    - Τα κύματα κινούνται **παράλληλα** → **λιγότερη κάθετη διάβρωση**, αλλά πιθανή μεταφορά άμμου κατά μήκος της ακτής
    """)

# Εισαγωγή παραμέτρων
col1, col2 = st.columns(2)
with col1:
    ύψος_κύματος = st.slider("Ύψος Κύματος (m)", 0.1, 3.0, 1.5, step=0.1)
    συχνότητα = st.slider("Συχνότητα Κυμάτων (κύματα/ώρα)", 1, 100, 10)
    γωνία = st.slider("Γωνία Πρόσπτωσης (μοίρες)", 0, 90, 45)
with col2:
    τύπος_ακτής = st.selectbox("Τύπος Ακτής", list(soil_types.keys()))
    έργο_προστασίας = st.selectbox("Έργο Προστασίας", list(protection_factors.keys()))
    
    # Εμφάνιση υπο-επιλογής τύπου βλάστησης
    if έργο_προστασίας == "Βλάστηση":
        τύπος_βλάστησης = st.selectbox("Είδος Βλάστησης", list(vegetation_levels.keys()))
        P = vegetation_levels[τύπος_βλάστησης]
    else:
        τύπος_βλάστησης = None
        P = protection_factors[έργο_προστασίας]

    χρόνια = st.slider("Διάρκεια Προσομοίωσης (έτη)", 1, 50, 10)

# Υπολογισμός διάβρωσης
K = soil_types[τύπος_ακτής]
θ_rad = np.radians(γωνία)
erosion_rate = K * ύψος_κύματος * συχνότητα * abs(np.cos(θ_rad)) * P
έτη = np.arange(0, χρόνια + 1)
υποχώρηση = erosion_rate * έτη

# Εμφάνιση αποτελεσμάτων
st.subheader("📊 Αποτελέσματα:")
st.write(f"**Ρυθμός Διάβρωσης**: {erosion_rate:.2f} m/έτος")
df = pd.DataFrame({"Έτος": έτη, "Υποχώρηση Ακτής (m)": υποχώρηση})
st.dataframe(df)

# Κατέβασμα σε CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Κατέβασε τα αποτελέσματα σε CSV", csv, "διαβρωση.csv", "text/csv")

# Διάγραμμα
τίτλος = "Προσομοίωση Διάβρωσης Παραλίας"
if έργο_προστασίας == "Βλάστηση" and τύπος_βλάστησης:
    τίτλος += f" με {τύπος_βλάστησης}"
else:
    τίτλος += f" ({έργο_προστασίας})"

fig, ax = plt.subplots()
ax.plot(έτη, υποχώρηση, marker='o', color='teal')
ax.set_xlabel("Έτη")
ax.set_ylabel("Υποχώρηση Ακτής (m)")
ax.set_title(τίτλος)
ax.grid(True)
st.pyplot(fig)

# Επεξήγηση
st.markdown("""
### ℹ️ Τι δείχνει το γράφημα;
- Όσο μεγαλύτερη η **υποχώρηση**, τόσο περισσότερη διάβρωση έχει συμβεί.
- Η **διάβρωση επηρεάζεται** από:
  - Ύψος και συχνότητα κύματος
  - Τύπο εδάφους
  - Γωνία πρόσκρουσης (πιο κάθετη = πιο έντονη)
  - Παρουσία έργων προστασίας (π.χ. βλάστηση, κυματοθραύστες)
""")

# Footer
st.markdown("---")
st.markdown("Δημιουργήθηκε για εκπαιδευτικούς σκοπούς 🌍")
