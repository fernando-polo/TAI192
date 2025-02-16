from fastapi import FastAPI, HTTPException
from typing import Optional


app = FastAPI(
    title="To-do-List",
    description="API - Lista de Tareas",
    version="1.0"
)

tareas = [{
            "id": 1,
            "titulo": "Estudiar para el examen",
            "descripcion": "Repasar los apuntes de TAI ",
            "vencimiento": "14-02-24",
            "Estado": "completada"
          },
          {
            "id": 2,
            "titulo": "Hacer chatbot de PONS",
            "descripcion": "Creación de chatbot",
            "vencimiento": "14-02-24",
            "Estado": "completada"
          },
          {
            "id": 3,
            "titulo": "Repartir vistas de TAI",
            "descripcion": "Repartir entre todos los integrantes del equipo las vistas",
            "vencimiento": "14-02-24",
            "Estado": "completada"
          },
          {
            "id": 4,
            "titulo": "Repartir vistas de Diseño de software",
            "descripcion": "Repartir entre todos los integrantes del equipo las vistas ",
            "vencimiento": "14-02-24",
            "Estado": "completada"
          },

]

# Endpoint - Inicio
@app.get("/")
def home():
    return {"message":"hola mundo"}


# Endpoint - Obtener todas las tareas
@app.get("/tarea", tags=["Endpoints Principales"])
def todas_las_tareas():
    return tareas


# Endpoint - Obtener una tarea específica por su ID
@app.get("/obtenerTarea/{id}", tags=["Endpoints Principales"])
def obtener_tarea(id:int):
    for index, tar in enumerate(tareas):
        if tar["id"] == id:
            return tareas[index]
    raise HTTPException(status_code=400, detail="Id no existe.")


# Endpoint - Crear nueva tarea
@app.post("/tareaNueva/", tags=["Endpoints Principales"])
def crear_nueva_tarea(tarea:dict):
    for tar in tareas:
        # if tar["id"] == tarea.get("id"):
        if tar["id"] == tarea["id"]:
          raise HTTPException(status_code=400, detail="Id ya existente.")
    tareas.append(tarea)
    return tarea


# Endpoint - Actualizar una tarea existente
@app.put("/editarTarea/{id}", tags = ["Endpoints Principales"])
def editar_tarea(id:int, tareaU: dict):
    for index, tar in enumerate(tareas):
        if tar["id"] == id:
            tareas[index].update(tareaU)
            return tareas[index]
    raise HTTPException(status_code=400, detail="El id no existe")


# Endpoint - Eliminar una tarea
@app.delete("/tareaEliminar/{id}", tags=["Endpoints Principales"])
def eliminar_tarea(id:int):
    for index, tar in enumerate(tareas):
        if tar["id"] == id:
            tareas.pop(index)
            return {'message':'Se eliminó exitosamente la tarea', 'tareas existentes: ':tareas}
    raise HTTPException(status_code=400, detail="El id no existe")       
