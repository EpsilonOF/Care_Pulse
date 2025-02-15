import streamlit as st
import pandas as pd
import requests
import json

# username = st.secrets["username"]
username = "felou"
# password = st.secrets["password"]

# Adding custom CSS directly to the page for text color adjustments
st.markdown(
    """
    <style>
        /* General styling for the app */
        .stApp {
            background: linear-gradient(to bottom, rgb(37, 150, 190), #0066FF); /* Gradient background */
        }
    </style>
    """, unsafe_allow_html=True
)

def home_page():
    st.title("Bienvenue sur notre plateforme médicale")
    st.header("Votre historique médical")

    # Exemple d'historique médical (à remplacer par des données réelles)
    historique = [
        {"date": "2023-01-01", "description": "Consultation pour douleur thoracique"},
        {"date": "2023-05-15", "description": "Suivi post-opératoire"},
    ]

    for entry in historique:
        st.write(f"**{entry['date']}**: {entry['description']}")

def post_consultation_page():
    st.write("Bienvenue sur votre espace personnel. Ici, vous pouvez consulter vos rapports médicaux.")

    st.header("📂 Vos documents médicaux")
    sample_reports = ["rapport_Alice.pdf"]

    for report in sample_reports:
        with open(report, "rb") as file:
            st.download_button(label=f"📥 Télécharger {report}", data=file, file_name=report, mime="application/pdf", key="download_btn", use_container_width=True)

    st.title("Post-consultation")

    st.header("Votre ordonnance")
    st.write("Médicament : Aspirine")
    st.write("Dosage : 500mg")
    st.write("Fréquence : 2 fois par jour")

    st.header("Explications de prise de traitement")
    st.write("Prenez le médicament avec un verre d'eau.")

def load_questions(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def save_responses(file_path, responses):
    with open(file_path, 'w') as file:
        json.dump(responses, file, indent=4)

questions = [
    {"id":1,"text": "Avez-vous des douleurs thoraciques ?", "type": "boolean"},
    {"id":2,"text": "Sur une échelle de 1 à 5, comment évalueriez-vous votre niveau de douleur ?", "type": "scale", "range": 5},
    {"id":3,"text": "À quel point êtes-vous satisfait de votre traitement actuel ?", "type": "scale", "range": 10}
]

def chatbot_page():
    st.title("📋 Questionnaire Médical")
    st.caption("Répondez aux questions suivantes pour aider votre médecin à mieux comprendre votre situation.")

    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0

    if "responses" not in st.session_state:
        st.session_state.responses = []

    patient_name = st.text_input("Nom du patient", key="patient_name")
    patient_gender = st.selectbox("Genre du patient", ["","Homme", "Femme", "Autre"], key="patient_gender")

    # Afficher l'historique des réponses
    for i, (question, response) in enumerate(zip(questions, st.session_state.responses)):
        st.write(f"**Question {i+1}**: {question['text']}")
        st.write(f"**Réponse**: {response}")

    # Poser la question actuelle
    if st.session_state.current_question_index < len(questions):
        current_question = questions[st.session_state.current_question_index]
        st.write(f"**Question {st.session_state.current_question_index + 1}**: {current_question['text']}")

        if current_question["type"] == "boolean":
            response = st.radio("Votre réponse", ["Vrai", "Faux"], key=f"question_{st.session_state.current_question_index}")
        elif current_question["type"] == "scale":
            response = st.slider("Votre réponse", 1, current_question["range"], key=f"question_{st.session_state.current_question_index}")

        if st.button("Continuer"):
            if response:
                st.session_state.responses.append(response)
                st.session_state.current_question_index += 1
                st.query_params = {"page": "questionnaire", "index": st.session_state.current_question_index}
                st.rerun()
    elif patient_name == "":
        st.warning("Veuillez entrer un nom pour continuer.")
    elif patient_gender == "":
        st.warning("Veuillez sélectionner un genre pour continuer.")
    else:
        st.write("Merci d'avoir répondu à toutes les questions. Vos réponses ont été transférées à un médecin.")
        structured_responses = {
            "patient_name": patient_name,
            "patient_gender": patient_gender,
            "responses": {question["id"]: response for question, response in zip(questions, st.session_state.responses)}
        }
        save_responses('responses.json', structured_responses)

def generate_pdf():
    # Fonction pour générer un PDF (exemple basique)
    pdf_content = "Voici votre rapport médical"
    return pdf_content

def send_pdf(pdf_content):
    # Fonction pour envoyer le PDF (ici simulée)
    st.write("PDF généré et envoyé avec succès.")

def main():
    # Sidebar pour la navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("Accueil"):
        st.session_state.page = "home"
    if st.sidebar.button("Post-consultation"):
        st.session_state.page = "post_consultation"
    if st.sidebar.button("Chatbot"):
        st.session_state.page = "chatbot"

    if 'page' not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "post_consultation":
        post_consultation_page()
    elif st.session_state.page == "chatbot":
        chatbot_page()
        
    # Boutons pour générer et envoyer le PDF
    pdf_content = generate_pdf()
    
    if st.button("Générer et envoyer le PDF", key="generate_pdf", help="Générer un rapport médical en PDF", use_container_width=True):
        send_pdf(pdf_content)

if __name__ == "__main__":
    main()
