from modelsPydantic import  modeloAuth
from genToken import createToken
from fastapi.responses import JSONResponse
from middlewares import BearerJWT
from fastapi import APIRouter

routerAuth = APIRouter()


# Endpoint Autenticación
@routerAuth.post('/auth/', tags=['Autentificación'])
def login(autorización:modeloAuth):
    if autorización.email == 'fernando@example.com' and autorización.passw == '12345678':
        token:str = createToken(autorización.model_dump())
        print(token)
        return JSONResponse(content=token)
    else:
        return {"Aviso":"El usuario no está autorizado."}