from fastapi import FastAPI, HTTPException, Depends
from DB.conexion import engine, Base
from routers.usuario import routerUsuario
from routers.auth import routerAuth



app = FastAPI(
    title="Mi primer API 192",
    description="Fernando Gómez, primeros pasos en fastAPI",
    version='1.0.1'
)



Base.metadata.create_all(bind = engine)



#Endpoint home
@app.get('/', tags=['Hola mundo'])
def home():
    return {'hello':'world fastAPI'}



app.include_router(routerAuth)
app.include_router(routerUsuario)
