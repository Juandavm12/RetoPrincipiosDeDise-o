from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Set, TYPE_CHECKING

from project.enums.accion_solicitud import AccionSolicitud

if TYPE_CHECKING:
    from project.domain.solicitud import SolicitudReembolso


# Interfaz: define el comportamiento de cada estado de la solicitud
# Principios: OCP (nuevos estados se agregan implementando esta interfaz sin modificar los existentes),
# LSP (todo estado concreto es sustituible por esta abstraccion),
# ISP (interfaz cohesiva con solo metodos de estado), DIP (servicios dependen de esta abstraccion),
# Polymorphism (cada estado resuelve sus transiciones polimorficamente),
# High Cohesion, DRY (contrato unico reutilizado por todos los estados)
class IEstadoSolicitud(ABC):

    @abstractmethod
    def nombre(self) -> str:
        """Retorna el nombre del estado."""
        pass

    @abstractmethod
    def accionesPermitidas(self) -> Set[AccionSolicitud]:
        """Retorna el conjunto de acciones permitidas en este estado."""
        pass

    @abstractmethod
    def puedeEjecutar(self, accion: AccionSolicitud) -> bool:
        """Verifica si una accion puede ejecutarse en este estado."""
        pass

    @abstractmethod
    def siguienteEstado(
        self, accion: AccionSolicitud, solicitud: SolicitudReembolso
    ) -> IEstadoSolicitud:
        """Retorna el siguiente estado tras ejecutar la accion dada."""
        pass
