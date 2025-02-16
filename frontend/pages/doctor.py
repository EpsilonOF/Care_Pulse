import logging
import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF
import json
import requests

# ===============================
# Fonctions existantes
# ===============================

def color_code(score):
    """Retourne la couleur en fonction du score."""
    if score >= 7:
        return "#FF4B4B"  # Rouge (Urgence)
    elif score >= 4:
        return "#FFA500"  # Orange (Modéré)
    else:
        return "#4CAF50"  # Vert (Stable)

def generate_pdf(patient_name, diagnosis):
    """Génère un PDF contenant le diagnostic du patient."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Diagnostic de {patient_name}", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, diagnosis)
    pdf_output = f"rapport_{patient_name}.pdf"
    pdf.output(pdf_output)
    return pdf_output



# ===============================
# Simulation des outputs JSON du modèle
# ===============================
FASTAPI_URL = "http://backend:8000/get_diagnostique/"

# Fonction pour récupérer les diagnostics depuis l'API
def get_diagnostics_from_api():
    response = requests.get(FASTAPI_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erreur lors de la récupération des diagnostics")
        return []

def format_response(response):
    """
    Formate la réponse d'une question :
    - Si les éléments aux index 1, 2 et 3 sont null, c'est une question oui/non.
    - Sinon, c'est une question sur une échelle et la réponse affichée est à l'index 3.
    """
    question_text = response[-1]  # Texte de la question (toujours à la fin)
    if response[1] is None and response[2] is None and response[3] is None:
        answer_str = "Oui\n" if response[0] == 1 else "Non\n"
    else:
        answer_str = response[3]
    return f"{question_text} : {answer_str}"

def get_formatted_diagnostic(data):
    """Construit une chaîne contenant toutes les réponses formatées pour un patient."""
    responses = data["responses"]
    lines = []
    for key, response in responses.items():
        lines.append(format_response(response))
    return "\n".join(lines)

# ===============================
# Interface Streamlit
# ===============================
def main():
    list_patient_score_dicts = []
    model_outputs = get_diagnostics_from_api()

    st.title("👨‍⚕️ Doctor Interface")

    tabs = st.tabs(["📋 Diagnostics du Modèle"])

    with tabs[0]:
        st.header("Diagnostics du Modèle")
        # Création d'une liste de patients pour le selectbox
        patient_list = [patient["patient_name"] for patient in model_outputs]

        # Sélecteur du patient
        selected_patient = st.selectbox("Choisissez un patient :", patient_list)

        # Recherche du patient sélectionné dans le modèle
        for data in model_outputs:
            if data["patient_name"] == selected_patient:
                # Affichage des caractéristiques principales
                st.subheader(f"Patient : {data['patient_name']}")
                gender = "Homme" if data["patient_gender"] == 1 else "Femme"
                st.write(f"Sexe du patient : {gender}")

                # Affichage des réponses
                st.write("### Réponses au questionnaire :")
                for question, response_info in data["responses"].items():
                    logging.error("DATA RESPONSES ITEMS : ", data["responses"].items())
                    # response_info est de la forme [?, ?, ?, ?, question_text]
                    question_text = question
                    # Par hypothèse, la valeur d'intérêt (note/réponse) est dans response_info[2]
                    note = response_info[0]

                    st.write(f"- **{question}** : {response_info[1]}")

                st.write(f"Compte-rendu : {data['contenu']}")
                break  # On arrête la boucle une fois le patient trouvé


if __name__ == "__main__":
    main()
