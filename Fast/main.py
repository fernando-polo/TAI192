from fastapi import FastAPI, HTTPException
from typing import Optional, List
from pydantic import BaseModel


app = FastAPI(
    title="Mi primer API 192",
    description="Fernando Gómez, primeros pasos en fastAPI",
    version='1.0.1'
)

class modeloUsuario(BaseModel):
    id:int
    nombre:str
    edad:int
    correo: str

# BD ficticia
usuarios = [
        {"id":1, "nombre":"Fernando", "edad":22, "correo":"fernando@gmail.com"},
        {"id":2, "nombre":"Max", "edad":20, "correo":"max@gmail.com"},
        {"id":3, "nombre":"Baru", "edad":24, "correo":"baru@gmail.com"},
        {"id":4, "nombre":"Mariana", "edad":25, "correo":"mariana@gmail.com"},
]

#Endpoint home
@app.get('/', tags=['Hola mundo'])
def home():
    return {'hello':'world fastAPI'}

#Endpoint CONSULTA TODOS
@app.get('/todosUsuarios', response_model = List[modeloUsuario], tags=['Operaciones CRUD'])
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

# Endpoint - Modificar usuario
@app.put('/usuariosPut/{id}', tags=['Operaciones CRUD'])
def usuariosPut(id:int, usuarioActualizado:dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index].update(usuarioActualizado)
            return usuarios[index]
    raise HTTPException(status_code=400, detail="El id no existe")

# Endpoint - Eliminar usuario
@app.delete('/usuarioDelete/{id}', tags=['Operaciones CRUD'])
def usuariosDelete(id: int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index) 
            return {"message": "Usuario eliminado", "usuarios": usuarios}
    raise HTTPException(status_code=404, detail='Id no existente.')
    
