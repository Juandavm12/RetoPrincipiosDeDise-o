from typing import List

from project.enums.tipo_solicitud import TipoSolicitud
from project.policies.politica_tipo_solicitud import IPoliticaTipoSolicitud


# Politica para solicitudes de urgencias
# Principios: SRP (solo define reglas del tipo URGENCIAS),
# OCP (se agrego sin modificar otras politicas), LSP (sustituible por IPoliticaTipoSolicitud),
# Polymorphism (implementa el contrato polimorfico de la interfaz),
# KISS (retorna valores directos sin logica compleja), DRY (reutiliza la interfaz comun)
class UrgenciasPolicy(IPoliticaTipoSolicitud):

    def obtenerTipo(self) -> TipoSolicitud:
        return TipoSolicitud.URGENCIAS

    def obtenerDocumentosObligatorios(self) -> List[str]:
        return ["HISTORIA_CLINICA_URGENCIAS", "FACTURA"]

    def obtenerMontoMaximo(self) -> float:
        return 3_500_000
