from typing import List

from project.enums.tipo_solicitud import TipoSolicitud
from project.policies.politica_tipo_solicitud import IPoliticaTipoSolicitud


# Politica para solicitudes de procedimientos ambulatorios
# Principios: SRP (solo define reglas del tipo PROCEDIMIENTO_AMBULATORIO),
# OCP (se agrego sin modificar otras politicas), LSP (sustituible por IPoliticaTipoSolicitud),
# Polymorphism (implementa el contrato polimorfico de la interfaz),
# KISS (retorna valores directos sin logica compleja), DRY (reutiliza la interfaz comun)
class ProcedimientoAmbulatorioPolicy(IPoliticaTipoSolicitud):

    def obtenerTipo(self) -> TipoSolicitud:
        return TipoSolicitud.PROCEDIMIENTO_AMBULATORIO

    def obtenerDocumentosObligatorios(self) -> List[str]:
        return ["ORDEN_MEDICA", "FACTURA"]

    def obtenerMontoMaximo(self) -> float:
        return 2_500_000
