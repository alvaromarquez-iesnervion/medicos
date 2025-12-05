from datetime import date
from pydantic import BaseModel
from typing import Optional

class Paciente(BaseModel):
    id: Optional[str] = None
    dni: str
    apellidos: str
    nombre: str
    seg_social: str
    f_nacimiento: date
    id_medico: int