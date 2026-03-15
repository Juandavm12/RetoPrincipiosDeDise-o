from __future__ import annotations

from typing import Set, TYPE_CHECKING

from project.enums.accion_solicitud import AccionSolicitud
from project.states.estado_solicitud import IEstadoSolicitud

if TYPE_CHECKING:
    from project.domain.solicitud import SolicitudReembolso


# Estado inicial: la solicitud esta en borrador
# Principios: SRP (solo gestiona transiciones desde DRAFT),
# OCP (se agrego sin modificar otros estados), LSP (sustituible por IEstadoSolicitud),
# Polymorphism (implementa transiciones propias de este estado),
# Creator (crea el siguiente estado SubmittedState),High Cohesion
class DraftState(IEstadoSolicitud):

    def nombre(self) -> str:
        return "DRAFT"

    def accionesPermitidas(self) -> Set[AccionSolicitud]:
        return {AccionSolicitud.SUBMIT}

    def puedeEjecutar(self, accion: AccionSolicitud) -> bool:
        return accion in self.accionesPermitidas()

    def siguienteEstado(
        self, accion: AccionSolicitud, solicitud: SolicitudReembolso
    ) -> IEstadoSolicitud:
        if accion == AccionSolicitud.SUBMIT:
            from project.states.submitted_state import SubmittedState
            return SubmittedState()
        raise ValueError(f"Accion {accion} no permitida en estado {self.nombre()}")
