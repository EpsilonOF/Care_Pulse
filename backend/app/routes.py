from fastapi import APIRouter
from .database import get_n_records

router = APIRouter()

@router.get("/data")
async def read_data(n: int = 10):
    """Lire les n premiers enregistrements de la base de données."""
    data = await get_n_records(n)
    return {"data": data}

@router.get("/home")
async def read_data(n: int = 10):
    """ok"""
    return {"ok": "ok"}
