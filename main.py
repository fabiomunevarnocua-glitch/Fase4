
# Archivo principal del sistema Software FJ.
# Se encarga de organizar las operaciones y mostrar el menú al usuario.

# Importación de los módulos, clases y funciones necesarios para el funcionamiento del sistema.
from cliente import registrar_cliente
from excepciones import ClienteInvalidoError, ReservaInvalidaError, ServicioInvalidoError
from logger_config import configurar_logger, registrar_error, registrar_evento
from reserva import Reserva
from servicio import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


# Registra un cliente utilizando los datos proporcionados por el usuario.
def agregar_cliente(clientes, nombre, documento, correo):
    # El módulo cliente valida los datos y agrega el objeto a la lista.
    cliente = registrar_cliente(clientes, nombre, documento, correo)
    return cliente.describir()


# Crea un servicio según el tipo seleccionado y lo almacena en la lista.
def agregar_servicio(servicios, tipo, nombre, tarifa, detalle):
    # tipo es la clase concreta que se quiere crear, por ejemplo ReservaSala.
    servicio = tipo(nombre, tarifa, detalle)
    servicios.append(servicio)
    return servicio.describir()


# Crea, confirma y procesa una reserva para calcular su costo.
def crear_reserva(reservas, cliente, servicio, duracion):
    # La reserva se guarda solo si se confirma y se calcula su costo.
    reserva = Reserva(cliente, servicio, duracion)
    reserva.confirmar()
    costo = reserva.procesar()
    reservas.append(reserva)
    return f"{reserva.mostrar_reserva()} | Costo: {costo:,.0f} COP"


# Cambia el estado de una reserva para indicar que ha sido cancelada.
def cancelar_reserva(reserva):
    # Conservamos la reserva en la lista para poder consultar su estado.
    reserva.cancelar()
    return reserva.mostrar_reserva()


# Ejecuta una operación y controla los posibles errores que puedan presentarse.
def ejecutar_operacion(numero, descripcion, operacion, *datos):
    print(f"\n{numero}. {descripcion}")
    try:
        # *datos entrega a la función cada argumento por separado.
        resultado = operacion(*datos)
    except (ClienteInvalidoError, ServicioInvalidoError, ReservaInvalidaError) as error:
        print(f"Rechazado: {error}")
        registrar_error(descripcion)
    else:
        print(resultado)
        registrar_evento(descripcion)


# Ejecuta una prueba automática de las principales funciones del sistema.
def ejecutar_demostracion():
    # Estas listas son independientes de las reservas digitadas en el menú.
    clientes = []
    servicios = []
    reservas = []

    try:
        configurar_logger()

        # Se prueban registros correctos y datos inválidos de clientes y servicios.
        ejecutar_operacion(1, "Registrar cliente", agregar_cliente,
                           clientes, "Ana", "1001", "ana@example.com")
        ejecutar_operacion(2, "Rechazar correo inválido", agregar_cliente,
                           clientes, "Eva", "1002", "correo-invalido")
        ejecutar_operacion(3, "Crear sala", agregar_servicio,
                           servicios, ReservaSala, "Principal", 30000, 12)
        ejecutar_operacion(4, "Crear equipo", agregar_servicio,
                           servicios, AlquilerEquipo, "Proyector", 20000, 2)
        ejecutar_operacion(5, "Crear asesoría", agregar_servicio,
                           servicios, AsesoriaEspecializada, "Técnica", 50000, "Python")
        ejecutar_operacion(6, "Rechazar tarifa negativa", agregar_servicio,
                           servicios, ReservaSala, "Auxiliar", -1000, 8)

        # Se crean reservas para comprobar el cálculo de los costos.
        ejecutar_operacion(7, "Reservar sala por 2 horas", crear_reserva,
                           reservas, clientes[0], servicios[0], 2)
        ejecutar_operacion(8, "Reservar dos equipos por 2 horas", crear_reserva,
                           reservas, clientes[0], servicios[1], 2)
        ejecutar_operacion(9, "Reservar asesoría por 2 horas", crear_reserva,
                           reservas, clientes[0], servicios[2], 2)
        ejecutar_operacion(10, "Rechazar duración de cero horas", crear_reserva,
                           reservas, clientes[0], servicios[0], 0)

        # Se comprueba el comportamiento del sistema cuando una sala no está disponible.
        servicios[0].set_disponible(False)
        ejecutar_operacion(11, "Rechazar sala no disponible", crear_reserva,
                           reservas, clientes[0], servicios[0], 2)

        # Se prueba la cancelación y el cálculo de costos con descuento e impuesto.
        ejecutar_operacion(12, "Cancelar la primera reserva", cancelar_reserva, reservas[0])
        ejecutar_operacion(13, "Calcular costo con descuento e impuesto",
                           servicios[0].calcular_costo, 2, 0.19, 0.10)
    except OSError as error:
        print(f"Problema de acceso a archivos: {error}")
    finally:
        # El resumen también se muestra si ocurre un problema con el archivo de log.
        print(f"\nClientes: {len(clientes)} | Servicios: {len(servicios)} | Reservas: {len(reservas)}")


# Permite seleccionar un elemento de una lista mediante su número.
def elegir_registro(registros, mostrar):
    # Los números del menú empiezan en 1. Las posiciones de la lista empiezan en 0.
    for numero, registro in enumerate(registros, start=1):
        print(f"{numero}. {mostrar(registro)}")

    try:
        numero = int(input("Escribe el número de la lista: "))
    except ValueError as error:
        raise ReservaInvalidaError("Escribe un número entero.") from error

    # Verifica que el número ingresado corresponda a un registro existente.
    if numero < 1 or numero > len(registros):
        raise ReservaInvalidaError("El número no está en la lista.")
    return registros[numero - 1]


# Presenta las opciones principales para que el usuario interactúe con el sistema.
def menu():
    # Se crean las listas que almacenan los clientes y las reservas.
    clientes = []
    reservas = []

    # Tarifas de ejemplo para poder hacer una reserva desde el primer registro.
    servicios = [
        ReservaSala("Principal", 30000, 12),
        AlquilerEquipo("Proyector", 20000, 1),
        AsesoriaEspecializada("Técnica", 50000, "Python"),
    ]

    # Configura el registro de eventos y errores del programa.
    configurar_logger()

    # Mantiene el menú activo hasta que el usuario seleccione la opción de salida.
    while True:
        # input muestra el menú y espera que el usuario escriba una opción.
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
            # Cada condición ejecuta la acción correspondiente a la opción seleccionada.
            if opcion == "1":
                nombre = input("Nombre: ")
                documento = input("Documento: ")
                correo = input("Correo: ")
                print(agregar_cliente(clientes, nombre, documento, correo))
                registrar_evento("Cliente registrado desde el menú")
            elif opcion == "2":
                # Antes de crear una reserva, se verifica que exista un cliente registrado.
                if not clientes:
                    raise ReservaInvalidaError("Primero registra un cliente con la opción 1.")

                print("Elige el cliente.")
                # La función que pasamos indica qué texto mostrar por cada objeto.
                cliente = elegir_registro(clientes, lambda cliente: cliente.describir())
                print("Elige el servicio.")
                servicio = elegir_registro(servicios, lambda servicio: servicio.describir())
                try:
                    # Aceptamos horas decimales con coma o con punto.
                    horas = float(input("Duración en horas: ").strip().replace(",", "."))
                except ValueError as error:
                    raise ReservaInvalidaError("La duración debe ser un número.") from error

                # Se registra la reserva y se informa el resultado de la operación.
                print(crear_reserva(reservas, cliente, servicio, horas))
                registrar_evento("Reserva confirmada desde el menú")
            elif opcion == "3":
                # Consultar la lista no cambia el estado de ninguna reserva.
                if not reservas:
                    print("Todavía no hay reservas.")
                for reserva in reservas:
                    print(reserva.mostrar_reserva())
            elif opcion == "4":
                # Comprueba que existan reservas antes de permitir su cancelación.
                if not reservas:
                    raise ReservaInvalidaError("Todavía no hay reservas para cancelar.")
                reserva = elegir_registro(reservas, Reserva.mostrar_reserva)
                print(cancelar_reserva(reserva))
                registrar_evento("Reserva cancelada desde el menú")
            elif opcion == "5":
                # Inicia la demostración automática de las funcionalidades del sistema.
                ejecutar_demostracion()
            elif opcion == "0":
                print("Programa finalizado.")
                break
            else:
                # Evita que se ingresen opciones que no están disponibles en el menú.
                raise ValueError("Selecciona una opción del 0 al 5.")
        except ValueError as error:
            # Las tres excepciones de la aplicación heredan de ValueError.
            print(f"Rechazado: {error}")
            registrar_error(f"Error en la opción {opcion} del menú")


# Punto de entrada del programa: ejecuta el menú al iniciar main.py.
# También permite importar sus funciones desde otros archivos sin abrir el menú.
if __name__ == "__main__":
    try:
        menu()
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma finalizado.")
    except OSError as error:
        print(f"No se pudo acceder al archivo de log: {error}")

