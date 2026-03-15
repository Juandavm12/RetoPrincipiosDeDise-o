from enum import Enum


# Enum que clasifica los tipos de solicitud de reembolso
# Principios: SRP (solo enumera tipos de solicitud), KISS (constantes planas),
# DRY (unico punto de definicion de tipos consumido por politicas y reglas),
# OCP (agregar un nuevo tipo no modifica los existentes)
class TipoSolicitud(Enum):
    MEDICAMENTO = "MEDICAMENTO"
    PROCEDIMIENTO_AMBULATORIO = "PROCEDIMIENTO_AMBULATORIO"
    URGENCIAS = "URGENCIAS"
    EXAMEN_DIAGNOSTICO = "EXAMEN_DIAGNOSTICO"
