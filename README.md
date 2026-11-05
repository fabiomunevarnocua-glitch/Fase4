# Fase 4 — Software FJ

Proyecto de programación orientada a objetos para gestionar clientes,
servicios y reservas. Los datos se guardan en listas en memoria.
El archivo de log registra eventos y errores.

## Primera meta

Crear un cliente, reservar una sala durante 2 horas y mostrar el costo.
Si la sala cuesta 30 000 COP por hora, el resultado esperado es 60 000 COP.

## Acuerdo entre módulos

- `Reserva(cliente, servicio, duracion)` recibe un objeto `Cliente`,
  un objeto `Servicio` y la duración en horas.
- `Servicio` declara el método `calcular_costo(duracion)`.
- `Sala`, `Equipo` y `Asesoria` implementan ese método con su propia tarifa.
- Al procesar la reserva, `Reserva` llama a
  `self.servicio.calcular_costo(self.duracion)` y devuelve el costo en COP.
