from abc import ABC, abstractmethod
from typing import Optional

from project.domain.solicitud import SolicitudReembolso
from project.domain.hallazgo_regla import HallazgoRegla


# Interfaz para las reglas de evaluacion
# Principios: OCP (nuevas reglas se agregan sin modificar las existentes),
# LSP (toda regla concreta es sustituible por esta abstraccion),
# ISP (un solo metodo: evaluar), DIP (el evaluador depende de esta abstraccion),
# Polymorphism (cada regla concreta resuelve su propia validacion),
# DRY (contrato unico reutilizado por todas las reglas)
class ReglaEvaluacion(ABC):

    @abstractmethod
    def evaluar(self, solicitud: SolicitudReembolso) -> Optional[HallazgoRegla]:
        """Evalua la solicitud y retorna un hallazgo si hay un problema, o None si pasa."""
        pass
