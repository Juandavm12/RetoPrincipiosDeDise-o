from typing import List

from project.enums.tipo_solicitud import TipoSolicitud
from project.policies.politica_tipo_solicitud import IPoliticaTipoSolicitud


# Politica para solicitudes de examenes diagnosticos
# Principios: SRP (solo define reglas del tipo EXAMEN_DIAGNOSTICO),
# OCP (se agrego sin modificar otras politicas), LSP (sustituible por IPoliticaTipoSolicitud),
# Polymorphism (implementa el contrato polimorfico de la interfaz),
# KISS (retorna valores directos sin logica compleja), DRY (reutiliza la interfaz comun)
class ExamenDiagnosticoPolicy(IPoliticaTipoSolicitud):

    def obtenerTipo(self) -> TipoSolicitud:
        return TipoSolicitud.EXAMEN_DIAGNOSTICO

    def obtenerDocumentosObligatorios(self) -> List[str]:
        return ["ORDEN_MEDICA", "RESULTADO_EXAMEN", "FACTURA"]

    def obtenerMontoMaximo(self) -> float:
        return 1_200_000
