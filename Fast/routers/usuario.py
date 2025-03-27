from fastapi import FastAPI, HTTPException, Depends
from modelsPydantic import modeloUsuario, modeloAuth
from genToken import createToken
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from middlewares import BearerJWT
from DB.conexion import Session
from models.modelsDB import User
from fastapi import APIRouter


routerUsuario = APIRouter()


#Endpoint Buscar un usuario por su ID
@routerUsuario.get('/usuariosGetID/{id}',response_model=modeloUsuario,  tags=['Operaciones CRUD'])
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
# @routerUsuario.get('/todosUsuarios', dependencies=[Depends(BearerJWT())], response_model = List[modeloUsuario], tags=['Operaciones CRUD'])
@routerUsuario.get('/usuariosGet',  response_model=modeloUsuario, tags=['Operaciones CRUD'])
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
@routerUsuario.post('/usuariosPost/', response_model=modeloUsuario, tags = ['Operaciones CRUD'])
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
@routerUsuario.put('/usuariosPut/{id}',response_model=modeloUsuario,  tags=['Operaciones CRUD'])
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
@routerUsuario.delete('/usuariosDelete/{id}',  tags=['Operaciones CRUD'])
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