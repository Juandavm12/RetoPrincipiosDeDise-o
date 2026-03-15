from abc import ABC, abstractmethod
from datetime import date


# Puerto externo: abstraccion para obtener la fecha actual del sistema
# Principios: DIP (las reglas dependen de esta abstraccion, no de datetime directo),
# ISP (interfaz con un solo metodo, minima y especifica), SRP (solo provee la fecha),
# Low Coupling (desacopla el dominio de la infraestructura del reloj)
class IClock(ABC):

    @abstractmethod
    def today(self) -> date:
        """Retorna la fecha actual del sistema."""
        pass
