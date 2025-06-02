import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Συντελεστές εδάφους και προστασίας
soil_types = {'Άμμος': 2.0, 'Πηλός': 1.0, 'Βράχος': 0.5, 'Χαλίκι': 0.8}
protection_factors = {'Καμία': 1.0, 'Κυματοθραύστες': 0.4, 'Τεχνητή παραλία': 0.5, 'Αναχώματα': 0.3}

# Εικόνα παραλίας
st.image("https://upload.wikimedia.org/wikipedia/commons/8/8e/Beach_wave.jpg", caption="Παραλία υπό διάβρωση", use_column_width=True)

st.title("🌊 Εκπαιδευτικό Εργαλείο--  : Διάβρωση Παραλίας")
st.markdown("**Πειραματίσου με διαφορετικές παραμέτρους και δες πώς η παραλία αλλάζει με τα χρόνια!**")

# Εισαγωγή παραμέτρων
col1, col2 = st.columns(2)
with col1:
    ύψος_κύματος = st.slider("Ύψος Κύματος (m)", 0.5, 5.0, 1.5, step=0.1)
    συχνότητα = st.slider("Συχνότητα Κυμάτων (κύματα/ώρα)", 1, 20, 5)
    γωνία = st.slider("Γωνία Πρόσπτωσης (μοίρες)", 0, 90, 45)
with col2:
    τύπος_ακτής = st.selectbox("Τύπος Ακτής", list(soil_types.keys()))
    έργο_προστασίας = st.selectbox("Έργο Προστασίας", list(protection_factors.keys()))
    χρόνια = st.slider("Διάρκεια Προσομοίωσης (έτη)", 1, 50, 10)

# Υπολογισμός
K = soil_types[τύπος_ακτής]
P = protection_factors[έργο_προστασίας]
θ_rad = np.radians(γωνία)
erosion_rate = K * ύψος_κύματος * συχνότητα * abs(np.sin(θ_rad)) * P
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

# Επεξήγηση
st.markdown("""
### ℹ️ Τι δείχνει το γράφημα;
- Όσο μεγαλύτερη η **υποχώρηση**, τόσο περισσότερη διάβρωση έχει συμβεί.
- Η **διάβρωση επηρεάζεται** από:
  - Ύψος και συχνότητα κύματος
  - Τύπο εδάφους
  - Γωνία πρόσπτωσης
  - Παρουσία έργων προστασίας
""")

# Footer
st.markdown("---")
st.markdown("Δημιουργήθηκε για εκπαιδευτικούς σκοπούς 🌍")
