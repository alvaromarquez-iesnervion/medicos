from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from routers.auth_users import authentication
from db.client import db_client
from db.schemas.medico import medico_schema, medicos_schema
from db.models.medico import Medico

from bson import ObjectId

router = APIRouter( 
    prefix="/medicosdb",
    tags=["medicosdb"]
)

@router.get("/", response_model=list[Medico])
async def medicos_db():
    # Igual que users_db pero con medicos_schema
    return medicos_schema(db_client.test.medicos.find())

@router.get("", response_model=Medico)
async def medico_query(id: str):
    # Igual que users_db
    return search_medico_id(id)

@router.get("/{medico_id}", response_model=Medico)
async def medico_db(medico_id: str):
    # Igual que users_db
    return search_medico_id(medico_id)

@router.post("/", response_model=Medico, status_code=201)
async def add_medico(medico: Medico):
    # ADAPTADO: usar ncolegiado en lugar de name+surname
    if type(search_medico_by_ncolegiado(medico.ncolegiado)) == Medico:
        raise HTTPException(status_code=409, detail="Médico ya existe")
    
    medico_dict = medico.model_dump()
    del medico_dict["id"]
    
    # CORREGIDO: usar 'medicos' (con s) consistentemente
    id = db_client.test.medicos.insert_one(medico_dict).inserted_id
    medico_dict["id"] = str(id)
    
    return Medico(**medico_dict)

@router.put("/{id}", response_model=Medico)
async def modify_medico(id: str, new_medico: Medico):
    # Igual que users_db
    medico_dict = new_medico.model_dump()
    del medico_dict["id"]   
    try:
        db_client.test.medicos.find_one_and_replace({"_id": ObjectId(id)}, medico_dict)
        return search_medico_id(id)    
    except:
        raise HTTPException(status_code=404, detail="Médico no encontrado")

@router.delete("/{id}", response_model=Medico)
async def delete_medico(id: str):
    # Igual que users_db
    found = db_client.test.medicos.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return Medico(**medico_schema(found))

## Funciones auxiliares

def search_medico_id(id: str):    
    # Igual que search_user_id
    try:
        medico = medico_schema(db_client.test.medicos.find_one({"_id": ObjectId(id)}))
        return Medico(**medico)
    except:
        return {"error": "Médico no encontrado"}

# ADAPTADO: buscar por ncolegiado (campo único del médico)
def search_medico_by_ncolegiado(ncolegiado: str):
    try:
        medico = medico_schema(db_client.test.medicos.find_one({"ncolegiado": ncolegiado}))
        return Medico(**medico)
    except:
        return {"error": "Médico no encontrado"}