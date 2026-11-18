import logging  # Módulo de Python para guardar mensajes con fecha y nivel.


def configurar_logger():
    # La configuración se comparte entre todas las operaciones.
    logger = logging.getLogger("fase4")
    if not logger.handlers:  # Agrega el archivo una sola vez para evitar líneas duplicadas.
        # El archivo conserva los mensajes de cada ejecución en UTF-8.
        archivo = logging.FileHandler("fase4.log", encoding="utf-8")
        archivo.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(archivo)
        logger.setLevel(logging.INFO)  # Guarda eventos normales y errores.
        logger.propagate = False  # Evita que otros registradores repitan el mensaje.
    return logger


def registrar_evento(mensaje):
    configurar_logger().info(mensaje)  # INFO identifica una operación correcta.


def registrar_error(mensaje):
    # Se llama desde except para guardar el error y su causa, si la tiene.
    configurar_logger().exception(mensaje)
