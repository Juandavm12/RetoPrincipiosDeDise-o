from typing import Optional

from project.domain.solicitud import SolicitudReembolso
from project.domain.hallazgo_regla import HallazgoRegla
from project.rules.regla_evaluacion import ReglaEvaluacion
from project.ports.tipo_solicitud_provider import ITipoSolicitudProvider


# Regla: verifica que la solicitud tenga los documentos obligatorios segun su politica
# Principios: SRP (solo valida documentacion minima), OCP (extensible sin modificar otras reglas),
# LSP (sustituible por ReglaEvaluacion), DIP (depende de ITipoSolicitudProvider, no de concretas),
# Polymorphism, Low Coupling (usa puerto para obtener la politica)
class ReglaDocumentacionMinima(ReglaEvaluacion):

    def __init__(self, provider: ITipoSolicitudProvider):
        self._provider = provider

    def evaluar(self, solicitud: SolicitudReembolso) -> Optional[HallazgoRegla]:
        politica = self._provider.obtenerPor(solicitud.tipoSolicitud)
        documentos_obligatorios = politica.obtenerDocumentosObligatorios()
        tipos_presentes = {doc.tipo for doc in solicitud.documentos}

        faltantes = [doc for doc in documentos_obligatorios if doc not in tipos_presentes]

        if faltantes:
            return HallazgoRegla(
                regla="ReglaDocumentacionMinima",
                descripcion=f"Documentos faltantes: {', '.join(faltantes)}",
            )
        return None
