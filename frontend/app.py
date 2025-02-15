import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests
from datetime import timedelta

# username = st.secrets["username"]
username = "felou"
# password = st.secrets["password"]

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
    st.title("Post-consultation")

    st.header("Votre ordonnance")
    st.write("Médicament : Aspirine")
    st.write("Dosage : 500mg")
    st.write("Fréquence : 2 fois par jour")

    st.header("Explications de prise de traitement")
    st.write("Prenez le médicament avec un verre d'eau.")


def chatbot_page():
    st.title("💬 Doctobot")
    st.caption("🚀 Détaillez votre cas, j'en ferai un rapport pour tenter de diminuer votre temps d'attente !")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Bonjour ! Comment puis-je vous aider ?"}]

    # Afficher l'historique de la conversation
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # mistral_api_key = st.secrets.get("mistral_api_key", "")
    
    if prompt := st.chat_input():
        # if not mistral_api_key:
        #     st.info("Please add your Mistral API key to continue.")
        #     st.stop()

        # Préparer les en-têtes pour l'appel API
#         headers = {
#             "Authorization": f"Bearer {mistral_api_key}",
#             "Content-Type": "application/json"
#         }

#         # Préparer les données pour l'appel API
#         data = {
#             "model": "mistral-model",  # Remplacez par le modèle approprié de Mistral
#             "messages": st.session_state.messages
#         }

        # Ajouter le message de l'utilisateur à l'historique
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Simuler une réponse automatique de l'assistant
        response_content = f"Merci pour votre message : '{prompt}'. Je suis là pour vous aider !"
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        st.chat_message("assistant").write(response_content)

#        Faire l'appel à l'API Mistral
        # response = requests.post(f"http://backend:8000/patients/{username}", headers=headers, json=data)
        # if response.status_code == 200:
        #     # Extraire et afficher la réponse de l'assistant
        #     msg = response.json()["choices"][0]["message"]["content"]
        #     st.session_state.messages.append({"role": "assistant", "content": msg})
        #     st.chat_message("assistant").write(msg)
        # else:
        #     st.error("Error in Mistral API request")


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

if __name__ == "__main__":
    main()
