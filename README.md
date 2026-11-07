# Fase 4 - Cliente reserva de salas

Proyecto de programación orientada a objetos para gestionar clientes,
servicios y reservas. Los datos se guardan en listas en memoria.
El archivo de log registra eventos y errores.

## Distribución del trabajo

| Archivo | Clase / Módulo | Funciones o métodos | Responsable |
|---|---|---|---|
| `cliente.py` | Cliente | `__init__()`<br>`get_nombre()`<br>`set_nombre()`<br>`get_documento()`<br>`set_documento()`<br>`get_correo()`<br>`set_correo()`<br>`validar_nombre()`<br>`validar_documento()`<br>`validar_correo()`<br>`mostrar_datos()` | **Fabio** |
| `servicio.py` | Servicio (abstracta) | `__init__()`<br>`calcular_costo()`<br>`describir()`<br>`validar_parametros()` | **Lesdy** |
| `servicio.py` | ReservaSala | `__init__()`<br>`calcular_costo()`<br>`describir()`<br>`validar_parametros()` | **Lesdy** |
| `servicio.py` | AlquilerEquipo | `__init__()`<br>`calcular_costo()`<br>`describir()`<br>`validar_parametros()` | **Disponible — Integrante 3** |
| `servicio.py` | AsesoriaEspecializada | `__init__()`<br>`calcular_costo()`<br>`describir()`<br>`validar_parametros()` | **Disponible — Integrante 4** |
| `reserva.py` | Reserva | `__init__()`<br>`confirmar()`<br>`cancelar()`<br>`procesar()`<br>`mostrar_reserva()` | **Disponible — Integrante 4** |
| `excepciones.py` | Excepciones personalizadas | Definición de excepciones | **Disponible — Integrante 5** |
| `logger_config.py` | Logger | `configurar_logger()`<br>`registrar_evento()`<br>`registrar_error()` | **Disponible — Integrante 5** |

Cada integrante trabajará en su propia rama y realizará sus commits desde su cuenta.
Los cambios se revisarán y probarán antes de integrarlos a `main`.

## Primera meta

Crear un cliente, reservar una sala durante 2 horas y mostrar el costo.
Si la sala cuesta 30 000 COP por hora, el resultado esperado es 60 000 COP.

## Acuerdo entre módulos

- `Reserva(cliente, servicio, duracion)` recibe un objeto `Cliente`,
  un objeto `Servicio` y la duración en horas.
- `Servicio` declara el método `calcular_costo(duracion)`.
- `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` implementan ese método con su propia tarifa.
- Al procesar la reserva, `Reserva` llama a
  `self.servicio.calcular_costo(self.duracion)` y devuelve el costo en COP.
