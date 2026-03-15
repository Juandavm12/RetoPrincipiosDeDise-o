from abc import ABC, abstractmethod


# Puerto externo: consulta si un prestador esta habilitado
# Principios: DIP (las reglas dependen de esta abstraccion, no de un servicio concreto),
# ISP (interfaz con un solo metodo), SRP (solo consulta habilitacion),
# Low Coupling (desacopla dominio de la fuente de datos externa)
class IPrestadorHabilitadoCatalog(ABC):

    @abstractmethod
    def estaHabilitado(self, idPrestador: str) -> bool:
        """Verifica si el prestador con el id dado esta habilitado."""
        pass
