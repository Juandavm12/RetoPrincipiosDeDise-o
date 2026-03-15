from abc import ABC, abstractmethod

from project.enums.tipo_solicitud import TipoSolicitud
from project.policies.politica_tipo_solicitud import IPoliticaTipoSolicitud


# Puerto externo: obtiene la politica asociada a un tipo de solicitud
# Principios: DIP (las reglas dependen de esta abstraccion, no de logica de mapeo concreta),
# ISP (interfaz con un solo metodo), SRP (solo resuelve tipo -> politica),
# Low Coupling (desacopla reglas de la resolucion de politicas)
class ITipoSolicitudProvider(ABC):

    @abstractmethod
    def obtenerPor(self, tipo: TipoSolicitud) -> IPoliticaTipoSolicitud:
        """Retorna la politica correspondiente al tipo de solicitud."""
        pass
