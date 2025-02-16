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
# Coefficients pour le calcul des scores
# ===============================

def sum_domain_scores(response_dict):

    sum_physical_limitations = sum([int(response_dict[str(i)][0]) for i in [1, 2, 3]])
    sum_symptom_frequency = sum([int(response_dict[str(i)][0]) for i in [5, 6]])
    sum_symptom_burden = sum([int(response_dict[str(i)][0]) for i in [4, 7]])
    sum_quality_of_life = sum([int(response_dict[str(i)][0]) for i in [8, 9]])
    sum_social_limitations = sum([int(response_dict[str(i)][0]) for i in [10, 11, 12]])

    return [sum_physical_limitations, sum_symptom_frequency, sum_symptom_burden, sum_quality_of_life, sum_social_limitations]


def calculate_transformed_score(sum_of_items, min_possible_sum, max_possible_sum):
    """
    Calculate the transformed score on a 0-100 scale.

    Parameters:
    sum_of_items (int): The sum of the item scores for the domain.
    min_possible_sum (int): The minimum possible sum for the domain.
    max_possible_sum (int): The maximum possible sum for the domain.

    Returns:
    float: The transformed score on a 0-100 scale.
    """
    if sum_of_items < min_possible_sum or sum_of_items > max_possible_sum:
        raise ValueError("Sum of items is out of the possible range.")

    transformed_score = ((sum_of_items - min_possible_sum) /
                         (max_possible_sum - min_possible_sum)) * 100
    return transformed_score


def calculate_total_score(patient_dict):
    """
    Calculate the total score across all domains.

    Parameters:
    physical_limitations_sum (int): Sum of scores for Physical Limitations items.
    symptom_frequency_sum (int): Sum of scores for Symptom Frequency items.
    symptom_burden_sum (int): Sum of scores for Symptom Burden items.
    quality_of_life_sum (int): Sum of scores for Quality of Life items.
    social_limitations_sum (int): Sum of scores for Social Limitations items.

    Returns:
    dict: patient name and overall summary score
    """
    physical_limitations_sum, symptom_frequency_sum, symptom_burden_sum, quality_of_life_sum, social_limitations_sum = sum_domain_scores(patient_dict["response"])
    min_max_values = {
        'physical_limitations': (3, 18),
        'symptom_frequency': (2, 14),
        'symptom_burden': (2, 10),
        'quality_of_life': (2, 10),
        'social_limitations': (3, 18)
    }
    patient_name = patient_dict["patient_name"]
    # Calculate transformed scores for each domain
    transformed_scores = {
        'physical_limitations': calculate_transformed_score(physical_limitations_sum, *min_max_values['physical_limitations']),
        'symptom_frequency': calculate_transformed_score(symptom_frequency_sum, *min_max_values['symptom_frequency']),
        'symptom_burden': calculate_transformed_score(symptom_burden_sum, *min_max_values['symptom_burden']),
        'quality_of_life': calculate_transformed_score(quality_of_life_sum, *min_max_values['quality_of_life']),
        'social_limitations': calculate_transformed_score(social_limitations_sum, *min_max_values['social_limitations'])
    }

    # Calculate the overall summary score
    overall_summary_score = sum(transformed_scores.values()) / len(transformed_scores)
    return {"patient_name": patient_name, "overall_summary_score": overall_summary_score}


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

    st.title("👨‍⚕️ Doctor Interface")

    tabs = st.tabs(["📋 Priorité des Patients", "📝 Diagnostic & PDF", "📄 Diagnostics du Modèle"])

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

                st.write(f"Compte-rendu : {data['contenu']}")
                break  # On arrête la boucle une fois le patient trouvé


if __name__ == "__main__":
    main()