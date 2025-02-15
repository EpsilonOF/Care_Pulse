import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests
from datetime import timedelta

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

def prise_de_rdv_page():
    st.title("Prendre un rendez-vous")

    date = st.date_input("Choisissez une date")
    heure = st.time_input("Choisissez une heure")

    # Calculer la date limite (1 mois à partir d'aujourd'hui)
    date_limite = datetime.date.today() + timedelta(days=30)

    if st.button("Vérifier la disponibilité"):
        # Logique pour vérifier la disponibilité
        if date > date_limite:
            st.write("Le délai de rendez-vous semble assez long. Si votre cas est critique, détaillez votre situation au chatbot pour essayer de diminuer l'attente de votre rendez-vous.")
        else:
            st.write("Rendez-vous disponible!")
            # Logique pour confirmer le rendez-vous

def post_consultation_page():
    st.title("Post-consultation")

    st.header("Votre ordonnance")
    st.write("Médicament : Aspirine")
    st.write("Dosage : 500mg")
    st.write("Fréquence : 2 fois par jour")

    st.header("Explications de prise de traitement")
    st.write("Prenez le médicament avec un verre d'eau.")

    st.header("FAQ")
    st.write("Q: Que faire en cas d'effets secondaires ?")
    st.write("R: Contactez immédiatement votre médecin.")

def chatbot_page():
    st.title("💬 Doctobot")
    st.caption("🚀 Détaillez votre cas, j'en ferai un rapport pour tenter de diminuer votre temps d'attente !")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Salam"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        mistral_api_key = st.secrets.get("mistral_api_key", "")  # Assurez-vous que votre clé API est configurée
        if not mistral_api_key:
            st.info("Please add your Mistral AI API key to continue.")
            st.stop()

        # Exemple d'appel à l'API Mistral AI
        headers = {
            "Authorization": f"Bearer {mistral_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-model",  # Remplacez par le modèle approprié
            "messages": st.session_state.messages
        }
        response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data)

        if response.status_code == 200:
            msg = response.json()["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)
        else:
            st.error("Error in Mistral AI API request")

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

def main():
    # Sidebar pour la navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("Accueil"):
        st.session_state.page = "home"
    if st.sidebar.button("Prendre un rendez-vous"):
        st.session_state.page = "prise_de_rdv"
    if st.sidebar.button("Post-consultation"):
        st.session_state.page = "post_consultation"
    if st.sidebar.button("Chatbot"):
        st.session_state.page = "chatbot"

    if 'page' not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "prise_de_rdv":
        prise_de_rdv_page()
    elif st.session_state.page == "post_consultation":
        post_consultation_page()
    elif st.session_state.page == "chatbot":
        chatbot_page()

if __name__ == "__main__":
    main()
