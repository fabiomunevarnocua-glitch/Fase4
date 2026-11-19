#Se traen los elementos del proyecto donde cliente 
#permite trabajar con los datos, servicio con los disponibles
#la reservainvalidaerro , errores realcionados con las reservas
#servicioinvalido error  para errores con los servicios, el registrar evento
#guarda informacion de las acciones realizadas y por ultimo esat el que registra los errores 
from cliente import Cliente
from servicio import Servicio
from excepciones import ReservaInvalidaError, ServicioInvalidoError
from logger_config import registrar_evento, registrar_error

class Reserva:
    def __init__(self, cliente, servicio, duracion):
        try:
            if not isinstance(cliente, Cliente):
                raise ReservaInvalidaError("El cliente  no es válido")
            if not isinstance(servicio, Servicio):
                raise ReservaInvalidaError("El servicio no es valido")

            servicio.validar_parametros(duracion)

        except ReservaInvalidaError:
            registrar_error("erro al crear la reserva por datos inválidos.")
            raise
        except ServicioInvalidoError as error:
            registrar_error("La duracion que ingreso no es válida.")
            raise ReservaInvalidaError(
                f"La duración no es válida: {error}"
            ) from error

        self.cliente=cliente
        self.servicio=servicio
        self.duracion=duracion
        self.__estado="pendiente"
        self.__costo= None

        registrar_evento(
            f"Reserva creada: cliente {cliente.get_documento()}, "
            f"servicio {servicio.get_nombre()}, {duracion} horas."
        )

    def get_estado(self):
        return self.__estado
    def get_costo(self):
        return self.__costo
    def confirmar(self):

        if self.__estado != "pendiente":
            raise ReservaInvalidaError(
                "solamente se pueden confirmar las reservas pendientes."
            )

        if not self.servicio.esta_disponible():
            raise ReservaInvalidaError("El servicio no se encuentra disponible.")

        self.__estado= "confirmada"

        registrar_evento(
            f"Reserva confirmada: cliente {self.cliente.get_documento()}, "
            f"servicio {self.servicio.get_nombre()}."
        )

    def cancelar(self):
        if self.__estado == "cancelada":
            raise ReservaInvalidaError("La reserva ya se encuentra cancelada.")

        self.__estado= "cancelada"

        registrar_evento(
            f"Reserva cancelada: cliente {self.cliente.get_documento()}, "
            f"servicio {self.servicio.get_nombre()}."
        )

    def procesar(self):

        try:
            if self.__estado != "confirmada":
                raise ReservaInvalidaError(
                    "solamente se pueden procesar reservas confirmadas."
                )
            if not self.servicio.esta_disponible():
                raise ReservaInvalidaError(
                    "el servicio ya no se encuentra disponible."
                )

            costo = self.servicio.calcular_costo(self.duracion)

        except ReservaInvalidaError:
            registrar_error(
                f"no se pudo procesar la reserva del cliente "
                f"{self.cliente.get_documento()}."
            )
            raise

        except ServicioInvalidoError as error:
            registrar_error(
                f"error al calcular el costo de la reserva del cliente "
                f"{self.cliente.get_documento()}."
            )
            raise ReservaInvalidaError(
                f"No se pudo calcular el costo: {error}"
            ) from error

        else:
            self.__costo = costo
            self.__estado = "procesada"

            registrar_evento(
                f"Reserva procesada: cliente {self.cliente.get_documento()}, "
                f"costo {costo}."
            )

            return costo

        finally:
            registrar_evento("Finalizó el intento de procesar la reserva")

    def mostrar_reserva(self):
        texto = self.cliente.mostrar_datos()
        texto += "\nServicio: " +self.servicio.describir()
        texto += f"\nDuración: {self.duracion} horas"
        texto += f"\nEstado: {self.__estado}"

        if self.__costo is None:
            texto += "\nCosto: Aún no calculado"
        else:
            texto += f"\nCosto: ${self.__costo}"
        return texto
#en el codigo se utilizo encapsulamiennto en los atributos estado y costo
#ya que son datos que se protegen para evitar que queden fuera de la clase 
#para consulta de valores se utilizan los metodos get estado y get costo
#se utiliza isinstance para comprobar que los datos que recibe sean objetos
#de las clases correspondientes por ultimo y no menos importante return texto 
#devuelve toda la infomacion de la reserva 
