"""
Entidad de dominio para Sensor con reglas de negocio
"""

from typing import Optional

class Sensor:
    def __init__(self, id_sensor: int, nombre: str, id_tipo_sensor: int, id_ubicacion: int, id_usuario: int, activo: bool = True):
        self.id_sensor = id_sensor
        self.nombre = nombre
        self.id_tipo_sensor = id_tipo_sensor
        self.id_ubicacion = id_ubicacion
        self.id_usuario = id_usuario
        self.activo = activo

    def cambiar_nombre(self, nuevo_nombre: str):
        """Cambia el nombre del sensor"""
        if not nuevo_nombre or len(nuevo_nombre.strip()) < 3:
            raise ValueError("El nombre del sensor debe tener al menos 3 caracteres")
        self.nombre = nuevo_nombre.strip()

    def cambiar_tipo_sensor(self, nuevo_id_tipo_sensor: int):
        """Cambia el tipo de sensor"""
        if nuevo_id_tipo_sensor <= 0:
            raise ValueError("El ID del tipo de sensor debe ser un número positivo")
        self.id_tipo_sensor = nuevo_id_tipo_sensor

    def cambiar_ubicacion(self, nueva_id_ubicacion: int):
        """Cambia la ubicación del sensor"""
        if nueva_id_ubicacion <= 0:
            raise ValueError("El ID de la ubicación debe ser un número positivo")
        self.id_ubicacion = nueva_id_ubicacion

    def asignar_usuario(self, nuevo_id_usuario: int):
        """Asigna el sensor a un usuario diferente"""
        if nuevo_id_usuario <= 0:
            raise ValueError("El ID del usuario debe ser un número positivo")
        self.id_usuario = nuevo_id_usuario

    def activar(self):
        """Activa el sensor"""
        if self.activo:
            raise ValueError("El sensor ya está activo")
        self.activo = True

    def desactivar(self):
        """Desactiva el sensor"""
        if not self.activo:
            raise ValueError("El sensor ya está desactivado")
        self.activo = False

    def alternar_estado(self):
        """Alterna el estado activo/inactivo del sensor"""
        self.activo = not self.activo

    def esta_activo(self) -> bool:
        """Verifica si el sensor está activo"""
        return self.activo

    def puede_generar_lecturas(self) -> bool:
        """Determina si el sensor puede generar lecturas"""
        return self.activo and self.id_tipo_sensor > 0

    def validar_configuracion(self) -> bool:
        """Valida que el sensor esté correctamente configurado"""
        return (
            self.nombre and len(self.nombre.strip()) >= 3 and
            self.id_tipo_sensor > 0 and
            self.id_ubicacion > 0 and
            self.id_usuario > 0
        )

    def __repr__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"<Sensor id={self.id_sensor}, nombre='{self.nombre}', tipo={self.id_tipo_sensor}, ubicacion={self.id_ubicacion}, usuario={self.id_usuario}, estado={estado}>"
