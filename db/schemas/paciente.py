def paciente_schema(paciente) -> dict:
    return {
        "id": str(paciente["_id"]),
        "dni": paciente["dni"],
        "apellidos": paciente["apellidos"],
        "nombre": paciente["nombre"]
    }

def pacientes_schema(pacientes) -> list:
    return [paciente_schema(paciente) for paciente in pacientes]