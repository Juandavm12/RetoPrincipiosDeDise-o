from typing import Set

from project.domain.solicitud import SolicitudReembolso
from project.domain.resultado_accion import ResultadoAccion
from project.enums.accion_solicitud import AccionSolicitud
from project.services.evaluador_solicitudes import EvaluadorSolicitudes
from project.services.ejecutor_acciones import EjecutorAcciones


# Fachada principal del sistema: expone las operaciones del motor de reglas
# Principios: SRP (solo coordina evaluacion y ejecucion de acciones),
# OCP (nuevos flujos se agregan sin modificar subsistemas internos),
# DIP (depende de abstracciones inyectadas: evaluador y ejecutor),
# Controller (punto de entrada que coordina el caso de uso),
# Low Coupling (el cliente solo conoce la fachada, no los subsistemas),
# KISS (API simple con pocos metodos publicos), YAGNI (sin metodos innecesarios)
class MotorReglasFacade:

    def __init__(
        self,
        evaluador: EvaluadorSolicitudes,
        ejecutor: EjecutorAcciones,
    ):
        self._evaluador = evaluador
        self._ejecutor = ejecutor

    def obtenerAccionesPermitidas(
        self, solicitud: SolicitudReembolso
    ) -> Set[AccionSolicitud]:
        """Retorna las acciones permitidas segun el estado actual de la solicitud."""
        return solicitud.estadoActual.accionesPermitidas()

    def ejecutarAccion(
        self, solicitud: SolicitudReembolso, accion: AccionSolicitud
    ) -> ResultadoAccion:
        """Ejecuta una accion sobre la solicitud, delegando al ejecutor."""
        # Si la accion es EVALUATE, primero evalua las reglas
        if accion == AccionSolicitud.EVALUATE:
            return self.evaluarSolicitud(solicitud)

        return self._ejecutor.ejecutar(solicitud, accion)

    def evaluarSolicitud(
        self, solicitud: SolicitudReembolso
    ) -> ResultadoAccion:
        """Evalua la solicitud ejecutando todas las reglas y almacena el resultado."""
        resultado = self._evaluador.evaluar(solicitud)
        solicitud.resultadoEvaluacion = resultado

        # Transicionar el estado (EVALUATE mantiene UNDER_REVIEW pero registra la evaluacion)
        resultado_accion = self._ejecutor.ejecutar(solicitud, AccionSolicitud.EVALUATE)
        if not resultado_accion.exitoso:
            return resultado_accion

        return ResultadoAccion(
            exitoso=True,
            mensaje=f"Evaluacion completada: {resultado.decision.value} ({len(resultado.hallazgos)} hallazgos)",
        )
