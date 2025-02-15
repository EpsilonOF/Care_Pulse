import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF
import json

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
model_output_1 = '''
{
    "patient_name": "bvcbvc",
    "patient_gender": 1,
    "responses": {
        "1": [1, null, null, null, "Avez-vous des douleurs thoraciques ?"],
        "2": [1, 1, 5, "Pas du tout", "Sur une \\u00e9chelle de 1 \\u00e0 5, comment \\u00e9valueriez-vous votre niveau de douleur ?"],
        "3": [1, 1, 5, "Pas satisfait", "À quel point êtes-vous satisfait de votre traitement actuel ?"]
    }
}
'''

model_output_2 = '''
{
    "patient_name": "Alice",
    "patient_gender": 0,
    "responses": {
        "1": [0, null, null, null, "Avez-vous des douleurs thoraciques ?"],
        "2": [1, 1, 5, "Modéré", "Sur une \\u00e9chelle de 1 \\u00e0 5, comment \\u00e9valueriez-vous votre niveau de douleur ?"],
        "3": [1, 1, 5, "Satisfait", "À quel point êtes-vous satisfait de votre traitement actuel ?"]
    }
}
'''

# Conversion des chaînes JSON en dictionnaires Python
data1 = json.loads(model_output_1)
data2 = json.loads(model_output_2)
model_outputs = [data1, data2]

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
        st.header("Diagnostics du Modèle")
        # Menu déroulant pour sélectionner un patient parmi les outputs du modèle
        patient_names = [data["patient_name"] for data in model_outputs]
        selected_patient = st.selectbox("Sélectionnez un patient", patient_names)

        # Trouver et afficher le diagnostic du patient sélectionné dans un encart formaté
        for data in model_outputs:
            if data["patient_name"] == selected_patient:
                formatted_diagnostic = get_formatted_diagnostic(data)
                # Encadrer le diagnostic dans une "carte" de style similaire aux priorités
                st.markdown(
                    f"""
                    <div style="
                        background-color: #0066FF; 
                        color: white; 
                        padding: 10px; 
                        margin: 6px 0; 
                        border-radius: 10px; 
                        text-align: left;
                        font-size: 15px;
                    ">
                        <strong>Nom du patient :</strong> {data["patient_name"]}<br><br>
                        <strong>Réponses du questionnaire :</strong><br>
                        <pre style="white-space: pre-wrap; font-size: 14px;">{formatted_diagnostic}</pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                break

if __name__ == "__main__":
    main()
