from typing import List

from project.enums.decision_evaluacion import DecisionEvaluacion
from project.domain.hallazgo_regla import HallazgoRegla


# Resultado consolidado de la evaluacion de todas las reglas sobre una solicitud
# Principios: SRP (solo agrupa decision + hallazgos), KISS (value object directo),
# YAGNI (sin logica adicional)
class ResultadoEvaluacion:

    def __init__(self, decision: DecisionEvaluacion, hallazgos: List[HallazgoRegla]):
        self.decision = decision
        self.hallazgos = hallazgos

    def __repr__(self) -> str:
        return f"ResultadoEvaluacion(decision={self.decision}, hallazgos={len(self.hallazgos)})"
