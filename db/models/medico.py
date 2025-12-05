from pydantic import BaseModel
from typing import Optional

class Medico(BaseModel):
    id: Optional[str] = None
    nombre: str
    apellidos: str
    ncolegiado: str
    especialidad: str
    