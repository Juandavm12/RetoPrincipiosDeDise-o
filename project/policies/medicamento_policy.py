from typing import List

from project.enums.tipo_solicitud import TipoSolicitud
from project.policies.politica_tipo_solicitud import IPoliticaTipoSolicitud


# Politica para solicitudes de medicamentos
# Principios: SRP (solo define reglas del tipo MEDICAMENTO),
# OCP (se agrego sin modificar otras politicas), LSP (sustituible por IPoliticaTipoSolicitud),
# Polymorphism (implementa el contrato polimorfico de la interfaz),
# KISS (retorna valores directos sin logica compleja), DRY (reutiliza la interfaz comun)
class MedicamentoPolicy(IPoliticaTipoSolicitud):

    def obtenerTipo(self) -> TipoSolicitud:
        return TipoSolicitud.MEDICAMENTO

    def obtenerDocumentosObligatorios(self) -> List[str]:
        return ["FORMULA_MEDICA", "FACTURA"]

    def obtenerMontoMaximo(self) -> float:
        return 800_000
