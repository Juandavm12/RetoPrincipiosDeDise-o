# Hallazgo generado por una regla de evaluacion cuando se detecta un problema
# Principios: SRP (solo transporta el resultado de una regla), KISS (value object simple),
# YAGNI (sin campos extra)
class HallazgoRegla:

    def __init__(self, regla: str, descripcion: str):
        self.regla = regla
        self.descripcion = descripcion

    def __repr__(self) -> str:
        return f"HallazgoRegla(regla={self.regla}, descripcion={self.descripcion})"
