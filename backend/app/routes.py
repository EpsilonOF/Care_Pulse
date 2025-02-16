from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
import logging as log
from typing import List, Literal, Optional
from db_models import *
from enter_model import *
from tortoise.query_utils import Prefetch
from tortoise.exceptions import DoesNotExist
from ds import take_question
from diago import interview_summup
from score import *

router = APIRouter()

@router.post("/create/patient/")
async def create_patient(patient_request: PatientCreateRequest):
    patient = await Patient.create(nom=patient_request.nom)
    return patient.nom


@router.post("/create/docteur/")
async def create_docteur(docteur_request: PatientCreateRequest):
    docteur = await Docteur.create(nom=docteur_request.nom)
    return docteur.nom



# Route GET /diagnostic
@router.get("/diagnostic", response_model=List[Question]) # envoyer les question au frontend
async def get_diagnostic_questions():
    """
    Renvoie une liste de questions pour le diagnostic.
    Chaque question inclut le type de réponse attendu (boolean ou scale).
    Pour les questions de type "scale", un intervalle (range) est également fourni.
    """
    question = take_question(questions)
    return question

def get_score(file):
    return calculate_total_score(file)

@router.post("/recup-diagnostic/", status_code=status.HTTP_200_OK)
async def create_diagnostic(data: DiagnosticData):
    log.error(f"Received diagnostic data: {data}")
    try:
        patient = await Patient.get(nom=data.patient_name)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Transformation des réponses
    responses = {}
    for key, value in data.responses.items():
        # Split the string into a list of values
        response_values = value.split(", ")
        # Convert the first three values to integers
        response_values[:3] = [int(v) for v in response_values[:3]]
        # Add the response to the responses dictionary
        responses[int(key)] = response_values

    # Création du dictionnaire file
    file = {
        "patient_name": data.patient_name,
        "patient_gender": "male" if data.patient_gender == 1 else "female" if data.patient_gender == 2 else "other",
        "responses": responses
    }

    # Appel de la fonction interview_summup avec les bonnes entrées
    res = interview_summup(get_score(file), file)

    diagnostic = await Diagnostic.create(
        contenu={"responses": res},
        questions=questions,
        patient=patient,
        genre=data.patient_gender,
        responses=responses
    )

    return {"message": "Diagnostic recorded successfully"}



class DiagnosticResponse(BaseModel):
    patient_name: str
    patient_gender: int
    responses: dict
    contenu: str

@router.get("/get_diagnostique/", response_model=List[DiagnosticResponse])
async def get_diagnostics():
    diagnostics = await Diagnostic.all().prefetch_related(
        Prefetch("patient", queryset=Patient.all().only("id", "nom"))
    )

    response = []
    for diagnostic in diagnostics:
        responses = {}
        for key, value in diagnostic.responses.items():
            # Convertir la chaîne en liste
            # Extraire le premier élément et le convertir en entier
            first_element = int(value[0])
            # Ajouter au dictionnaire salut
            responses[value[4]] = [str(first_element),value[3]]
        response.append({
            "patient_name": diagnostic.patient.nom,
            "patient_gender": diagnostic.genre,
            "responses": responses,
            "contenu": diagnostic.contenu["responses"]
        })

    return response

@router.get("/home")
async def read_data(n: int = 10):
    """ok"""
    return {"ok": "ok"}
