import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Συντελεστές εδάφους και προστασίας
soil_types = {'Άμμος': 2.0, 'Πηλός': 1.0, 'Βράχος': 0.5, 'Χαλίκι': 0.8}
protection_factors = {'Καμία': 1.0, 'Κυματοθραύστες': 0.4, 'Τεχνητή παραλία': 0.5, 'Αναχώματα': 0.3}
vegetation_factor = 0.7  # Βλάστηση μειώνει τη διάβρωση κατά 30%
human_impact_factors = {
    "Καμία": 1.0,
    "Καταστροφή Βλάστησης": 1.3,
    "Κτίρια Κοντά στην Ακτή": 1.5,
    "Θετική Περιβαλλοντική Διαχείριση": 0.7
}

# Εικόνα παραλίας
st.image("https://www.patrisnews.com/wp-content/uploads/2014/11/diavrosh.jpg", caption="Παραλία υπό διάβρωση", use_container_width=True)

st.title("🌊 Εκπαιδευτικό Εργαλείο: Διάβρωση Παραλίας")
st.markdown("**Πειραματίσου με διαφορετικές παραμέτρους και δες πώς η παραλία αλλάζει με τα χρόνια!**")

# Διάγραμμα γωνίας πρόσκρουσης
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

# Επεξήγηση Γωνίας Πρόσκρουσης
with st.expander("❓ Τι είναι η Γωνία Πρόσκρουσης Κυμάτων;"):
    st.markdown("""
    Η **γωνία πρόσκρουσης** δείχνει από ποια κατεύθυνση έρχονται τα κύματα σε σχέση με τη γραμμή της ακτής:

    - 🟩 **0°** → Τα κύματα έρχονται **κάθετα** στην ακτή → **μέγιστη διάβρωση**
    - 🟧 **45°** → Τα κύματα έρχονται **λοξά** → διάβρωση και μεταφορά υλικών
    - 🟥 **90°** → Τα κύματα κινούνται **παράλληλα** με την ακτή → ελάχιστη κάθετη διάβρωση
    """)
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
    βλαστηση = st.checkbox("🌿 Υπάρχει Βλάστηση;")
    ανθρωπινη_παρεμβαση = st.selectbox("Ανθρώπινη Παρέμβαση", list(human_impact_factors.keys()))
    χρόνια = st.slider("Διάρκεια Προσομοίωσης (έτη)", 1, 50, 10)

# Υπολογισμός διάβρωσης
K = soil_types[τύπος_ακτής]
P = protection_factors[έργο_προστασίας]
θ_rad = np.radians(γωνία)
erosion_rate = K * ύψος_κύματος * συχνότητα * abs(np.cos(θ_rad)) * P

if βλαστηση:
    erosion_rate *= vegetation_factor

erosion_rate *= human_impact_factors[ανθρωπινη_παρεμβαση]

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

# Γράφημα
fig, ax = plt.subplots()
ax.plot(έτη, υποχώρηση, marker='o', color='teal')
ax.set_xlabel("Έτη")
ax.set_ylabel("Υποχώρηση Ακτής (m)")
ax.set_title("Προσομοίωση Διάβρωσης Παραλίας")
ax.grid(True)
st.pyplot(fig)

# Επεξήγηση Βλάστησης
st.markdown("""
### 🌿 Πώς βοηθά η Βλάστηση;
- Η παρουσία **φυτών και ριζών** στην παραλία:
  - **Σταθεροποιεί** το έδαφος
  - Μειώνει την **απώλεια υλικού** από τα κύματα και τον άνεμο
  - **Απορροφά** την ενέργεια των κυμάτων

👉 Στην προσομοίωση, η βλάστηση μειώνει τη διάβρωση κατά **30%**
""")

# Επεξήγηση Ανθρώπινου Παράγοντα
st.markdown("""
### 👣 Ρόλος του Ανθρώπινου Παράγοντα
- Οι ανθρώπινες παρεμβάσεις επηρεάζουν **θετικά ή αρνητικά** την ακτή:

| Παρέμβαση | Επίδραση |
|----------|----------|
| ❌ Καταστροφή Βλάστησης | Αυξάνει τη διάβρωση |
| ❌ Κτίρια κοντά στην ακτή | Επιταχύνουν την υποχώρηση |
| ✅ Θετική Περιβαλλοντική Διαχείριση | Μειώνει τη διάβρωση |

👉 Η επιλογή σου επηρεάζει άμεσα το αποτέλεσμα της προσομοίωσης.
""")

# Footer
st.markdown("---")
st.markdown("Δημιουργήθηκε για εκπαιδευτικούς σκοπούς 🌍")
