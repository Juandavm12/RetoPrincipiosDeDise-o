from typing import Optional

from project.domain.solicitud import SolicitudReembolso
from project.domain.hallazgo_regla import HallazgoRegla
from project.rules.regla_evaluacion import ReglaEvaluacion
from project.ports.tipo_solicitud_provider import ITipoSolicitudProvider


# Regla: valida que el valor solicitado no supere el monto maximo de la politica
# Principios: SRP (solo valida monto maximo), OCP (extensible sin modificar otras reglas),
# LSP (sustituible por ReglaEvaluacion), DIP (depende de ITipoSolicitudProvider, no de concretas),
# Polymorphism, Low Coupling (usa puerto para obtener la politica)
class ReglaMontoMaximo(ReglaEvaluacion):

    def __init__(self, provider: ITipoSolicitudProvider):
        self._provider = provider

    def evaluar(self, solicitud: SolicitudReembolso) -> Optional[HallazgoRegla]:
        politica = self._provider.obtenerPor(solicitud.tipoSolicitud)
        monto_maximo = politica.obtenerMontoMaximo()

        if solicitud.valorSolicitado > monto_maximo:
            return HallazgoRegla(
                regla="ReglaMontoMaximo",
                descripcion=f"Valor solicitado ({solicitud.valorSolicitado}) supera el maximo ({monto_maximo})",
            )
        return None
