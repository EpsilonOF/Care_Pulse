from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging as log
from typing import List, Literal, Optional
from db_models import *

router = APIRouter()

# Modèle Pydantic pour une question
class Question(BaseModel):
    id: int
    text: str
    response_type: Literal["boolean", "scale"]  # Type de réponse attendu
    range: Optional[List[int]] = None  # Intervalle pour les réponses de type "scale"

class PatientCreateRequest(BaseModel):
    nom: str

@router.post("/create/patient/")
async def create_patient(patient_request: PatientCreateRequest):
    patient = await Patient.create(nom=patient_request.nom)
    return patient.nom


@router.post("/create/docteur/")
async def create_docteur(docteur_request: PatientCreateRequest):
    docteur = await Docteur.create(nom=docteur_request.nom)
    return docteur.nom


# Liste de questions (simulée)
questions = [
    {"id": 1, "text": "Avez-vous des antécédents médicaux ?", "response_type": "boolean"},
    {"id": 2, "text": "Sur une échelle de 1 à 10, à quel point votre douleur est-elle intense ?", "response_type": "scale", "range": [1, 10]},
    {"id": 3, "text": "Avez-vous des allergies connues ?", "response_type": "boolean"},
    {"id": 4, "text": "Sur une échelle de 0 à 5, à quel point vous sentez-vous fatigué ?", "response_type": "scale", "range": [0, 5]},
    {"id": 5, "text": "Prenez-vous des médicaments actuellement ?", "response_type": "boolean"},
]

# Route GET /diagnostic
@router.get("/diagnostic", response_model=List[Question])
async def get_diagnostic_questions():
    """
    Renvoie une liste de questions pour le diagnostic.
    Chaque question inclut le type de réponse attendu (boolean ou scale).
    Pour les questions de type "scale", un intervalle (range) est également fourni.
    """
    question = questions
    return question



@router.get("/home")
async def read_data(n: int = 10):
    """ok"""
    return {"ok": "ok"}
