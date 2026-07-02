# Cola del Mostrador de Biblioteca — Cola por Etiqueta de Servicio (Ejemplo de Clase)

> **Para instructores:** Escenario paralelo en aula para `branch-queue`. Misma columna vertebral (una `deque` por etiqueta de servicio, contador global de tickets, cinco operaciones núcleo, menú CLI, estructuras stdlib, debate de concurrencia), dominio distinto. Los estudiantes siguen el enunciado bancario completo en `README.md` de la raíz del proyecto.

_Estas instrucciones también están disponibles en [inglés](./README.md)._

---

## El reto

Una biblioteca de barrio sigue repartiendo tickets de papel en el mostrador de ayuda. Los usuarios esperan por **devoluciones**, **recogida de reservas** o **nuevas tarjetas de biblioteca** — cada empleado atiende solo un tipo de servicio. Tu demo en vivo modela un **gestor de colas en terminal** (sin UI) donde cada empleado llama al siguiente usuario al instante, sin recorrer toda la sala.

> **Según la especificación de la supervisora del mostrador:**
>
> - Cada usuario recibe una **etiqueta de servicio**: `devolucion`, `recogida` o `nueva_tarjeta`.
> - Registrar nombre, etiqueta y hora de llegada.
> - Los números de ticket son globales (1, 2, 3, …) entre todos los servicios.
> - Cada empleado llama al siguiente usuario **solo de su cola de servicio** — FIFO dentro de esa etiqueta.
> - Operaciones: emitir ticket, llamar siguiente, peek siguiente, listar en espera (agrupado), stats.

### Nota de alcance

Pensado para **una sesión en vivo (~60–90 min)**. Mismos patrones que el proyecto estudiante, pero:

- Dominio de **mostrador de biblioteca**, no sucursal bancaria.
- Un solo archivo `library_queue.py` — sin repo plantilla.
- `DESIGN.md` se discute **en voz alta en clase**; los estudiantes lo escriben en el proyecto real.
- Menú CLI de cinco opciones como tarea si falta tiempo; la demo en vivo necesita al menos emitir ticket / llamar siguiente / ver espera.

---

## Qué construir

### Modelo de datos

- [ ] Dataclass `PatronTicket`: `number` (int), `patron_name`, `service_tag` (`"devolucion"` | `"recogida"` | `"nueva_tarjeta"`), `issued_at` (`datetime`).
- [ ] Clase `LibraryDeskQueue` con una `deque` interna por etiqueta y contador global de tickets.

### Operaciones de cola

- [ ] `issue_ticket(patron_name, service_tag)` — encola en la `deque` correcta; devuelve el ticket.
- [ ] `call_next(service_tag)` — desencola y devuelve el siguiente de esa etiqueta; error descriptivo si está vacía.
- [ ] `peek_next(service_tag)` — siguiente sin extraer.
- [ ] `list_waiting()` — dict con cada etiqueta → lista ordenada de tickets en espera.
- [ ] `stats()` — conteo por etiqueta más `"total"`.

| Método         | Comportamiento esperado                                           |
| -------------- | ----------------------------------------------------------------- |
| `issue_ticket` | Ticket en la `deque` del servicio; número incrementa globalmente  |
| `call_next`    | `popleft` solo de la `deque` de la etiqueta pedida                |
| `peek_next`    | Frente de esa `deque`, sin mutación                               |
| `list_waiting` | `{devolucion: [...], recogida: [...], nueva_tarjeta: [...]}` FIFO |
| `stats`        | p. ej. `{devolucion: 1, recogida: 0, nueva_tarjeta: 2, total: 3}` |

### CLI (mínimo para demo en vivo)

- [ ] Menú en bucle:
  - Emitir ticket (nombre + etiqueta).
  - Llamar siguiente (`call_next` — pedir etiqueta).
  - Ver lista de espera (`list_waiting`).
  - _(Tarea si falta tiempo: stats + salida pulida)_

### Correctitud (demo ante la clase)

- [ ] Dos usuarios de `devolucion` → el primero emitido se llama primero.
- [ ] `call_next("recogida")` no quita a nadie de `devolucion`.
- [ ] Los números de ticket no se repiten entre etiquetas distintas.
- [ ] `call_next` / `peek_next` vacíos → capturados en CLI, sin crash.
- [ ] Etiqueta inválida rechazada al emitir ticket.

⚠️ **Solo stdlib:** `collections.deque`, `datetime`.

---

## Verificar juntos

- [ ] Emitir ticket de recogida, luego de devolución → `call_next("devolucion")` atiende devolución; recogida sigue esperando.
- [ ] Dos tickets de recogida con 30 s de diferencia → el primero emitido se llama primero con `call_next("recogida")`.
- [ ] El orden de `list_waiting` coincide con FIFO esperado en cada etiqueta tras mezclar inserciones.
- [ ] `stats()` coincide con la cola visible.
- [ ] `call_next` en etiqueta vacía imprime mensaje amable; el programa continúa.
- [ ] Etiqueta inválida (p. ej. `renovacion`) rechazada sin crash.

---

## Preguntas de debate

1. ¿Por qué una única lista de todos los usuarios en espera hace `call_next` lento cuando la sala se llena? ¿Qué operación pasa a O(n)?
2. ¿En qué se diferencia una cola por etiqueta de servicio de una cola de **prioridad** (como niveles de triaje)? ¿Cuándo usarías cada una?
3. Si dos empleados comparten la misma `deque` de `devolucion`, ¿qué orden de mutación en `call_next` evita llamar dos veces al mismo usuario?
