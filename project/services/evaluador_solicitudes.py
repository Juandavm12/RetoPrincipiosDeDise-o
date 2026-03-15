from typing import List

from project.domain.solicitud import SolicitudReembolso
from project.domain.hallazgo_regla import HallazgoRegla
from project.domain.resultado_evaluacion import ResultadoEvaluacion
from project.enums.decision_evaluacion import DecisionEvaluacion
from project.rules.regla_evaluacion import ReglaEvaluacion


# Servicio que ejecuta todas las reglas de evaluacion y genera el resultado consolidado
# Principios: SRP (solo orquesta la ejecucion de reglas y consolida hallazgos),
# OCP (nuevas reglas se inyectan sin modificar este servicio),
# DIP (depende de la abstraccion ReglaEvaluacion, no de reglas concretas),
# Polymorphism (itera reglas polimorficas transparentemente),
# Low Coupling (desacoplado de las reglas concretas via inyeccion),
# Creator (crea ResultadoEvaluacion con los datos que posee)
class EvaluadorSolicitudes:

    def __init__(self, reglas: List[ReglaEvaluacion]):
        self._reglas = reglas

    def evaluar(self, solicitud: SolicitudReembolso) -> ResultadoEvaluacion:
        """Ejecuta todas las reglas y genera el resultado de evaluacion."""
        hallazgos: List[HallazgoRegla] = []

        for regla in self._reglas:
            hallazgo = regla.evaluar(solicitud)
            if hallazgo is not None:
                hallazgos.append(hallazgo)

        # Si hay hallazgos la solicitud es RECHAZABLE, si no es APROBABLE
        decision = (
            DecisionEvaluacion.RECHAZABLE if hallazgos
            else DecisionEvaluacion.APROBABLE
        )

        return ResultadoEvaluacion(decision=decision, hallazgos=hallazgos)
