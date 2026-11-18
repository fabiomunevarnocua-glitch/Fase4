# Cada módulo usa la excepción que corresponde a su operación.
# ValueError permite manejar juntas estas excepciones en el menú.
class ClienteInvalidoError(ValueError):
    pass  # Identifica datos de cliente que no se pueden registrar.


class ServicioInvalidoError(ValueError):
    pass  # Identifica parámetros o costos incorrectos de un servicio.


class ReservaInvalidaError(ValueError):
    pass  # Identifica problemas al crear, confirmar o cancelar una reserva.
