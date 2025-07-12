"""
Entidad de dominio para ComandoIR con posibles reglas de negocio
"""

class ComandoIR:
    def __init__(self, id_comando: int, id_sensor: int, nombre: str, descripcion: str, comando: str):
        self.id_comando = id_comando
        self.id_sensor = id_sensor
        self.nombre = nombre
        self.descripcion = descripcion
        self.comando = comando

    def cambiar_nombre(self, nuevo_nombre: str):
        if not nuevo_nombre or len(nuevo_nombre.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        self.nombre = nuevo_nombre

    def actualizar_descripcion(self, nueva_desc: str):
        self.descripcion = nueva_desc.strip()

    def actualizar_comando(self, nuevo_comando: str):
        if not nuevo_comando or len(nuevo_comando.strip()) < 1:
            raise ValueError("El comando no puede estar vacío.")
        self.comando = nuevo_comando.strip()

    def asignar_sensor(self, nuevo_id_sensor: int):
        if nuevo_id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo.")
        self.id_sensor = nuevo_id_sensor

    def __repr__(self):
        return f"<ComandoIR id={self.id_comando}, nombre='{self.nombre}', sensor={self.id_sensor}>"
