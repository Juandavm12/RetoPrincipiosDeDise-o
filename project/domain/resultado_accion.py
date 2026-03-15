# Resultado de ejecutar una accion sobre una solicitud
# Principios: SRP (solo transporta exito/fallo de una accion),
# YAGNI (solo los campos necesarios)
class ResultadoAccion:

    def __init__(self, exitoso: bool, mensaje: str):
        self.exitoso = exitoso
        self.mensaje = mensaje

    def __repr__(self) -> str:
        return f"ResultadoAccion(exitoso={self.exitoso}, mensaje={self.mensaje})"
