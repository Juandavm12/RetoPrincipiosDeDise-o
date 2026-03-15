from project.domain.solicitud import SolicitudReembolso
from project.domain.resultado_accion import ResultadoAccion
from project.enums.accion_solicitud import AccionSolicitud


# Servicio responsable de validar acciones permitidas y cambiar el estado de la solicitud
# Principios: SRP (solo gestiona transiciones de estado),
# OCP (nuevos estados se agregan sin modificar este servicio),
# DIP (depende de la abstraccion IEstadoSolicitud, no de estados concretos),
# Low Coupling (delega la logica de transicion al propio estado),
# Polymorphism (el estado actual decide el siguiente via polimorfismo)
class EjecutorAcciones:

    def ejecutar(
        self, solicitud: SolicitudReembolso, accion: AccionSolicitud
    ) -> ResultadoAccion:
        """Valida que la accion sea permitida y transiciona al siguiente estado."""
        estado_actual = solicitud.estadoActual

        if not estado_actual.puedeEjecutar(accion):
            return ResultadoAccion(
                exitoso=False,
                mensaje=f"Accion {accion.value} no permitida en estado {estado_actual.nombre()}",
            )

        try:
            nuevo_estado = estado_actual.siguienteEstado(accion, solicitud)
            solicitud.estadoActual = nuevo_estado
            return ResultadoAccion(
                exitoso=True,
                mensaje=f"Transicion exitosa: {estado_actual.nombre()} -> {nuevo_estado.nombre()}",
            )
        except ValueError as e:
            return ResultadoAccion(exitoso=False, mensaje=str(e))
