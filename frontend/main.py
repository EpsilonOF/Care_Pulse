import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Bienvenue", page_icon="🏥", layout="wide")

# Style CSS pour le fond bleu
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0066FF; /* Bleu Doctolib */
            color: white;
            text-align: center;
        }
        h1 {
            font-size: 3em;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre centré
st.markdown("<h1>🏥 Bienvenue sur Care Pulse</h1>", unsafe_allow_html=True)

<<<<<<< HEAD
# Styling for big choice buttons
button_style = """
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 120px;
    font-size: 24px;
    font-weight: bold;
    border-radius: 10px;
    margin: 10px 0;
"""

# Interface pour choisir (Grandes cases)
if st.button("👨‍⚕️ Médecin", key="doctor_btn", help="Accéder à l'interface médecin", use_container_width=True):
    st.session_state.role = "doctor"
    st.rerun()

if st.button("👤 Patient", key="patient_btn", help="Accéder à l'interface patient", use_container_width=True):
    st.session_state.role = "patient"
    st.rerun()

# Redirection automatique
if st.session_state.role == "doctor":
    st.session_state.role = None  # Reset the role to avoid multiple redirections
    st.switch_page("pages/doctor")  # Switch to the doctor page

elif st.session_state.role == "patient":
    st.session_state.role = None  # Reset the role
    st.switch_page("pages/patient")  # Switch to the patient page
=======
>>>>>>> refs/remotes/origin/main
