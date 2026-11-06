from abc import ABC, abstractmethod


class ClienteInvalidoError(ValueError):
    pass


class Entidad(ABC):
    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador debe ser un texto no vacío.")

        self.__identificador = identificador.strip()

    def obtener_identificador(self):
        return self.__identificador

    @abstractmethod
    def describir(self):
        pass


class Cliente(Entidad):
    def __init__(self, identificador, nombre, correo):
        try:
            super().__init__(identificador)
        except ValueError as error:
            raise ClienteInvalidoError(str(error)) from error

        if not isinstance(nombre, str) or not nombre.strip():
            raise ClienteInvalidoError("El nombre del cliente es obligatorio.")

        if not isinstance(correo, str):
            raise ClienteInvalidoError("El correo debe ser un texto.")

        correo = correo.strip()
        partes = correo.split("@")
        if len(partes) != 2 or partes[0] == "":
            raise ClienteInvalidoError("El correo tiene un formato inválido.")

        dominio = partes[1].split(".")
        if len(dominio) < 2 or "" in dominio:
            raise ClienteInvalidoError("El correo tiene un formato inválido.")

        for caracter in correo:
            if caracter.isspace():
                raise ClienteInvalidoError("El correo no debe tener espacios.")

        self.__nombre = nombre.strip()
        self.__correo = correo

    def obtener_nombre(self):
        return self.__nombre

    def obtener_correo(self):
        return self.__correo

    def describir(self):
        return f"Cliente {self.obtener_identificador()}: {self.obtener_nombre()}"


def registrar_cliente(clientes, identificador, nombre, correo):
    cliente = Cliente(identificador, nombre, correo)

    # Revisar la lista antes de guardar al cliente.
    for registrado in clientes:
        if registrado.obtener_identificador() == cliente.obtener_identificador():
            raise ClienteInvalidoError("Ya existe un cliente con ese identificador.")

    clientes.append(cliente)
    return cliente


if __name__ == "__main__":
    clientes = []
    casos = [
        ("C001", "Ana", "ana@example.com"),
        ("C002", "", "eva@example.com"),
        ("C002", "Eva", "correo-invalido"),
        ("C001", "Eva", "eva@example.com"),
        ("C002", "Luis", "luis@example.com"),
    ]

    for identificador, nombre, correo in casos:
        try:
            cliente = registrar_cliente(clientes, identificador, nombre, correo)
        except ClienteInvalidoError as error:
            print(f"No se pudo registrar: {error}")
        else:
            print(f"Cliente registrado: {cliente.obtener_nombre()}")

    print(f"Total de clientes registrados: {len(clientes)}")
