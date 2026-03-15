from __future__ import annotations

from typing import Set, TYPE_CHECKING

from project.enums.accion_solicitud import AccionSolicitud
from project.enums.decision_evaluacion import DecisionEvaluacion
from project.states.estado_solicitud import IEstadoSolicitud

if TYPE_CHECKING:
    from project.domain.solicitud import SolicitudReembolso


# Estado: la solicitud esta en revision, permite evaluar, aprobar o rechazar
# Principios: SRP (solo gestiona transiciones desde UNDER_REVIEW),
# OCP (se agrego sin modificar otros estados), LSP (sustituible por IEstadoSolicitud),
# Polymorphism (implementa transiciones propias de este estado),
# Creator (crea ApprovedState o RejectedState segun decision),
# KISS (logica clara con validaciones directas), High Cohesion
class UnderReviewState(IEstadoSolicitud):

    def nombre(self) -> str:
        return "UNDER_REVIEW"

    def accionesPermitidas(self) -> Set[AccionSolicitud]:
        return {AccionSolicitud.EVALUATE, AccionSolicitud.APPROVE, AccionSolicitud.REJECT}

    def puedeEjecutar(self, accion: AccionSolicitud) -> bool:
        return accion in self.accionesPermitidas()

    def siguienteEstado(
        self, accion: AccionSolicitud, solicitud: SolicitudReembolso
    ) -> IEstadoSolicitud:
        if accion == AccionSolicitud.EVALUATE:
            # EVALUATE no cambia de estado, solo ejecuta las reglas
            return self

        if accion == AccionSolicitud.APPROVE:
            # Solo se puede aprobar si la evaluacion resulto APROBABLE
            if (
                solicitud.resultadoEvaluacion is not None
                and solicitud.resultadoEvaluacion.decision == DecisionEvaluacion.APROBABLE
            ):
                from project.states.approved_state import ApprovedState
                return ApprovedState()
            raise ValueError("No se puede aprobar: la evaluacion no es APROBABLE")

        if accion == AccionSolicitud.REJECT:
            # Solo se puede rechazar si la evaluacion resulto RECHAZABLE
            if (
                solicitud.resultadoEvaluacion is not None
                and solicitud.resultadoEvaluacion.decision == DecisionEvaluacion.RECHAZABLE
            ):
                from project.states.rejected_state import RejectedState
                return RejectedState()
            raise ValueError("No se puede rechazar: la evaluacion no es RECHAZABLE")

        raise ValueError(f"Accion {accion} no permitida en estado {self.nombre()}")
