import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation # Νέα εισαγωγή
from PIL import Image

# Συντελεστές εδάφους και προστασίας
soil_types = {'Άμμος': 2.0, 'Πηλός': 1.0, 'Βράχος': 0.5, 'Χαλίκι': 0.8}
protection_factors = {'Καμία': 1.0, 'Κυματοθραύστες': 0.4, 'Τεχνητή παραλία': 0.5, 'Αναχώματα': 0.3}

# Εικόνα παραλίας
st.image("https://upload.wikimedia.org/wikipedia/commons/8/8e/Beach_wave.jpg", caption="Παραλία υπό διάβρωση", use_column_width=True)

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

st.markdown("---")

## Προσομοίωση Διάβρωσης με Animation

st.subheader("⏳ Εξέλιξη Διάβρωσης με τα Χρόνια:")

# Δημιουργία γραφήματος για animation
fig_anim, ax_anim = plt.subplots()
line, = ax_anim.plot([], [], marker='o', color='teal')
ax_anim.set_xlabel("Έτη")
ax_anim.set_ylabel("Υποχώρηση Ακτής (m)")
ax_anim.set_title("Προσομοίωση Διάβρωσης Παραλίας - Εξέλιξη")
ax_anim.grid(True)
ax_anim.set_xlim(0, χρόνια)
ax_anim.set_ylim(0, υποχώρηση[-1] * 1.1 if υποχώρηση[-1] > 0 else 1) # Αυξάνουμε λίγο το y-limit αν υπάρχει υποχώρηση

# Συνάρτηση ενημέρωσης του animation
def update(frame):
    current_year = frame
    if current_year <= χρόνια: # Ελέγχουμε να μην ξεπεράσουμε τα χρόνια
        xdata = έτη[:current_year + 1]
        ydata = υποχώρηση[:current_year + 1]
        line.set_data(xdata, ydata)
        ax_anim.set_title(f"Προσομοίωση Διάβρωσης Παραλίας - Έτος: {current_year}")
    return line,

# Δημιουργία του animation
# Το interval είναι σε ms, οπότε 200ms = 0.2 δευτερόλεπτα ανά καρέ
anim = FuncAnimation(fig_anim, update, frames=range(χρόνια + 1), blit=True, interval=200, repeat=False)

# Αποθήκευση του animation ως αρχείο MP4
# Για να δουλέψει αυτό, χρειάζεστε το ffmpeg εγκατεστημένο στο σύστημα
# Επειδή το Streamlit Cloud δεν έχει πάντα προεγκατεστημένο το ffmpeg,
# είναι πιο ασφαλές να το εμφανίσουμε απευθείας ως βίντεο αν είναι δυνατό.
try:
    # Αν το Streamlit υποστηρίζει animation rendering απευθείας, θα το δείξει.
    # Διαφορετικά, μπορεί να χρειαστεί να αποθηκεύσουμε το animation και να το φορτώσουμε.
    # Για απλότητα, θα προσπαθήσουμε να το δείξουμε απευθείας μέσω st.pyplot
    # το οποίο μπορεί να το μετατρέψει σε GIF/MP4 αυτόματα.
    st.pyplot(fig_anim)
except Exception as e:
    st.warning(f"Δεν ήταν δυνατόν να προβληθεί το animation απευθείας. Παρακαλώ ελέγξτε τις ρυθμίσεις σας. ({e})")
    # Ως fallback, μπορούμε να δείξουμε το τελικό γράφημα
    fig_final, ax_final = plt.subplots()
    ax_final.plot(έτη, υποχώρηση, marker='o', color='teal')
    ax_final.set_xlabel("Έτη")
    ax_final.set_ylabel("Υποχώρηση Ακτής (m)")
    ax_final.set_title("Προσομοίωση Διάβρωσης Παραλίας (Τελικό Γράφημα)")
    ax_final.grid(True)
    st.pyplot(fig_final)


# Το αρχικό στατικό γράφημα θα μεταφερθεί μετά το animation ή θα παραλειφθεί
# Επειδή έχουμε animation, το στατικό γράφημα μπορεί να μην είναι απαραίτητο,
# εκτός αν θέλουμε να δείξουμε το τελικό αποτέλεσμα ξεκάθαρα.
# Για την ώρα, το αφήνω παρακάτω, αλλά μπορείτε να το αφαιρέσετε.

fig, ax = plt.subplots()
ax.plot(έτη, υποχώρηση, marker='o', color='teal')
ax.set_xlabel("Έτη")
ax.set_ylabel("Υποχώρηση Ακτής (m)")
ax.set_title("Προσομοίωση Διάβρωσης Παραλίας (Τελικό Γράφημα)") # Αλλάζω τον τίτλο για να ξεχωρίζει
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
