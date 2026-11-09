# EJERCICIO 1
# Crea un endpoint GET /tareas/{tarea_id} que devuelva una sola tarea.
# Indicaciones:
#   1. Importa HTTPException: from fastapi import Depends, FastAPI, HTTPException
#   2. Decorador: @app.get("/tareas/{tarea_id}", response_model=schemas.TareaLeer)
#   3. Parámetros: tarea_id: int y db: sqlite3.Connection = Depends(get_db)
#   4. Consulta: db.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,)).fetchone()
#   5. fetchone() devuelve None si no hay resultado: en ese caso lanza
#      HTTPException(status_code=404, detail="Tarea no encontrada")
#   6. Si existe, devuelve dict(fila)
#   7. Prueba en /docs con un id que exista y con otro que no

import sqlite3

from fastapi import Depends, FastAPI

import schemas
from database import crear_tablas, get_connection

# Creamos las tablas si no existen
crear_tablas()

app = FastAPI()


# Creamos una dependencia para obtener la conexión a la base de datos
def get_db():
    db = get_connection()
    try:
        yield db
    finally:
        db.close()


@app.post("/tareas", response_model=schemas.TareaLeer, status_code=201)
def crear_tarea(datos: schemas.TareaCrear, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute("INSERT INTO tareas (titulo) VALUES (?)", (datos.titulo,))
    db.commit()
    fila = db.execute("SELECT * FROM tareas WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return dict(fila)

@app.get("/tareas", response_model=list[schemas.TareaLeer])
def listar_tareas(db: sqlite3.Connection = Depends(get_db)):
    filas = db.execute("SELECT * FROM tareas").fetchall()
    return [dict(f) for f in filas]

