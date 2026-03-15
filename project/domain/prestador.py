# Entidad que representa al prestador de servicios de salud
# Principios: SRP (solo modela datos del prestador), KISS (estructura minima),
# YAGNI (sin metodos ni campos innecesarios)
class Prestador:

    def __init__(self, id: str, nombre: str):
        self.id = id
        self.nombre = nombre

    def __repr__(self) -> str:
        return f"Prestador(id={self.id}, nombre={self.nombre})"
