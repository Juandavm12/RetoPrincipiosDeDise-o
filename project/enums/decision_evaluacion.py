from enum import Enum


# Enum que representa la decision final de la evaluacion
# Principios: SRP (solo enumera decisiones posibles), KISS (dos valores claros),
# DRY (centraliza las decisiones usadas por evaluador y estados)
class DecisionEvaluacion(Enum):
    APROBABLE = "APROBABLE"
    RECHAZABLE = "RECHAZABLE"
