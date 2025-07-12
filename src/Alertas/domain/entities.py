"""
Entidad de dominio para Alerta con posibles reglas de negocio
"""

from datetime import datetime
from typing import Optional

class Alerta:
    def __init__(self, id_alerta: int, id_lectura: int, tipo_alerta: str, descripcion: str, fecha_hora: Optional[datetime] = None):
        self.id_alerta = id_alerta
        self.id_lectura = id_lectura
        self.tipo_alerta = tipo_alerta
        self.descripcion = descripcion
        self.fecha_hora = fecha_hora or datetime.now()

    """ def cambiar_tipo_alerta(self, nuevo_tipo: str):
        tipos_validos = ["CRITICA", "ADVERTENCIA", "INFO", "ERROR", "MANTENIMIENTO"]
        if not nuevo_tipo or nuevo_tipo.strip().upper() not in tipos_validos:
            raise ValueError(f"El tipo de alerta debe ser uno de: {', '.join(tipos_validos)}")
        self.tipo_alerta = nuevo_tipo.strip().upper()
    """
    def actualizar_descripcion(self, nueva_desc: str):
        if not nueva_desc or len(nueva_desc.strip()) < 5:
            raise ValueError("La descripción debe tener al menos 5 caracteres.")
        self.descripcion = nueva_desc.strip()

    def asignar_lectura(self, nuevo_id_lectura: int):
        if nuevo_id_lectura <= 0:
            raise ValueError("El ID de la lectura debe ser un número positivo.")
        self.id_lectura = nuevo_id_lectura

    def es_critica(self) -> bool:
        """Determina si la alerta es crítica"""
        return self.tipo_alerta == "CRITICA"

    def es_reciente(self, minutos: int = 30) -> bool:
        """Determina si la alerta es reciente (dentro de los últimos X minutos)"""
        diferencia = datetime.now() - self.fecha_hora
        return diferencia.total_seconds() < (minutos * 60)

    def __repr__(self):
        return f"<Alerta id={self.id_alerta}, tipo='{self.tipo_alerta}', lectura={self.id_lectura}, fecha={self.fecha_hora}>"
