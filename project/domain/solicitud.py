from __future__ import annotations

from typing import List, Optional
from datetime import date

from project.enums.tipo_solicitud import TipoSolicitud
from project.domain.paciente import Paciente
from project.domain.prestador import Prestador
from project.domain.documento import DocumentoAdjunto
from project.domain.resultado_evaluacion import ResultadoEvaluacion


# Clase central del dominio: representa una solicitud de reembolso
# Principios: SRP (modela solo datos de la solicitud; logica delegada a servicios y estados),
# OCP (extensible via estados y reglas sin modificar esta clase),
# Low Coupling (no depende de implementaciones concretas de estado),
# High Cohesion (agrupa solo atributos propios de la solicitud),
# Creator (la facade o fachada, crea y asigna estados, no la solicitud misma)
class SolicitudReembolso:

    def __init__(
        self,
        paciente: Optional[Paciente],
        prestador: Optional[Prestador],
        tipoSolicitud: Optional[TipoSolicitud],
        valorSolicitado: float,
        fechaEvento: date,
        documentos: Optional[List[DocumentoAdjunto]] = None,
    ):
        self.paciente = paciente
        self.prestador = prestador
        self.tipoSolicitud = tipoSolicitud
        self.valorSolicitado = valorSolicitado
        self.fechaEvento = fechaEvento
        self.documentos: List[DocumentoAdjunto] = documentos if documentos is not None else []
        # El estado actual se asigna externamente por el motor
        self.estadoActual = None  # tipo: IEstadoSolicitud
        # El resultado de evaluacion se asigna tras ejecutar las reglas
        self.resultadoEvaluacion: Optional[ResultadoEvaluacion] = None
