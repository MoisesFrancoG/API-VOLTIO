"""
Entidad de dominio para Lectura con posibles reglas de negocio
"""

from datetime import datetime
from typing import Optional

class Lectura:
    def __init__(self, id_lectura: int, id_sensor: int, valor: float, unidad: str, fecha_hora: Optional[datetime] = None):
        self.id_lectura = id_lectura
        self.id_sensor = id_sensor
        self.valor = valor
        self.unidad = unidad
        self.fecha_hora = fecha_hora or datetime.now()

    def actualizar_valor(self, nuevo_valor: float):
        """Actualiza el valor de la lectura"""
        if nuevo_valor < 0:
            raise ValueError("El valor no puede ser negativo.")
        self.valor = nuevo_valor

    def cambiar_unidad(self, nueva_unidad: str):
        """Cambia la unidad de medida"""
        unidades_validas = ["°C", "°F", "V", "A", "W", "kW", "kWh", "%", "ppm", "bar", "Pa", "m/s", "Hz"]
        if not nueva_unidad or nueva_unidad.strip() not in unidades_validas:
            raise ValueError(f"La unidad debe ser una de: {', '.join(unidades_validas)}")
        self.unidad = nueva_unidad.strip()

    def asignar_sensor(self, nuevo_id_sensor: int):
        """Asigna la lectura a un sensor diferente"""
        if nuevo_id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo.")
        self.id_sensor = nuevo_id_sensor

    def es_valor_critico(self, limite_superior: float = 100.0, limite_inferior: float = 0.0) -> bool:
        """Determina si el valor está fuera de los límites normales"""
        return self.valor > limite_superior or self.valor < limite_inferior

    def es_lectura_reciente(self, minutos: int = 30) -> bool:
        """Determina si la lectura es reciente (dentro de los últimos X minutos)"""
        diferencia = datetime.now() - self.fecha_hora
        return diferencia.total_seconds() < (minutos * 60)

    def convertir_temperatura(self, unidad_destino: str) -> float:
        """Convierte temperatura entre Celsius y Fahrenheit"""
        if self.unidad == "°C" and unidad_destino == "°F":
            return (self.valor * 9/5) + 32
        elif self.unidad == "°F" and unidad_destino == "°C":
            return (self.valor - 32) * 5/9
        elif self.unidad == unidad_destino:
            return self.valor
        else:
            raise ValueError("Conversión no soportada entre estas unidades")

    def __repr__(self):
        return f"<Lectura id={self.id_lectura}, sensor={self.id_sensor}, valor={self.valor}{self.unidad}, fecha={self.fecha_hora}>"
