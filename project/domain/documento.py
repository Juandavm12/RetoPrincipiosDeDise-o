from datetime import date


# Entidad que representa un documento adjunto a la solicitud
# Principios: SRP (solo modela datos del documento), KISS (estructura simple sin logica innecesaria),
# YAGNI (solo atributos estrictamente necesarios)
class DocumentoAdjunto:

    def __init__(self, tipo: str, nombre: str, fechaCarga: date):
        self.tipo = tipo
        self.nombre = nombre
        self.fechaCarga = fechaCarga

    def __repr__(self) -> str:
        return f"DocumentoAdjunto(tipo={self.tipo}, nombre={self.nombre})"
