from typing import Optional

from project.domain.solicitud import SolicitudReembolso
from project.domain.hallazgo_regla import HallazgoRegla
from project.rules.regla_evaluacion import ReglaEvaluacion
from project.ports.clock import IClock


# Regla: valida que la fecha del evento no supere 60 dias respecto a la fecha actual
# Principios: SRP (solo valida ventana temporal), OCP (extensible sin modificar otras reglas),
# LSP (sustituible por ReglaEvaluacion), DIP (depende de IClock abstracto, no de datetime directo),
# Polymorphism, Low Coupling (usa puerto IClock), KISS
class ReglaVentanaTiempo(ReglaEvaluacion):

    DIAS_MAXIMOS = 60

    def __init__(self, clock: IClock):
        self._clock = clock

    def evaluar(self, solicitud: SolicitudReembolso) -> Optional[HallazgoRegla]:
        hoy = self._clock.today()
        diferencia = (hoy - solicitud.fechaEvento).days

        if diferencia > self.DIAS_MAXIMOS:
            return HallazgoRegla(
                regla="ReglaVentanaTiempo",
                descripcion=f"Han pasado {diferencia} dias desde el evento (maximo {self.DIAS_MAXIMOS})",
            )
        return None
