from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, HTTPException



router = APIRouter(prefix="/medicos"
                   , tags=["Médicos"])

class Medico(BaseModel):
    id: int
    nombre: str
    apellidos: str
    ncolegiado: str
    especialidad: str

medicos_list = [
    Medico(id=1, nombre="Juan", apellidos="Pérez", ncolegiado="12345", especialidad="Cardiología"),
    Medico(id=2, nombre="Ana", apellidos="García", ncolegiado="67890", especialidad="Dermatología"),
    Medico(id=3, nombre="Luis", apellidos="Martínez", ncolegiado="54321", especialidad="Pediatría"),
    Medico(id=4, nombre="Marta", apellidos="López", ncolegiado="98765", especialidad="Neurología"),
    Medico(id=5, nombre="Carlos", apellidos="Sánchez", ncolegiado="11223", especialidad="Oncología"),
    Medico(id=6, nombre="Laura", apellidos="Fernández", ncolegiado="44556", especialidad="Ginecología"),
    Medico(id=7, nombre="Javier", apellidos="Gómez", ncolegiado="77889", especialidad="Psiquiatría"),
    Medico(id=8, nombre="Sofía", apellidos="Ruiz", ncolegiado="99001", especialidad="Endocrinología"),
    Medico(id=9, nombre="Diego", apellidos="Torres", ncolegiado="22334", especialidad="Traumatología"),
    Medico(id=10, nombre="Elena", apellidos="Ramírez", ncolegiado="55667", especialidad="Oftalmología"),
    Medico(id=11, nombre="Miguel", apellidos="Vargas", ncolegiado="88990", especialidad="Cardiología"),
]
    

@router.get("/", response_class=HTMLResponse)
def root():
    return """
        <html>
            <head>
                <title>Médicos API</title>
            </head>
            <body>
                <h1>Bienvenido a la API de Médicos </h1>
                <p><a href="/medicos">Ver lista de médicos</a></p>
            </body>
        </html>
    """


@router.get("/")
def medicos():
    return medicos_list if medicos_list else {"mensaje": "No hay médicos disponibles"}

@router.get("/{medico_id}")
def medico(medico_id: int):
    return search_medico( medico_id)

@router.get("/query/") # Obtener un medico por su ID con query parameter
def medico(id: int):
    return search_medico(id)

@router.post("/", status_code=201, response_model=Medico) # Crear un nuevo medico
def create_medico(medico: Medico):
    medico.id=next_id()  # Asignar el siguiente ID disponible
    medicos_list.append(medico) 
    return medico

@router.put("/{id}", response_model=Medico) # Actualizar un medico existente
def update_medico(id: int, medico:Medico):
    for index, saved_medico in enumerate(medicos_list): # Recorro la lista con índice
        if saved_medico.id == id: # Si encuentro el medico a actualizar
            medico.id = id  # Le pongo el ID correcto
            medicos_list[index] = medico # Actualizo el medico en la lista
            return medico # Devuelvo el medico actualizado
    
    raise HTTPException(status_code=404, detail="Doctor not found") # Si no lo encuentro, lanzo excepción 404    

@router.delete("/{id}")
def delete_medico(id:int):
    for saved_medico in medicos_list:
        if saved_medico.id ==id:
            medicos_list.remove(saved_medico)
            return {}
    raise HTTPException(status_code=404, detail="Doctor not found")

##funciones auxiliares

def search_medico(id: int):
    medicos = [medico for medico in medicos_list if medico.id == id] 
    if not medicos: # Si la lista está vacía
        raise HTTPException(status_code=404, detail="Doctor not found") # Lanzar excepción 404
    
    return medicos[0]


def next_id():
    return max((m.id for m in medicos_list), default=0) + 1

                                            
    