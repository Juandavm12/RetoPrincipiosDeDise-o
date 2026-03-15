# Entidad que representa al paciente que solicita el reembolso
# Principios: SRP (solo modela datos del paciente), KISS (estructura minima),
# YAGNI (sin metodos ni campos innecesarios)
class Paciente:

    def __init__(self, id: str, nombre: str):
        self.id = id
        self.nombre = nombre

    def __repr__(self) -> str:
        return f"Paciente(id={self.id}, nombre={self.nombre})"
