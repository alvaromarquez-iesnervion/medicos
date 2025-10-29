from datetime import date
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, HTTPException



router = APIRouter(prefix="/pacientes"
                   , tags=["Pacientes"])


class Paciente(BaseModel):
    id: int
    dni: str
    apellidos: str
    nombre: str
    seg_social: str
    f_nacimiento: date
    id_medico: int


pacientes_list = [
    Paciente(id=1, dni="12345678A", apellidos="Gómez Pérez", nombre="Lucía", seg_social="123456789012", f_nacimiento="1990-04-15", id_medico=1),
    Paciente(id=2, dni="23456789B", apellidos="Ruiz Fernández", nombre="Daniel", seg_social="234567890123", f_nacimiento="1985-09-22", id_medico=2),
    Paciente(id=3, dni="34567890C", apellidos="Martín López", nombre="Sofía", seg_social="345678901234", f_nacimiento="2002-12-10", id_medico=3),
    Paciente(id=4, dni="45678901D", apellidos="Serrano Torres", nombre="Javier", seg_social="456789012345", f_nacimiento="1978-03-03", id_medico=4),
    Paciente(id=5, dni="56789012E", apellidos="Castro Gómez", nombre="Elena", seg_social="567890123456", f_nacimiento="1969-07-28", id_medico=5),
    Paciente(id=6, dni="67890123F", apellidos="Moreno Ruiz", nombre="Raúl", seg_social="678901234567", f_nacimiento="1995-01-12", id_medico=6),
    Paciente(id=7, dni="78901234G", apellidos="Vega Martínez", nombre="Carmen", seg_social="789012345678", f_nacimiento="1988-06-09", id_medico=7),
    Paciente(id=8, dni="89012345H", apellidos="Navarro Pérez", nombre="Andrés", seg_social="890123456789", f_nacimiento="1975-11-17", id_medico=8),
    Paciente(id=9, dni="90123456J", apellidos="Campos García", nombre="Marina", seg_social="901234567890", f_nacimiento="1993-05-02", id_medico=9),
    Paciente(id=10, dni="01234567K", apellidos="Jiménez Vargas", nombre="Óscar", seg_social="012345678901", f_nacimiento="1981-10-26", id_medico=10),
]


@router.get("/")
def pacientes():
    return pacientes_list if pacientes_list else {"mensaje": "No hay pacientes disponibles"}

@router.get("/{id}")
def paciente(id:int):
    return search_paciente(id)

@router.get("/query/") # Obtener un paciente por su ID con query parameter
def paciente(id: int):
    return search_paciente(id)

@router.post("/", status_code=201, response_model=Paciente) # Crear un nuevo paciente
def create_paciente(paciente: Paciente):
    paciente.id=next_id()  # Asignar el siguiente ID disponible
    pacientes_list.append(paciente) 
    return paciente

@router.put("/{id}", response_model=Paciente) # Actualizar un paciente existente
def update_paciente(id: int, paciente:Paciente):
    for index, saved_paciente in enumerate(pacientes_list): # Recorro la lista con índice
        if saved_paciente.id == id: # Si encuentro el paciente a actualizar
            paciente.id = id  # Le pongo el ID correcto
            pacientes_list[index] = paciente # Actualizo el paciente en la lista
            return paciente # Devuelvo el paciente actualizado
    
    raise HTTPException(status_code=404, detail="Patient not found") # Si no lo encuentro, lanzo excepción 404    

@router.delete("/{id}")
def delete_paciente(id:int):
    for saved_paciente in pacientes_list:
        if saved_paciente.id ==id:
            pacientes_list.remove(saved_paciente)
            return {}
    raise HTTPException(status_code=404, detail="Patient not found")


def search_paciente(id: int):
    pacientes = [paciente for paciente in pacientes_list if paciente.id == id] 
    if not pacientes: # Si la lista está vacía
        raise HTTPException(status_code=404, detail="Patient not found") # Lanzar excepción 404

    return pacientes[0]


def next_id() -> int:
    return max((p.id for p in pacientes_list), default=0) + 1
                                            
