# Módulo de clientes de Software FJ.
# Los datos se leen y modifican mediante métodos get y set.
from abc import ABC, abstractmethod  # Permite definir una clase abstracta.


class ClienteInvalidoError(ValueError):  # Representa errores en los datos del cliente.
    pass  # Utiliza el comportamiento de ValueError con un nombre propio.


class Entidad(ABC):  # Es la base abstracta que representa una entidad del sistema.
    @abstractmethod  # Obliga a las clases hijas a implementar este método.
    def describir(self):  # Define cómo debe solicitarse la descripción de una entidad.
        pass  # Cada clase hija escribirá su propia descripción.


class Cliente(Entidad):  # Hereda de Entidad y representa a una persona registrada.
    def __init__(self, nombre, documento, correo):  # Recibe los datos del nuevo cliente.
        self.set_nombre(nombre)  # Valida el nombre antes de guardarlo.
        self.set_documento(documento)  # Valida el documento antes de guardarlo.
        self.set_correo(correo)  # Valida el correo antes de guardarlo.

    def validar_nombre(self, nombre):  # Comprueba el dato recibido sin modificar el objeto.
        if not isinstance(nombre, str):  # Verifica que el nombre sea texto.
            raise ClienteInvalidoError("El nombre debe ser un texto.")  # Informa el tipo incorrecto.
        if nombre.strip() == "":  # Comprueba que haya contenido aparte de espacios.
            raise ClienteInvalidoError("El nombre es obligatorio.")  # Rechaza el nombre vacío.

    def validar_documento(self, documento):  # Revisa el identificador del cliente.
        if not isinstance(documento, str):  # Exige texto para conservar posibles ceros iniciales.
            raise ClienteInvalidoError("El documento debe ser un texto.")  # Informa el tipo incorrecto.
        if documento.strip() == "":  # Revisa que el documento tenga contenido.
            raise ClienteInvalidoError("El documento es obligatorio.")  # Rechaza el documento vacío.

    def validar_correo(self, correo):  # Hace una comprobación básica del formato del correo.
        if not isinstance(correo, str):  # Verifica el tipo antes de usar métodos de texto.
            raise ClienteInvalidoError("El correo debe ser un texto.")  # Informa el tipo incorrecto.
        correo = correo.strip()  # Quita espacios de los extremos para revisar el correo.
        partes = correo.split("@")  # Separa el usuario del dominio del correo.
        if len(partes) != 2 or partes[0] == "":  # Exige una sola arroba y un usuario.
            raise ClienteInvalidoError("El correo tiene un formato inválido.")  # Rechaza el formato.
        dominio = partes[1].split(".")  # Separa las partes del dominio.
        if len(dominio) < 2 or "" in dominio:  # Exige un punto y partes con contenido.
            raise ClienteInvalidoError("El dominio del correo es inválido.")  # Rechaza el dominio.
        for caracter in correo:  # Revisa uno por uno los caracteres del correo.
            if caracter.isspace():  # Detecta espacios o tabulaciones dentro del correo.
                raise ClienteInvalidoError("El correo no debe contener espacios.")  # Informa el error.

    def get_nombre(self):  # Permite consultar el nombre encapsulado.
        return self.__nombre  # Devuelve el nombre del objeto actual.

    def set_nombre(self, nombre):  # Permite cambiar el nombre con validación.
        self.validar_nombre(nombre)  # Detiene el cambio si el dato es inválido.
        self.__nombre = nombre.strip()  # Guarda el nombre en un atributo interno.

    def get_documento(self):  # Permite consultar el documento encapsulado.
        return self.__documento  # Devuelve el documento del objeto actual.

    def set_documento(self, documento):  # Permite cambiar el documento con validación.
        self.validar_documento(documento)  # Revisa el dato antes de modificarlo.
        self.__documento = documento.strip()  # Guarda el documento como texto.

    def get_correo(self):  # Permite consultar el correo encapsulado.
        return self.__correo  # Devuelve el correo del objeto actual.

    def set_correo(self, correo):  # Permite cambiar el correo con validación.
        self.validar_correo(correo)  # Mantiene el correo anterior si el nuevo dato falla.
        self.__correo = correo.strip()  # Guarda el correo que pasó la validación.

    def describir(self):  # Implementa el método abstracto definido en Entidad.
        return f"Cliente {self.get_documento()}: {self.get_nombre()}"  # Devuelve una descripción.

    def mostrar_datos(self):  # Prepara los datos para mostrarlos desde el programa principal.
        datos = self.describir()  # Obtiene el documento y el nombre.
        datos = datos + f" | Correo: {self.get_correo()}"  # Agrega el correo al texto.
        return datos  # Devuelve el texto para que quien llama decida dónde mostrarlo.


def registrar_cliente(clientes, nombre, documento, correo):  # Recibe la lista y los datos del cliente.
    cliente = Cliente(nombre, documento, correo)  # Crea el objeto y valida sus tres datos.
    for registrado in clientes:  # Revisa los clientes que ya están guardados.
        if registrado.get_documento() == cliente.get_documento():  # Compara documentos sin espacios externos.
            raise ClienteInvalidoError("Ya existe un cliente con ese documento.")  # Evita registrar un duplicado.
    clientes.append(cliente)  # Guarda el objeto después de pasar todas las validaciones.
    return cliente  # Devuelve el cliente para utilizarlo en otras operaciones.


if __name__ == "__main__":  # Abre el menú solo al ejecutar este archivo directamente.
    clientes = []  # Guarda los clientes durante esta ejecución del programa.
    while True:  # Repite el menú hasta que el usuario elija salir.
        print("\n1. Registrar cliente")  # Muestra la opción para ingresar datos.
        print("2. Mostrar clientes")  # Muestra la opción de consultar la lista.
        print("3. Salir")  # Muestra la opción para terminar.
        opcion = input("Seleccione una opción: ").strip()  # Lee la elección del usuario.
        if opcion == "1":  # Inicia el registro cuando se elige la primera opción.
            nombre = input("Nombre: ")  # Solicita el nombre del cliente.
            documento = input("Documento: ")  # Lee el documento como texto.
            correo = input("Correo: ")  # Solicita el correo del cliente.
            try:  # Intenta validar y guardar los datos recibidos.
                cliente = registrar_cliente(clientes, nombre, documento, correo)  # Crea el objeto encapsulado.
            except ClienteInvalidoError as error:  # Controla los datos inválidos sin cerrar el menú.
                print(f"No se pudo registrar: {error}")  # Explica qué dato debe corregirse.
            else:  # Se ejecuta cuando el registro termina correctamente.
                print(f"Cliente registrado: {cliente.get_nombre()}")  # Consulta el nombre mediante su método.
        elif opcion == "2":  # Atiende la consulta de clientes registrados.
            if len(clientes) == 0:  # Comprueba si la lista está vacía.
                print("Todavía no hay clientes registrados.")  # Informa que falta registrar clientes.
            else:  # Recorre la lista cuando ya tiene datos.
                for cliente in clientes:  # Obtiene cada objeto de la lista.
                    print(cliente.mostrar_datos())  # Consulta sus datos mediante los métodos públicos.
        elif opcion == "3":  # Atiende la solicitud de terminar.
            print("Programa finalizado.")  # Confirma que termina la ejecución.
            break  # Sale del ciclo del menú.
        else:  # Atiende cualquier opción distinta de las anteriores.
            print("Opción inválida. Seleccione 1, 2 o 3.")  # Invita a elegir una opción permitida.
