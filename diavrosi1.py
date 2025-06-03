import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Συντελεστές εδάφους και προστασίας
soil_types = {'Άμμος': 2.0, 'Πηλός': 1.0, 'Βράχος': 0.5, 'Χαλίκι': 0.8}
protection_factors = {'Καμία': 1.0, 'Κυματοθραύστες': 0.4, 'Τεχνητή παραλία': 0.5, 'Αναχώματα': 0.3}

# Εικόνα παραλίας
st.image("https://www.patrisnews.com/wp-content/uploads/2014/11/diavrosh.jpg", caption="Παραλία υπό διάβρωση", use_container_width=True)

st.title("🌊 Εκπαιδευτικό Εργαλείο: Διάβρωση Παραλίας")
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

# Επεξήγηση Γωνίας Πρόσκρουσης
with st.expander("❓ Τι είναι η Γωνία Πρόσκρουσης Κυμάτων;"):
    st.markdown("""
    Η **γωνία πρόσκρουσης** δείχνει από ποια κατεύθυνση έρχονται τα κύματα σε σχέση με την παραλία:

    - 🟦 0° → Τα κύματα έρχονται ευθεία, χτυπούν κάθετα την ακτή → έντονη, κάθετη διάβρωση  
    - 🔁 45° → Τα κύματα έρχονται λοξά → παρασύρουν υλικά κατά μήκος της ακτής  
    - 🔄 90° → Τα κύματα κινούνται σχεδόν παράλληλα με την ακτή → μικρότερη κάθετη διάβρωση, μεγαλύτερη μεταφορά άμμου  

    Παρακάτω βλέπεις ένα σχήμα με παραδείγματα:
    """)

    # Διάγραμμα με matplotlib
    fig_angle, ax_angle = plt.subplots(figsize=(6, 4))

    # Ακτή (κάθετη γραμμή)
    ax_angle.plot([3, 3], [0, 3], color='saddlebrown', linewidth=5, label='Ακτή')

    # Κύμα 0°
    ax_angle.annotate("0°", xy=(3, 1.5), xytext=(1.8, 1.5),
                      arrowprops=dict(arrowstyle='->', lw=2, color='green'), fontsize=10, color='green')

    # Κύμα 45°
    ax_angle.annotate("45°", xy=(3, 2.5), xytext=(1.5, 3),
                      arrowprops=dict(arrowstyle='->', lw=2, color='orange'), fontsize=10, color='orange')

    # Κύμα 90°
    ax_angle.annotate("90°", xy=(3.2, 0.5), xytext=(4.8, 0.5),
                      arrowprops=dict(arrowstyle='->', lw=2, color='red'), fontsize=10, color='red')

    ax_angle.set_xlim(0, 6)
    ax_angle.set_ylim(0, 3.5)
    ax_angle.axis('off')
    st.pyplot(fig_angle)

    st.markdown("""
    👉 Όταν αυξάνεται η γωνία πρόσκρουσης:
    - Η **κάθετη διάβρωση μειώνεται** (τα κύματα δεν «χτυπούν» δυνατά την ακτή)
    - Η **παράλληλη μεταφορά άμμου αυξάνεται**, με αποτέλεσμα να αλλάζει το σχήμα της παραλίας

    Δες και αυτό το μικρό animation:
    """)

    # Ενσωμάτωση GIF με κίνηση κύματος
    st.image(
    "https://upload.wikimedia.org/wikipedia/commons/2/2c/Beach_drift.gif",
    caption="👉 Δες πώς τα κύματα που έρχονται λοξά μεταφέρουν την άμμο κατά μήκος της ακτής!",
    use_container_width=True
)


# Footer
st.markdown("---")
st.markdown("Δημιουργήθηκε για εκπαιδευτικούς σκοπούς 🌍")
