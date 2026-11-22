
# Punto de entrada principal del sistema Software FJ.
# Este archivo conecta los módulos de clientes, servicios y reservas.
# También contiene el menú de opciones y las pruebas automáticas.

# Importación de las funciones y clases necesarias para ejecutar el programa.
from cliente import registrar_cliente
from excepciones import ClienteInvalidoError, ReservaInvalidaError, ServicioInvalidoError
from logger_config import configurar_logger, registrar_error, registrar_evento
from reserva import Reserva
from servicio import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


# Función para registrar un cliente en el sistema.
def agregar_cliente(clientes, nombre, documento, correo):
    # Se utiliza el módulo cliente para validar y registrar la información.
    cliente = registrar_cliente(clientes, nombre, documento, correo)
    return cliente.describir()


# Función encargada de crear y registrar un servicio.
def agregar_servicio(servicios, tipo, nombre, tarifa, detalle):
    # Se recibe el tipo de servicio y se crea el objeto correspondiente.
    servicio = tipo(nombre, tarifa, detalle)
    servicios.append(servicio)
    return servicio.describir()


# Función que permite crear y procesar una reserva.
def crear_reserva(reservas, cliente, servicio, duracion):
    # Se crea la reserva relacionando el cliente con el servicio seleccionado.
    reserva = Reserva(cliente, servicio, duracion)

    # Se confirma la reserva y se calcula el costo correspondiente.
    reserva.confirmar()
    costo = reserva.procesar()

    # Se almacena la reserva y se devuelve su información.
    reservas.append(reserva)
    return f"{reserva.mostrar_reserva()} | Costo: {costo:,.0f} COP"


# Función para cancelar una reserva existente.
def cancelar_reserva(reserva):
    # La reserva permanece almacenada para consultar posteriormente su estado.
    reserva.cancelar()
    return reserva.mostrar_reserva()


# Función que ejecuta operaciones y controla posibles errores.
def ejecutar_operacion(numero, descripcion, operacion, *datos):
    print(f"\n{numero}. {descripcion}")
    try:
        # Se ejecuta la operación con los argumentos recibidos.
        resultado = operacion(*datos)

    # Se capturan los errores relacionados con clientes, servicios y reservas.
    except (ClienteInvalidoError, ServicioInvalidoError, ReservaInvalidaError) as error:
        print(f"Rechazado: {error}")

        # Se registra el error para llevar un control de las operaciones rechazadas.
        registrar_error(descripcion)
    else:
        # Si la operación se realiza correctamente, se muestra y registra el resultado.
        print(resultado)
        registrar_evento(descripcion)


# Función que realiza una demostración automática del funcionamiento del sistema.
def ejecutar_demostracion():
    # Se crean listas independientes para almacenar los datos de las pruebas.
    clientes = []
    servicios = []
    reservas = []

    try:
        # Se configura el registro de eventos y errores.
        configurar_logger()

        # Prueba 1: registro correcto de un cliente.
        ejecutar_operacion(1, "Registrar cliente", agregar_cliente,
                           clientes, "Ana", "1001", "ana@example.com")

        # Prueba 2: validación de un correo electrónico incorrecto.
        ejecutar_operacion(2, "Rechazar correo inválido", agregar_cliente,
                           clientes, "Eva", "1002", "correo-invalido")

        # Prueba 3: creación de una sala.
        ejecutar_operacion(3, "Crear sala", agregar_servicio,
                           servicios, ReservaSala, "Principal", 30000, 12)

        # Prueba 4: creación de un servicio de alquiler de equipos.
        ejecutar_operacion(4, "Crear equipo", agregar_servicio,
                           servicios, AlquilerEquipo, "Proyector", 20000, 2)

        # Prueba 5: creación de una asesoría especializada.
        ejecutar_operacion(5, "Crear asesoría", agregar_servicio,
                           servicios, AsesoriaEspecializada, "Técnica", 50000, "Python")

        # Prueba 6: rechazo de un servicio con tarifa negativa.
        ejecutar_operacion(6, "Rechazar tarifa negativa", agregar_servicio,
                           servicios, ReservaSala, "Auxiliar", -1000, 8)

        # Prueba 7: creación de una reserva de sala por dos horas.
        ejecutar_operacion(7, "Reservar sala por 2 horas", crear_reserva,
                           reservas, clientes[0], servicios[0], 2)

        # Prueba 8: reserva de dos equipos durante dos horas.
        ejecutar_operacion(8, "Reservar dos equipos por 2 horas", crear_reserva,
                           reservas, clientes[0], servicios[1], 2)

        # Prueba 9: reserva de una asesoría especializada.
        ejecutar_operacion(9, "Reservar asesoría por 2 horas", crear_reserva,
                           reservas, clientes[0], servicios[2], 2)

        # Prueba 10: rechazo de una reserva con duración de cero horas.
        ejecutar_operacion(10, "Rechazar duración de cero horas", crear_reserva,
                           reservas, clientes[0], servicios[0], 0)

        # Se cambia la disponibilidad de la sala para probar su validación.
        servicios[0].set_disponible(False)

        # Prueba 11: intento de reservar una sala que no está disponible.
        ejecutar_operacion(11, "Rechazar sala no disponible", crear_reserva,
                           reservas, clientes[0], servicios[0], 2)

        # Prueba 12: cancelación de la primera reserva registrada.
        ejecutar_operacion(12, "Cancelar la primera reserva", cancelar_reserva, reservas[0])

        # Prueba 13: cálculo del costo aplicando impuesto y descuento.
        ejecutar_operacion(13, "Calcular costo con descuento e impuesto",
                           servicios[0].calcular_costo, 2, 0.19, 0.10)

    except OSError as error:
        # Se informa cuando ocurre un problema de acceso a los archivos.
        print(f"Problema de acceso a archivos: {error}")
    finally:
        # Se muestra el resumen de clientes, servicios y reservas procesadas.
        print(f"\nClientes: {len(clientes)} | Servicios: {len(servicios)} | Reservas: {len(reservas)}")


# Función que permite seleccionar un registro de una lista.
def elegir_registro(registros, mostrar):
    # Se muestran los registros numerados para facilitar su selección.
    for numero, registro in enumerate(registros, start=1):
        print(f"{numero}. {mostrar(registro)}")

    try:
        # Se solicita al usuario el número del registro que desea seleccionar.
        numero = int(input("Escribe el número de la lista: "))
    except ValueError as error:
        raise ReservaInvalidaError("Escribe un número entero.") from error

    # Se valida que el número ingresado corresponda a un registro existente.
    if numero < 1 or numero > len(registros):
        raise ReservaInvalidaError("El número no está en la lista.")

    # Se devuelve el elemento seleccionado.
    return registros[numero - 1]


# Función principal que contiene el menú interactivo del sistema.
def menu():
    # Se inicializan las listas que almacenan la información durante la ejecución.
    clientes = []
    reservas = []

    # Se crean los servicios disponibles con sus respectivas tarifas.
    servicios = [
        ReservaSala("Principal", 30000, 12),
        AlquilerEquipo("Proyector", 20000, 1),
        AsesoriaEspecializada("Técnica", 50000, "Python"),
    ]

    # Se configura el registro de eventos y errores.
    configurar_logger()

    # El ciclo mantiene el menú activo hasta que el usuario seleccione salir.
    while True:
        opcion = input("""
--- Software FJ ---
1. Registrar cliente
2. Crear reserva y calcular costo
3. Mostrar reservas
4. Cancelar reserva
5. Ejecutar demostración automática
0. Salir
Selecciona una opción: """).strip()

        try:
            # Opción 1: registrar un nuevo cliente.
            if opcion == "1":
                nombre = input("Nombre: ")
                documento = input("Documento: ")
                correo = input("Correo: ")

                print(agregar_cliente(clientes, nombre, documento, correo))
                registrar_evento("Cliente registrado desde el menú")

            # Opción 2: crear una reserva y calcular su costo.
            elif opcion == "2":
                # Antes de crear una reserva, se verifica que exista un cliente registrado.
                if not clientes:
                    raise ReservaInvalidaError("Primero registra un cliente con la opción 1.")

                # Se selecciona el cliente que realizará la reserva.
                print("Elige el cliente.")
                cliente = elegir_registro(clientes, lambda cliente: cliente.describir())

                # Se selecciona el servicio que se desea reservar.
                print("Elige el servicio.")
                servicio = elegir_registro(servicios, lambda servicio: servicio.describir())

                try:
                    # Se solicita la duración en horas y se acepta coma o punto decimal.
                    horas = float(input("Duración en horas: ").strip().replace(",", "."))
                except ValueError as error:
                    raise ReservaInvalidaError("La duración debe ser un número.") from error

                # Se crea la reserva y se muestra el costo calculado.
                print(crear_reserva(reservas, cliente, servicio, horas))
                registrar_evento("Reserva confirmada desde el menú")

            # Opción 3: consultar las reservas registradas.
            elif opcion == "3":
                if not reservas:
                    print("Todavía no hay reservas.")

                # Se muestra la información de cada reserva.
                for reserva in reservas:
                    print(reserva.mostrar_reserva())

            # Opción 4: cancelar una reserva existente.
            elif opcion == "4":
                # Comprueba que existan reservas antes de permitir su cancelación.
                if not reservas:
                    raise ReservaInvalidaError("Todavía no hay reservas para cancelar.")

                # Se selecciona la reserva que se desea cancelar.
                reserva = elegir_registro(reservas, Reserva.mostrar_reserva)
                print(cancelar_reserva(reserva))
                registrar_evento("Reserva cancelada desde el menú")

            # Opción 5: ejecutar las pruebas automáticas del programa.
            elif opcion == "5":
                # Inicia la demostración automática de las funcionalidades del sistema.
                ejecutar_demostracion()

            # Opción 0: finalizar el programa.
            elif opcion == "0":
                print("Programa finalizado.")
                break

            # Se controlan las opciones que no están disponibles en el menú.
            else:
                # Evita que se ingresen opciones que no están disponibles en el menú.
                raise ValueError("Selecciona una opción del 0 al 5.")

        except ValueError as error:
            # Se muestra el mensaje del error y se registra en el archivo de log.
            print(f"Rechazado: {error}")
            registrar_error(f"Error en la opción {opcion} del menú")


# Este bloque permite ejecutar el menú cuando se inicia directamente main.py.
# Evita que el menú se ejecute automáticamente cuando el archivo es importado.
if __name__ == "__main__":
    try:
        menu()
    except (EOFError, KeyboardInterrupt):
        # Permite finalizar el programa cuando el usuario interrumpe la ejecución.
        print("\nPrograma finalizado.")
    except OSError as error:
        # Se informa si ocurre un problema al acceder al archivo de registro.
        print(f"No se pudo acceder al archivo de log: {error}")

