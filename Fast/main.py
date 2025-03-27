from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, List
from modelsPydantic import modeloUsuario, modeloAuth
from genToken import createToken
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from middlewares import BearerJWT
from DB.conexion import Session, engine, Base
from models.modelsDB import User



app = FastAPI(
    title="Mi primer API 192",
    description="Fernando Gómez, primeros pasos en fastAPI",
    version='1.0.1'
)


Base.metadata.create_all(bind = engine)


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



# Endpoint Autenticación
@app.post('/auth/', tags=['Autentificación'])
def login(autorización:modeloAuth):
    if autorización.email == 'fernando@example.com' and autorización.passw == '12345678':
        token:str = createToken(autorización.model_dump())
        print(token)
        return JSONResponse(content=token)
    else:
        return {"Aviso":"El usuario no está autorizado."}



#Endpoint Buscar un usuario por su ID
@app.get('/usuariosGetID/{id}',response_model=modeloUsuario,  tags=['Operaciones CRUD'])
def buscarUno(id: int):
    db=Session()
    try:
        consultauno = db.query(User).filter(User.id == id).first()

        if not consultauno:
            return JSONResponse(status_code=404, content={'message':'Usuario no encontrado.'})
        return JSONResponse(content=jsonable_encoder(consultauno))
    
    except Exception as e:
        return JSONResponse(status_code=500, 
                            content={'message':'Error al consultar usuario.', 
                                     'Excepción':str(e)})
    finally:
        db.close()



#Endpoint Consultar todos los usuarios
# @app.get('/todosUsuarios', dependencies=[Depends(BearerJWT())], response_model = List[modeloUsuario], tags=['Operaciones CRUD'])
@app.get('/usuariosGet',  response_model=modeloUsuario, tags=['Operaciones CRUD'])
def leerUsuarios():
    db=Session()
    try:
        consulta = db.query(User).all()
        return JSONResponse(content=jsonable_encoder(consulta))
    except Exception as e:
        return JSONResponse(status_code=500, 
                            content={'message':'Error al consultar usuarios.', 
                                     'Excepción':str(e)})
    finally:
        db.close()



# Endpoint - Agregar nuevos usuarios
@app.post('/usuariosPost/', response_model=modeloUsuario, tags = ['Operaciones CRUD'])
def agregarUsuario(usuario:modeloUsuario):
    db = Session()
    try:
        db.add(User(**usuario.model_dump()))
        db.commit()
        return JSONResponse(status_code=201, 
                            content={'message':'Usuario guardado.', 
                            'usuario':usuario.model_dump()  })
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, 
                            content={'message':'Error al guardar usuario.', 
                                     'Excepción':str(e)})
    finally:
        db.close()



# Endpoint - Actualizar usuario
@app.put('/usuariosPut/{id}',response_model=modeloUsuario,  tags=['Operaciones CRUD'])
def modificarUsuario(id: int, usuario:modeloUsuario):
    db=Session()
    try:
        consultauno = db.query(User).filter(User.id == id).first()

        if not consultauno:
            return JSONResponse(status_code=404, content={'message':'Usuario no encontrado.'})  
        
        for key, value in usuario.model_dump(exclude_unset=True).items():
            setattr(consultauno, key, value)    

        db.commit()
        db.refresh(consultauno)    
        return JSONResponse(content=jsonable_encoder(consultauno))
    
    except Exception as e:
        return JSONResponse(status_code=500, 
                            content={'message':'Error al consultar usuario.', 
                                     'Excepción':str(e)})
    finally:
        db.close()



# Endpoint - Eliminar usuario
@app.delete('/usuariosDelete/{id}',  tags=['Operaciones CRUD'])
def eliminarUsuario(id: int):
    db=Session()
    try:

        consultauno = db.query(User).filter(User.id == id).first()
        if not consultauno:
            return JSONResponse(status_code=404, content={'message':'Usuario no existente.'})
        
        db.delete(consultauno)  
        db.commit()

        consulta = db.query(User).all()

        return JSONResponse(content={'message':'Usuario eliminado correctamente', 'base de datos actual: ':jsonable_encoder(consulta) })
    
    except Exception as e:
        return JSONResponse(status_code=500, 
                            content={'message':'Error al encontrar al usuario.', 
                                     'Excepción':str(e)})
    finally:
        db.close()