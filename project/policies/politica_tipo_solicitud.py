from abc import ABC, abstractmethod
from typing import List, Set

from project.enums.tipo_solicitud import TipoSolicitud


# Interfaz que define la politica asociada a un tipo de solicitud
# Principios: OCP (nuevas politicas se agregan sin modificar las existentes),
# LSP (toda subclase es sustituible por esta interfaz), ISP (interfaz minima y cohesiva),
# DIP (las reglas dependen de esta abstraccion, no de concretas),
# Polymorphism (GRASP: cada tipo resuelve su propia politica)
class IPoliticaTipoSolicitud(ABC):

    @abstractmethod
    def obtenerTipo(self) -> TipoSolicitud:
        """Retorna el tipo de solicitud que maneja esta politica."""
        pass

    @abstractmethod
    def obtenerDocumentosObligatorios(self) -> List[str]:
        """Retorna la lista de tipos de documentos obligatorios."""
        pass

    @abstractmethod
    def obtenerMontoMaximo(self) -> float:
        """Retorna el monto maximo permitido para este tipo de solicitud."""
        pass
