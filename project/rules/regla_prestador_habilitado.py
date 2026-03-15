from typing import Optional

from project.domain.solicitud import SolicitudReembolso
from project.domain.hallazgo_regla import HallazgoRegla
from project.rules.regla_evaluacion import ReglaEvaluacion
from project.ports.prestador_catalog import IPrestadorHabilitadoCatalog


# Regla: consulta el puerto externo para validar que el prestador este habilitado
# Principios: SRP (solo valida habilitacion del prestador), OCP (extensible sin modificar otras),
# LSP (sustituible por ReglaEvaluacion), DIP (depende de IPrestadorHabilitadoCatalog abstracto),
# Polymorphism, Low Coupling (usa puerto abstracto, no servicio concreto), KISS
class ReglaPrestadorHabilitado(ReglaEvaluacion):

    def __init__(self, catalogo: IPrestadorHabilitadoCatalog):
        self._catalogo = catalogo

    def evaluar(self, solicitud: SolicitudReembolso) -> Optional[HallazgoRegla]:
        if not self._catalogo.estaHabilitado(solicitud.prestador.id):
            return HallazgoRegla(
                regla="ReglaPrestadorHabilitado",
                descripcion=f"El prestador '{solicitud.prestador.nombre}' no esta habilitado",
            )
        return None
