# Los tres servicios comparten validaciones y reglas de costo.
from abc import abstractmethod
from math import isfinite

from cliente import Entidad
from excepciones import ServicioInvalidoError


class Servicio(Entidad):
    """Datos y reglas comunes de los servicios de Software FJ."""

    def __init__(self, nombre, tarifa_hora):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio es obligatorio.")
        self._validar_numero(tarifa_hora, "La tarifa")
        if tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa debe ser mayor que cero.")

        # Los atributos con __ se leen o cambian mediante métodos de la clase.
        self.__nombre = nombre.strip()
        self.__tarifa_hora = tarifa_hora
        self.__disponible = True

    def get_nombre(self):
        return self.__nombre

    def esta_disponible(self):
        return self.__disponible

    def set_disponible(self, disponible):
        if not isinstance(disponible, bool):
            raise ServicioInvalidoError("La disponibilidad debe ser True o False.")
        self.__disponible = disponible

    def _validar_numero(self, valor, campo):
        # Aceptamos enteros y decimales. La comparación exacta excluye True y False.
        if type(valor) not in (int, float):
            raise ServicioInvalidoError(f"{campo} debe ser un número.")
        try:
            finito = isfinite(valor)  # Rechaza infinito y NaN.
        except OverflowError as error:
            raise ServicioInvalidoError(f"{campo} es demasiado grande.") from error
        if not finito:
            raise ServicioInvalidoError(f"{campo} debe ser un número finito.")

    def _validar_duracion(self, duracion):
        self._validar_numero(duracion, "La duración")
        if duracion <= 0:
            raise ServicioInvalidoError("La duración debe ser mayor que cero.")

    def _calcular_costo_base(self, duracion, impuesto, descuento, unidades=1):
        # Una tasa de 0.10 equivale al 10 %. Primero se aplica el descuento.
        self._validar_numero(impuesto, "El impuesto")
        self._validar_numero(descuento, "El descuento")
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise ServicioInvalidoError("Las tasas deben estar entre 0 y 1.")

        try:
            # Multiplicamos la tarifa por las horas y las unidades antes de aplicar las tasas.
            costo = self.__tarifa_hora * duracion * unidades * (1 - descuento) * (1 + impuesto)
        except OverflowError as error:
            raise ServicioInvalidoError("El costo es demasiado grande.") from error
        self._validar_numero(costo, "El costo")
        return round(costo, 2)

    # Las clases concretas deben ofrecer los mismos métodos para que Reserva pueda usarlas.
    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass


class ReservaSala(Servicio):
    # Una sala cobra por hora. Su capacidad se valida al crear el servicio.
    def __init__(self, nombre, tarifa_hora, capacidad):
        super().__init__(nombre, tarifa_hora)
        if type(capacidad) is not int or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad debe ser un entero positivo.")
        self.__capacidad = capacidad

    def describir(self):
        return f"Sala {self.get_nombre()} para {self.__capacidad} personas"

    def validar_parametros(self, duracion):
        self._validar_duracion(duracion)

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros(duracion)  # Comprueba las horas antes de calcular.
        return self._calcular_costo_base(duracion, impuesto, descuento)


class AlquilerEquipo(Servicio):
    # En equipos, la tarifa se aplica por hora y por unidad.
    def __init__(self, nombre, tarifa_hora, unidades):
        super().__init__(nombre, tarifa_hora)
        if type(unidades) is not int or unidades <= 0:
            raise ServicioInvalidoError("Las unidades deben ser un entero positivo.")
        self.__unidades = unidades

    def describir(self):
        return f"Equipo {self.get_nombre()} ({self.__unidades} unidades)"

    def validar_parametros(self, duracion):
        self._validar_duracion(duracion)

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros(duracion)  # Comprueba las horas antes de calcular.
        return self._calcular_costo_base(duracion, impuesto, descuento, self.__unidades)


class AsesoriaEspecializada(Servicio):
    # El tema identifica qué se ofrece en la asesoría.
    def __init__(self, nombre, tarifa_hora, tema):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(tema, str) or not tema.strip():
            raise ServicioInvalidoError("El tema de la asesoría es obligatorio.")
        self.__tema = tema.strip()

    def describir(self):
        return f"Asesoría {self.get_nombre()} sobre {self.__tema}"

    def validar_parametros(self, duracion):
        self._validar_duracion(duracion)

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros(duracion)  # Comprueba las horas antes de calcular.
        return self._calcular_costo_base(duracion, impuesto, descuento)
