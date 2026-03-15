from __future__ import annotations

from typing import Set, TYPE_CHECKING

from project.enums.accion_solicitud import AccionSolicitud
from project.states.estado_solicitud import IEstadoSolicitud

if TYPE_CHECKING:
    from project.domain.solicitud import SolicitudReembolso


# Estado final: la solicitud fue rechazada (no permite mas acciones)
# Principios: SRP (solo representa el estado terminal rechazado),
# OCP (se agrego sin modificar otros estados), LSP (sustituible por IEstadoSolicitud),
# Polymorphism (implementa el contrato sin transiciones),
# KISS (estado terminal sin logica compleja), YAGNI (sin metodos extra), High Cohesion
class RejectedState(IEstadoSolicitud):

    def nombre(self) -> str:
        return "REJECTED"

    def accionesPermitidas(self) -> Set[AccionSolicitud]:
        return set()

    def puedeEjecutar(self, accion: AccionSolicitud) -> bool:
        return False

    def siguienteEstado(
        self, accion: AccionSolicitud, solicitud: SolicitudReembolso
    ) -> IEstadoSolicitud:
        raise ValueError(f"No hay transiciones desde el estado {self.nombre()}")
