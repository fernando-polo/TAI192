from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI(
    title="Mi primer API 192",
    description="Fernando Gómez, primeros pasos en fastAPI",
    version='1.0.1'
)

usuarios = [
        {"id":1, "nombre":"Fernando", "edad":22},
        {"id":2, "nombre":"Max", "edad":20},
        {"id":3, "nombre":"Baru", "edad":24},
        {"id":4, "nombre":"Mariana", "edad":25},
]

#Endpoint home
@app.get('/', tags=['Hola mundo'])
def home():
    return {'hello':'world fastAPI'}

#Endpoint CONSULTA TODOS
@app.get('/todosUsuarios', tags=['Operaciones CRUD'])
def leerUsuarios():
    return {'Los usuarios registrados son: ': usuarios}

# Endpoint - Agregar nuevos usuarios
@app.post('/usuarios/', tags = ['Operaciones CRUD'])
def agregarUsuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(status_code=400, detail='Id ya existente.')
    usuarios.append(usuario)    
    return usuario

@app.put('/usuariosPut/{id}', tags=['Operaciones CRUD'])
def usuariosPut(id:int, usuarioActualizado:dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index].update(usuarioActualizado)
            return usuarios[index]
    raise HTTPException(status_code=400, detail="El id no existe")
