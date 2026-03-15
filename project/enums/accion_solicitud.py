from enum import Enum


# Enum que define las acciones posibles sobre una solicitud
# Principios: SRP (solo enumera acciones), KISS (constantes claras sin logica),
# DRY (centraliza nombres de acciones que se reutilizan en estados y servicios)
class AccionSolicitud(Enum):
    SUBMIT = "SUBMIT"
    START_REVIEW = "START_REVIEW"
    EVALUATE = "EVALUATE"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
