from fastapi import FastAPI
from routers import medicos, pacientes, auth_users
from fastapi.staticfiles import StaticFiles
from routers import medicos_db

app = FastAPI()

#Routers
app.include_router(medicos.router)
app.include_router(medicos_db.router)
app.include_router(pacientes.router)
app.include_router(auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical API"}