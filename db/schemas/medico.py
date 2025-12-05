def medico_schema(medico) -> dict:
    return {
        "id": str(medico["_id"]),
        "nombre": medico["nombre"],
        "apellidos": medico["apellidos"],
        "ncolegiado": medico["ncolegiado"],
        "especialidad": medico["especialidad"]  
    }

def medicos_schema(medicos) -> list:
    return [medico_schema(medico) for medico in medicos]