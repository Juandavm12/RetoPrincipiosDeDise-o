from __future__ import annotations

from typing import Set, TYPE_CHECKING

from project.enums.accion_solicitud import AccionSolicitud
from project.states.estado_solicitud import IEstadoSolicitud

if TYPE_CHECKING:
    from project.domain.solicitud import SolicitudReembolso


# Estado: la solicitud fue enviada y espera revision
# Principios: SRP (solo gestiona transiciones desde SUBMITTED),
# OCP (se agrego sin modificar otros estados), LSP (sustituible por IEstadoSolicitud),
# Polymorphism (implementa transiciones propias de este estado),
# Creator (crea el siguiente estado UnderReviewState), KISS, High Cohesion
class SubmittedState(IEstadoSolicitud):

    def nombre(self) -> str:
        return "SUBMITTED"

    def accionesPermitidas(self) -> Set[AccionSolicitud]:
        return {AccionSolicitud.START_REVIEW}

    def puedeEjecutar(self, accion: AccionSolicitud) -> bool:
        return accion in self.accionesPermitidas()

    def siguienteEstado(
        self, accion: AccionSolicitud, solicitud: SolicitudReembolso
    ) -> IEstadoSolicitud:
        if accion == AccionSolicitud.START_REVIEW:
            from project.states.under_review_state import UnderReviewState
            return UnderReviewState()
        raise ValueError(f"Accion {accion} no permitida en estado {self.nombre()}")
