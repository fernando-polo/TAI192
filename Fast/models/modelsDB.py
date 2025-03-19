from DB.conexion import Base

#Aquí declaramos los tipos de datos que estamos usando
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'tbUsers'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String)
    age = Column(Integer)
    email = Column(String)