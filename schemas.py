from pydantic import BaseModel


# Es lo que se envia a la API para crear una tarea
class TareaCrear(BaseModel):
    titulo: str


# Lo que la API debe devolver al cliente cuando se crea o se lee una tarea
class TareaLeer(BaseModel):
    id: int
    titulo: str
    completada: bool
