from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging as log
from db_models import *

router = APIRouter()


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




@router.get("/home")
async def read_data(n: int = 10):
    """ok"""
    return {"ok": "ok"}
