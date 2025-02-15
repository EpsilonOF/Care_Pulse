from typing import List, Literal, Optional, Dict
from pydantic import BaseModel, Field



# Liste de questions (simulée)
questions = [
    {"id": 1, "text": "Avez-vous des antécédents médicaux ?", "response_type": "boolean"},
    {"id": 2, "text": "Sur une échelle de 1 à 10, à quel point votre douleur est-elle intense ?", "response_type": "scale", "range": [1, 10]},
    {"id": 3, "text": "Avez-vous des allergies connues ?", "response_type": "boolean"},
    {"id": 4, "text": "Sur une échelle de 0 à 5, à quel point vous sentez-vous fatigué ?", "response_type": "scale", "range": [0, 5]},
    {"id": 5, "text": "Prenez-vous des médicaments actuellement ?", "response_type": "boolean"},
]
# Modèle Pydantic pour une question
class Question(BaseModel):
    id: int
    text: str
    response_type: Literal["boolean", "scale"]  # Type de réponse attendu
    range: Optional[List[int]] = None  # Intervalle pour les réponses de type "scale"

class PatientCreateRequest(BaseModel):
    nom: str



class DiagnosticData(BaseModel):
    patient_name: str = Field(..., example="Felou")
    patient_gender: str = Field(..., example="Homme")
    responses: Dict[str, str] = Field(..., example={"1": "Vrai", "2": "2", "3": "4"})


class DiagnosticResponse(BaseModel):
    id: int
    genre: str
    contenu: Dict[str, str]
    questions: Dict[str, str]
    patient_name: str

    class Config:
        orm_mode = True
