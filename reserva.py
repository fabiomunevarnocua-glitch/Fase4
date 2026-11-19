from cliente import Cliente
from servicio import Servicio
from excepciones import ReservaInvalidaError,ServicioInvalidoError
from logger_config import registrar_evento,registrar_error


class Reserva:

    def __init__(self, cliente, servicio, duracion):
        try:
            if not isinstance(cliente, Cliente):
                raise ReservaInvalidaError("El cliente tiene que ser un objeto de la clase Cliente.")
            if not isinstance(servicio, Servicio):
                raise ReservaInvalidaError("El servicio tiene que ser un objeto de la clase Servicio.")
            servicio.validar_parametros(duracion)
        except ReservaInvalidaError:
            registrar_error("No se pudo crear la reserva: ya que el cliente o servicio es inválido.")
            raise
        except ServicioInvalidoError as error:
            registrar_error("No se pudo crear la reserva por una duración inválida.")
            raise ReservaInvalidaError(f"La duración no es válida: {error}") from error
        self.cliente = cliente
        self.servicio =servicio
        self.duracion =duracion
        self.__estado ="pendiente"   
        self.__costo=None           
        registrar_evento(
            f"Reserva creada: cliente {cliente.get_documento()}, "
            f"servicio {servicio.get_nombre()}, {duracion} horas."
        )

    def get_estado(self):
        return self.__estado

    def get_costo(self):
        return self.__costo

    def confirmar(self):
        try:
            if self.__estado != "pendiente":
                raise ReservaInvalidaError(
                    f"No se puede confirmar una reserva en estado {self.__estado}."
                )
            if not self.servicio.esta_disponible():
                raise ReservaInvalidaError("El servicio no está disponible.")
        except ReservaInvalidaError:
            registrar_error(
                f"No se pudo confirmar la reserva del cliente {self.cliente.get_documento()}."
            )
            raise
        else:
            self.__estado = "confirmada"
            registrar_evento(
                f"Reserva confirmada: cliente {self.cliente.get_documento()}, "
                f"servicio {self.servicio.get_nombre()}."
            )

    def cancelar(self):
        try:
            if self.__estado == "cancelada":
                raise ReservaInvalidaError("La reserva ya está cancelada.")
            elif self.__estado == "procesada":
                raise ReservaInvalidaError("no se puede cancelar una reserva que ya fue procesada.")
        except ReservaInvalidaError:
            registrar_error(
                f"no se pudo cancelar la reserva del cliente {self.cliente.get_documento()}."
            )
            raise
        else:
            self.__estado = "cancelada"
            registrar_evento(
                f"Reserva cancelada: cliente {self.cliente.get_documento()}, "
                f"servicio {self.servicio.get_nombre()}."
            )

    def procesar(self):
        try:
            if self.__estado != "confirmada":
                raise ReservaInvalidaError(
                    f"como tal solo se puede procesar una reserva confirmada (estado actual: {self.__estado})."
                )
            if not self.servicio.esta_disponible():
                raise ReservaInvalidaError("El servicio ya no se encuentra disponible.")
            costo = self.servicio.calcular_costo(self.duracion)
        except ReservaInvalidaError:
            registrar_error(
                f"no se pudo procesar la reserva del cliente {self.cliente.get_documento()}."
            )
            raise
        except ServicioInvalidoError as error:
            registrar_error(
                f"Error al calcular el costo de la reserva del cliente {self.cliente.get_documento()}."
            )
            raise ReservaInvalidaError("no se pudo calcular el costo de la reserva.") from error
        else:
            self.__costo=costo
            self.__estado = "procesada"
            registrar_evento(
                f"Reserva procesada: cliente {self.cliente.get_documento()}, costo {costo}."
            )
        finally:
            registrar_evento(" se terminó el intento de procesar la reserva.")

    def mostrar_reserva(self):
        texto = self.cliente.mostrar_datos()
        texto = texto + "\nServicio: " + self.servicio.describir()
        texto = texto + f"\nDuración: {self.duracion} horas"
        texto = texto + f"\nEstado: {self.__estado}"
        if self.__costo is None:
            texto = texto + "\nCosto: aún no calculado"
        else:
            texto = texto + f"\nCosto: ${self.__costo}"
        return texto
