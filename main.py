from fastapi import FastAPI
from routers import medicos, pacientes
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(medicos.router)
app.include_router(pacientes.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical API"}