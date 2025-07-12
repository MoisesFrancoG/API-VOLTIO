from typing import List
from src.Alertas.domain.schemas import AlertaCreate, AlertaUpdate, AlertaResponse
from src.Alertas.application.interfaces import AlertaRepositoryInterface


class AlertaUseCases:
    """Casos de uso para la entidad Alerta"""

    def __init__(self, repository: AlertaRepositoryInterface):
        self.repository = repository

    def listar_alertas(self) -> List[AlertaResponse]:
        """Listar todas las alertas"""
        return self.repository.get_all()

    def obtener_alerta(self, id_alerta: int) -> AlertaResponse:
        """Obtener una alerta por ID"""
        return self.repository.get_by_id(id_alerta)

    def obtener_alertas_por_lectura(self, id_lectura: int) -> List[AlertaResponse]:
        """Obtener todas las alertas de una lectura específica"""
        return self.repository.get_by_lectura(id_lectura)

    def obtener_alertas_por_tipo(self, tipo_alerta: str) -> List[AlertaResponse]:
        """Obtener todas las alertas de un tipo específico"""
        return self.repository.get_by_tipo(tipo_alerta)

    def obtener_alertas_criticas(self) -> List[AlertaResponse]:
        """Obtener todas las alertas críticas"""
        return self.repository.get_criticas()

    def obtener_alertas_recientes(self, horas: int = 24) -> List[AlertaResponse]:
        """Obtener alertas recientes (últimas X horas)"""
        return self.repository.get_recientes(horas)

    def crear_alerta(self, alerta: AlertaCreate) -> AlertaResponse:
        """Crear una nueva alerta"""
        return self.repository.create(alerta)

    def actualizar_alerta(self, id_alerta: int, alerta: AlertaUpdate) -> AlertaResponse:
        """Actualizar una alerta existente"""
        return self.repository.update(id_alerta, alerta)

    def eliminar_alerta(self, id_alerta: int) -> None:
        """Eliminar una alerta"""
        self.repository.delete(id_alerta)

    def generar_reporte_alertas_criticas(self) -> dict:
        """Generar un reporte de alertas críticas"""
        alertas_criticas = self.obtener_alertas_criticas()
        alertas_recientes = self.obtener_alertas_recientes(24)
        
        criticas_recientes = [
            alerta for alerta in alertas_criticas 
            if alerta.id_alerta in [a.id_alerta for a in alertas_recientes]
        ]
        
        return {
            "total_criticas": len(alertas_criticas),
            "criticas_recientes_24h": len(criticas_recientes),
            "alertas_criticas": alertas_criticas,
            "alertas_recientes": criticas_recientes
        }
