"""
Entidad de dominio para Ubicacion con posibles reglas de negocio
"""

class Ubicacion:
    def __init__(self, id_ubicacion: int, nombre: str, descripcion: str):
        self.id_ubicacion = id_ubicacion
        self.nombre = nombre
        self.descripcion = descripcion

    def cambiar_nombre(self, nuevo_nombre: str):
        if not nuevo_nombre or len(nuevo_nombre.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        self.nombre = nuevo_nombre

    def actualizar_descripcion(self, nueva_desc: str):
        self.descripcion = nueva_desc.strip()

    def __repr__(self):
        return f"<Ubicacion id={self.id_ubicacion}, nombre='{self.nombre}'>"
