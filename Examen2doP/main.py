from fastapi import FastAPI, HTTPException
from models import modeloUsuario

app = FastAPI()

app = FastAPI(
    title="EXAMEN",
    description="Fernando Gómez"
)

@app.get('/')
def home():
    return {'message':'hola mundo'}

conductores = [
        {"nombre":"Fernando", "tipo_licencia":"A", "No_Licencia":"AAAAAAAAAAAA"},
        {"nombre":"Baruch", "tipo_licencia":"A", "No_Licencia":"BBBBBBBBBBBB"},
        {"nombre":"José", "tipo_licencia":"A", "No_Licencia":"CCCCCCCCCCCC"},
        {"nombre":"Max", "tipo_licencia":"A", "No_Licencia":"DDDDDDDDDDDD"}
        ]

@app.get('/AllDrivers', tags=["EndPoints examen"])
def AllDrivers():
    return conductores

@app.put('/ChangeDriver/{No_Licencia}', response_model=modeloUsuario, tags=["EndPoints examen"])
def ChangeDriver(No_Licencia:str, usuarioActualizado:modeloUsuario,):
    for index, usr in enumerate(conductores):
        if usr["No_Licencia"] == No_Licencia:
            conductores[index]=usuarioActualizado.model_dump()
            return conductores[index]
    raise HTTPException(status_code=400, detail="El id no existe")

