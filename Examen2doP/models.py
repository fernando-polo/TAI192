from pydantic import BaseModel, Field

class modeloUsuario(BaseModel):
    nombre:str = Field(...,min_length=3, description="Nombre con mínimo de 3 letras.")
    tipo_licencia:str = Field(...,min_length=1, max_length=1, description="Licencia de sólo un carácter.")
    No_Licencia:str = Field(...,min_length=12, max_length=12, description="Número de licencia de 12 caracteres.")