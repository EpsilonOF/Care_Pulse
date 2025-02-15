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
def generate_priority_list():
    """Génération de données fictives pour les scores des patients."""
    np.random.seed(42)
    patients = ["Alice", "Bob", "Charlie", "David", "Emma"]
    scores = np.random.uniform(0, 10, len(patients))
    df = pd.DataFrame({"Nom": patients, "Score": scores})
    df = df.sort_values(by="Score", ascending=False)
    return df

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

def calculate_health_score(response_list, scores_to_coefs):
    sum_responses = [sum(response_list[i:i+5]) for i in range(0, 25, 5)]
    return max(0, min(10, 10 * (1 - sum([scores_to_coefs[score-1][i] for i, score in enumerate(sum_responses)]))))

# ===============================
# Coefficients pour le calcul des scores
# ===============================
score_to_coefs_MO = [0, 0.03759, 0.04774, 0.17949, 0.32509]
score_to_coefs_SC = [0, 0.03656, 0.050781, 0.172251, 0.258331]
score_to_coefs_UA = [0, 0.03313, 0.03979, 0.15689, 0.24005]
score_to_coefs_PD = [0, 0.02198, 0.04704, 0.26374, 0.44399]
score_to_coefs_AD = [0, 0.02046, 0.04683, 0.20005, 0.25803]

scores_to_coefs = np.array(list(zip(score_to_coefs_MO, score_to_coefs_SC, score_to_coefs_UA, score_to_coefs_PD, score_to_coefs_AD)))

# ===============================
# Simulation des données pour les autres onglets
# ===============================
patients_list = ["Alice", "Bob", "Charlie", "Diana", "Ethan"]
patient_responses = {name: np.random.randint(0, 2, 25).tolist() for name in patients_list}
patient_scores = {name: calculate_health_score(responses, scores_to_coefs) for name, responses in patient_responses.items()}
sorted_patients = sorted(patient_scores.items(), key=lambda x: x[1], reverse=True)

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
    st.title("👨‍⚕️ Doctor Interface")

    tabs = st.tabs(["📋 Priorité des Patients", "📝 Diagnostic & PDF", "📄 Diagnostics du Modèle"])

    # Onglet 1 : Priorité des Patients
    with tabs[0]:
        st.header("Liste des patients classés par priorité")
        for name, score in sorted_patients:
            diagnosis = f"Compte-rendu médical de {name}.\nÉtat du patient analysé avec un score de {score:.2f}/10."
            color = color_code(score)
            st.markdown(
                f"""
                <div style="
                    background-color: {color};
                    color: white;
                    padding: 6px;
                    margin: 6px 0;
                    border-radius: 10px;
                    text-align: center;
                    font-size: 15px;
                    font-weight: bold;
                ">
                    {name} : Score = {score:.2f}
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.expander(f"📋 Voir le compte-rendu de {name}"):
                st.write(diagnosis)
                pdf_file = generate_pdf(name, diagnosis)
                with open(pdf_file, "rb") as file:
                    st.download_button(label="📥 Télécharger le PDF", data=file, file_name=pdf_file, mime="application/pdf")

    # Onglet 2 : Rédiger un diagnostic
    with tabs[1]:
        st.header("📝 Rédiger un diagnostic")
        patient_name = st.selectbox("Sélectionnez un patient", patients_list)
        diagnosis_text = st.text_area("Écrivez le diagnostic ici")

        if st.button("📄 Générer et Envoyer PDF"):
            pdf_file = generate_pdf(patient_name, diagnosis_text)
            with open(pdf_file, "rb") as file:
                st.download_button(label="📥 Télécharger le PDF", data=file, file_name=pdf_file, mime="application/pdf")
            st.success(f"📄 PDF généré et envoyé pour {patient_name} !")

    # Onglet 3 : Diagnostics du Modèle
    with tabs[2]:
        # requete request pour avoir les data
        model_outputs = get_diagnostics_from_api()
        logging.error("okokokokokokok  :", model_outputs)
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
                for question_id, response_info in data["responses"].items():
                    # response_info est de la forme [?, ?, ?, ?, question_text]
                    question_text = response_info[4]
                    # Par hypothèse, la valeur d'intérêt (note/réponse) est dans response_info[2]
                    note = response_info[2]

                    st.write(f"- **Question {question_id}** : {question_text}")
                    if note is not None:
                        st.write(f"  Réponse : {note}")
                    else:
                        st.write("  Réponse : Non renseigné")

                break  # On arrête la boucle une fois le patient trouvé


if __name__ == "__main__":
    main()
