# API Caja de Recetas Comunitaria — Mini-auditoría de serialización (Ejemplo en clase)

> **Para instructores:** Escenario paralelo para `ai-eng-backend-serialization`. Misma columna vertebral (inventario → ✅/⚠️/❌ → `response_model` Pydantic → esquemas lectura/escritura separados → documento de auditoría), dominio distinto. Los estudiantes siguen el enunciado completo del monorepo en el `README.md` de la raíz.

_These instructions are also available in [English](./README.md)._

---

## El reto

**Cocina del Barrio** es un servicio FastAPI diminuto para un intercambio comunitario de recetas: los socios publican platos y exploran los de otros. El prototipo devuelve filas SQLAlchemy tal cual — con ruido interno de `owner_id` e `ingredients` anidados completos en el listado. En una sesión, demuestra cómo los serializers convierten un volcado ORM implícito en un contrato listo para producción.

### Nota de alcance

| Proyecto evaluable (`ai-eng-backend-serialization`) | Este ejemplo en clase   |
| --------------------------------------------------- | ----------------------- |
| Superficie API completa del monorepo                | 4 rutas en app toy      |
| Las 3 fases + rúbrica completa                      | Auditar + arreglar 2 ❌ |
| Rama `feature/serialization-audit`                  | Cualquier rama local    |
| Regresión de toda la suite de tests                 | Smoke test de 2 rutas   |

---

## Qué construir

### 1. Inventario (10 min)

Rutas toy (ajusta paths al starter):

| Método | Ruta                        | Propósito                      |
| ------ | --------------------------- | ------------------------------ |
| GET    | `/recipes`                  | Listar recetas                 |
| GET    | `/recipes/{id}`             | Detalle de receta              |
| POST   | `/recipes`                  | Crear receta                   |
| GET    | `/recipes/{id}/ingredients` | Listar ingredientes (opcional) |

- [ ] Clasificar cada ruta ✅ / ⚠️ / ❌ en `docs/serialization-audit.md` (tabla mínima).

### 2. Esquemas (30 min)

- [ ] `RecipeListItem` — `id`, `title`, `cuisine`, `prep_minutes` (sin ingredientes anidados en listado).
- [ ] `RecipeDetail` — añade `description` e `ingredients: list[IngredientLine]` solo en detalle.
- [ ] `RecipeCreate` — entrada: `title`, `cuisine`, `prep_minutes`, `description` (sin `id` ni campos internos de owner).
- [ ] `RecipePublic` — salida tras POST (solo campos seguros).

### 3. Conectar rutas (25 min)

- [ ] `GET /recipes` → `response_model=list[RecipeListItem]`
- [ ] `GET /recipes/{id}` → `response_model=RecipeDetail`
- [ ] `POST /recipes` → body `RecipeCreate`, `response_model=RecipePublic`

Documentar en la auditoría **por qué** el listado eliminó ingredientes anidados.

### 4. Verificar (15 min)

- [ ] Abrir `/docs` — respuestas de ejemplo coinciden con esquemas.
- [ ] Actualizar tabla de auditoría: rutas corregidas en ✅.

---

## Verificar juntos

- [ ] Existe `docs/serialization-audit.md` con columnas antes/después.
- [ ] Al menos dos rutas pasaron de ❌ a ✅.
- [ ] POST usa `RecipeCreate`, no `RecipePublic`, como cuerpo de petición.
- [ ] El JSON del listado no incluye array `ingredients`.

---

## Preguntas de discusión

1. ¿Cuándo justifica un objeto anidado en un endpoint de listado frente a cuándo nunca conviene?
2. ¿Por qué los esquemas de escritura deben omitir campos que asigna el servidor (`id`, `owner_id`)?
3. ¿Cómo ayuda `response_model` a clientes OpenAPI aunque la API no sea pública?
