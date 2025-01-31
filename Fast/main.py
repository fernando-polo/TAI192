from fastapi import FastAPI
from typing import Optional

app = FastAPI(
    title="Mi primer API 192",
    description="Fernando Gómez, primeros pasos en fastAPI",
    version='1.0.1'
)

usuarios = [
        {'id':1, 'nombre':'Fernando', 'edad':22},
        {'id':2, 'nombre':'Baruch', 'edad':21},
        {'id':3, 'nombre':'Ivan', 'edad':20},
        {'id':4, 'nombre':'Max', 'edad':19}
]

#Endpoint home
@app.get('/', tags=['Hola mundo'])
def home():
    return {'hello':'world fastAPI'}

#Endpoint promedio
@app.get('/promedio', tags=['Mi calificación'])
def promedio():
    return 6.1

#Endpoint con parámetros OBLIGATORIOS
@app.get('/usuario/{id}', tags=['Parámetro obligatorio'])
def consultaUsuario(id:int):
    # Conectamos a la bd
    # Consultamos
    return {'Se encontró el usuario':id}

#Endpoint con parámetros OPCIONAL
@app.get('/usuario/', tags=['Parámetro opcional'])
def consultaUsuario(id: Optional[int] = None):
    if id is not None:
        for usu in usuarios:
            if usu["id"] == id:
                return {"mensaje" : "Usuario encontrado", "usuario": usu}
        return {"mensaje" : f"Usuario no encontrado {id}"}
    else:
        return{"mensaje" : "No se proporciono un id"}
    

#Endpoint con varios parametro opcionales
@app.get("/usuarios/", tags=["3 parámetros opcionales"])
async def consulta_usuarios(
    usuario_id: Optional[int] = None,
    nombre: Optional[str] = None,
    edad: Optional[int] = None
):
    resultados = []

    for usuario in usuarios:
        if (
            (usuario_id is None or usuario["id"] == usuario_id) and
            (nombre is None or usuario["nombre"].lower() == nombre.lower()) and
            (edad is None or usuario["edad"] == edad)
        ):
            resultados.append(usuario)

    if resultados:
        return {"usuarios_encontrados": resultados}
    else:
        return {"mensaje": "No se encontraron usuarios que coincidan con los parámetros proporcionados."}
