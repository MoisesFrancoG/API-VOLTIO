"""
Entidad de dominio para TipoSensor con posibles reglas de negocio
"""

class TipoSensor:
    def __init__(self, id_tipo_sensor: int, nombre: str, descripcion: str):
        self.id_tipo_sensor = id_tipo_sensor
        self.nombre = nombre
        self.descripcion = descripcion

    def cambiar_nombre(self, nuevo_nombre: str):
        if not nuevo_nombre or len(nuevo_nombre.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        self.nombre = nuevo_nombre

    def actualizar_descripcion(self, nueva_desc: str):
        self.descripcion = nueva_desc.strip()

    def __repr__(self):
        return f"<TipoSensor id={self.id_tipo_sensor}, nombre='{self.nombre}'>"
