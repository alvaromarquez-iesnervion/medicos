from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from routers.auth_users import authentication
from db.client import db_client
from db.schemas.paciente import paciente_schema, pacientes_schema
from db.models.paciente import Paciente

from bson import ObjectId

router = APIRouter( 
    prefix="/pacientesdb",
    tags=["pacientesdb"]
)

@router.get("/", response_model=list[Paciente])
async def pacientes_db():
    return pacientes_schema(db_client.test.pacientes.find())

@router.get("", response_model=Paciente)
async def paciente_query(id: str):
    return search_paciente_id(id)

@router.get("/{paciente_id}", response_model=Paciente)
async def paciente_db(paciente_id: str):
    return search_paciente_id(paciente_id)

@router.post("/", response_model=Paciente, status_code=201)
async def add_paciente(paciente: Paciente):
    # Verificar si el paciente ya existe por DNI
    if type(search_paciente_by_dni(paciente.dni)) == Paciente:
        raise HTTPException(status_code=409, detail="Paciente ya existe")
    
    paciente_dict = paciente.model_dump()
    del paciente_dict["id"]
    
    id = db_client.test.pacientes.insert_one(paciente_dict).inserted_id
    paciente_dict["id"] = str(id)
    
    return Paciente(**paciente_dict)

@router.put("/{id}", response_model=Paciente)
async def modify_paciente(id: str, new_paciente: Paciente):
    paciente_dict = new_paciente.model_dump()
    del paciente_dict["id"]   
    try:
        db_client.test.pacientes.find_one_and_replace({"_id": ObjectId(id)}, paciente_dict)
        return search_paciente_id(id)    
    except:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

@router.delete("/{id}", response_model=Paciente)
async def delete_paciente(id: str):
    found = db_client.test.pacientes.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return Paciente(**paciente_schema(found))

## Funciones auxiliares

def search_paciente_id(id: str):    
    try:
        paciente = paciente_schema(db_client.test.pacientes.find_one({"_id": ObjectId(id)}))
        return Paciente(**paciente)
    except:
        return {"error": "Paciente no encontrado"}

def search_paciente_by_dni(dni: str):
    try:
        paciente = paciente_schema(db_client.test.pacientes.find_one({"dni": dni}))
        return Paciente(**paciente)
    except:
        return {"error": "Paciente no encontrado"}