"""
Entidad de dominio para Rol con posibles reglas de negocio
"""

class Rol:
    def __init__(self, id_rol: int, nombre: str, descripcion: str):
        self.id_rol = id_rol
        self.nombre = nombre
        self.descripcion = descripcion

    def cambiar_nombre(self, nuevo_nombre: str):
        if not nuevo_nombre or len(nuevo_nombre.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        self.nombre = nuevo_nombre

    def actualizar_descripcion(self, nueva_desc: str):
        self.descripcion = nueva_desc.strip()

    def __repr__(self):
        return f"<Rol id={self.id_rol}, nombre='{self.nombre}'>"
