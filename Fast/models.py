from pydantic import BaseModel, Field, EmailStr

class modeloUsuario(BaseModel):
    id:int = Field(...,gt=0, description="Id único y sólo números positivos.")
    nombre:str = Field(...,min_length=3, max_length=85, description="Nombre con mínimo de 3 letras y máximo a 85.")
    edad:int = Field(..., ge=1, le=120)
    correo:EmailStr = Field(..., examples=["Usuario23@gmail.com"])