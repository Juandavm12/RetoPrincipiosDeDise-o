from typing import Optional

from project.domain.solicitud import SolicitudReembolso
from project.domain.hallazgo_regla import HallazgoRegla
from project.rules.regla_evaluacion import ReglaEvaluacion


# Regla: valida la consistencia basica de los datos de la solicitud
# Principios: SRP (solo valida presencia de campos obligatorios),
# OCP (se agrego sin modificar otras reglas), LSP (sustituible por ReglaEvaluacion),
# Polymorphism (implementa evaluar de forma especifica),
# KISS (validaciones directas sin complejidad), High Cohesion
class ReglaConsistenciaDatos(ReglaEvaluacion):

    def evaluar(self, solicitud: SolicitudReembolso) -> Optional[HallazgoRegla]:
        errores = []

        if solicitud.valorSolicitado <= 0:
            errores.append("valor solicitado debe ser mayor a 0")
        if solicitud.paciente is None:
            errores.append("no existe paciente")
        if solicitud.prestador is None:
            errores.append("no existe prestador")
        if solicitud.tipoSolicitud is None:
            errores.append("no existe tipo de solicitud")

        if errores:
            return HallazgoRegla(
                regla="ReglaConsistenciaDatos",
                descripcion=f"Datos inconsistentes: {'; '.join(errores)}",
            )
        return None
