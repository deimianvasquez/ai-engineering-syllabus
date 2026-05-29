# Community Recipe Box API — Serialization Mini-Audit (Class Example)

> **For instructors:** Parallel classroom scenario for `ai-eng-backend-serialization`. Same spine (endpoint inventory → ✅/⚠️/❌ → Pydantic `response_model` → separate read/write schemas → audit doc), different domain. Students still follow the full monorepo brief in the project root `README.md`.

_Estas instrucciones también están disponibles en [español](./README.es.md)._

---

## The challenge

**Neighbor Cook** is a tiny FastAPI service for a community recipe swap: members post recipes and browse others' dishes. The prototype returns SQLAlchemy rows directly — including internal `owner_id` blobs and full nested `ingredients` on list views. In one session, demo how serializers turn an implicit ORM dump into a production-safe contract.

### Scope note

| Graded project (`ai-eng-backend-serialization`) | This class example        |
| ----------------------------------------------- | ------------------------- |
| Full company monorepo API surface               | 4 routes on a toy app     |
| All phases + full rubric                        | Audit + fix 2 ❌ routes   |
| Branch `feature/serialization-audit`            | Any local branch          |
| Complete test suite regression                  | Smoke test 2 fixed routes |

---

## What to build

### 1. Inventory (10 min)

Toy routes (adjust paths to your starter):

| Method | Path                        | Purpose                             |
| ------ | --------------------------- | ----------------------------------- |
| GET    | `/recipes`                  | List recipes                        |
| GET    | `/recipes/{id}`             | Recipe detail                       |
| POST   | `/recipes`                  | Create recipe                       |
| GET    | `/recipes/{id}/ingredients` | List ingredients (optional stretch) |

- [ ] Classify each route ✅ / ⚠️ / ❌ in `docs/serialization-audit.md` (create a minimal table).

### 2. Schemas (30 min)

- [ ] `RecipeListItem` — `id`, `title`, `cuisine`, `prep_minutes` (no nested ingredients on list).
- [ ] `RecipeDetail` — adds `description` and `ingredients: list[IngredientLine]` only on detail route.
- [ ] `RecipeCreate` — input: `title`, `cuisine`, `prep_minutes`, `description` (no `id`, no owner internals).
- [ ] `RecipePublic` — output after POST (mirror safe fields, never echo ORM-only columns).

### 3. Wire routes (25 min)

- [ ] `GET /recipes` → `response_model=list[RecipeListItem]`
- [ ] `GET /recipes/{id}` → `response_model=RecipeDetail`
- [ ] `POST /recipes` → body `RecipeCreate`, `response_model=RecipePublic`

Document in the audit file **why** list dropped nested ingredients.

### 4. Verify (15 min)

- [ ] Open `/docs` — response samples match schemas.
- [ ] Update audit table: fixed routes marked ✅.

---

## Verify together

- [ ] `docs/serialization-audit.md` exists with before/after columns.
- [ ] At least two routes moved from ❌ to ✅.
- [ ] POST uses `RecipeCreate`, not `RecipePublic`, as request body.
- [ ] List response JSON has no `ingredients` array.

---

## Discussion questions

1. When is a nested object in a list endpoint justified vs. always wrong?
2. Why must write schemas omit fields that the server assigns (`id`, `owner_id`)?
3. How does `response_model` help OpenAPI clients even if you never publish the API publicly?
