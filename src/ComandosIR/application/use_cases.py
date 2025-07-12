from typing import List
from src.ComandosIR.domain.schemas import ComandoIRCreate, ComandoIRUpdate, ComandoIRResponse
from src.ComandosIR.application.interfaces import ComandoIRRepositoryInterface


class ComandoIRUseCases:
    """Casos de uso para la entidad ComandoIR"""

    def __init__(self, repository: ComandoIRRepositoryInterface):
        self.repository = repository

    def listar_comandos_ir(self) -> List[ComandoIRResponse]:
        """Listar todos los comandos IR"""
        return self.repository.get_all()

    def obtener_comando_ir(self, id_comando: int) -> ComandoIRResponse:
        """Obtener un comando IR por ID"""
        return self.repository.get_by_id(id_comando)

    def obtener_comandos_por_sensor(self, id_sensor: int) -> List[ComandoIRResponse]:
        """Obtener todos los comandos IR de un sensor específico"""
        return self.repository.get_by_sensor(id_sensor)

    def crear_comando_ir(self, comando_ir: ComandoIRCreate) -> ComandoIRResponse:
        """Crear un nuevo comando IR"""
        return self.repository.create(comando_ir)

    def actualizar_comando_ir(self, id_comando: int, comando_ir: ComandoIRUpdate) -> ComandoIRResponse:
        """Actualizar un comando IR existente"""
        return self.repository.update(id_comando, comando_ir)

    def eliminar_comando_ir(self, id_comando: int) -> None:
        """Eliminar un comando IR"""
        self.repository.delete(id_comando)
