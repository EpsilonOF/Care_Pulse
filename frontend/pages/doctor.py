import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF

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
        return "#FF4B4B"  # Rouge
    elif score >= 4:
        return "#FFA500"  # Orange
    else:
        return "#4CAF50"  # Vert

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

def main():
    st.title("👨‍⚕️ Doctor Interface")
    
    tabs = st.tabs(["📋 Priorité des Patients", "📝 Diagnostic & PDF"])
    
    with tabs[0]:  # Onglet Priorité des Patients
        st.header("Liste des patients classés par priorité")
        df = generate_priority_list()
        
        for _, row in df.iterrows():
            color = color_code(row['Score'])
            patient_name = row["Nom"]
            file_name = f"rapport_{patient_name}.pdf"
            
            # Affichage en HTML + CSS
            st.markdown(
                f"""
                <div style="
                    display: flex; 
                    justify-content: space-between; 
                    align-items: center; 
                    background-color: {color}; 
                    padding: 12px; 
                    border-radius: 8px; 
                    margin-bottom: 10px;
                    color: white;
                    font-weight: bold;
                ">
                    <span style="margin-left: 10px;">{patient_name} - Score: {row['Score']:.2f}</span>
                    <a href="{file_name}" download="{file_name}">
                        <button style="
                            background-color: white;
                            color: black;
                            border: none;
                            padding: 6px 10px;
                            border-radius: 5px;
                            cursor: pointer;
                            font-weight: bold;">
                            📥
                        </button>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

    with tabs[1]:  # Onglet Diagnostic & PDF
        st.header("📝 Rédiger un diagnostic")
        patient_name = st.selectbox("Sélectionnez un patient", ["Alice", "Bob", "Charlie", "David", "Emma"])
        diagnosis_text = st.text_area("Écrivez le diagnostic ici")
        
        if st.button("📄 Générer et Envoyer PDF"):
            pdf_file = generate_pdf(patient_name, diagnosis_text)
            with open(pdf_file, "rb") as file:
                st.download_button(label="📥 Télécharger le PDF", data=file, file_name=pdf_file, mime="application/pdf")
            st.success(f"📄 PDF généré et envoyé pour {patient_name} !")

if __name__ == "__main__":
    main()
