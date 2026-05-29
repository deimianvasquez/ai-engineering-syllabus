# Auditoría de Serialización del Backend

<!-- hide -->

By [@4GeeksAcademy](https://github.com/4GeeksAcademy) and [other contributors](https://github.com/4GeeksAcademy/backend-serialization-audit/graphs/contributors) at [4Geeks Academy](https://4geeksacademy.com/)

[![build by developers](https://img.shields.io/badge/build_by-Developers-blue)](https://4geeks.com)
[![4Geeks Academy](https://img.shields.io/twitter/follow/4geeksacademy?style=social&logo=x)](https://x.com/4geeksacademy)

_These instructions are [available in English](./README.md)._

**Antes de empezar**: 📗 [Lee las instrucciones](https://4geeks.com/lesson/how-to-start-a-project) sobre cómo iniciar un proyecto de código.

<!-- endhide -->

---

## 🎯 Tu reto

El backend que lleva semanas construyéndose está a punto de recibir usuarios reales. Antes de eso, tu CTO ha identificado un problema crítico: varios endpoints de la API devuelven objetos de base de datos sin ningún control de forma, sin filtrado de campos y sin protección frente a la exposición de campos internos del modelo. En un entorno de demo con poco tráfico, esto es invisible. A escala, genera cuellos de botella de rendimiento, riesgos de seguridad y contratos frágiles con el cliente.

Tu tarea es liderar una auditoría de serialización del backend. El objetivo no es reescribir nada desde cero, sino inspeccionar cada endpoint existente con criterio técnico y llevar la API a estándares de producción.

> Tu CTO ha compartido el siguiente briefing:
>
> #### Qué necesitamos
>
> - Una auditoría escrita que identifique cada endpoint y su estado de serialización actual.
> - Una clasificación de cada endpoint: cuáles exponen campos innecesarios, cuáles carecen de un esquema de respuesta definido y cuáles ya están bien definidos.
> - Para cada endpoint que requiera trabajo, una nota sobre _qué tipo_ de mejora es necesaria — no solo "necesita serializer", sino _por qué_ y _cómo debería ser el payload de salida_.
>
> #### Entregable mínimo
>
> Cada endpoint de la API debe tener un serializer de respuesta explícito definido antes de que esta tarea se considere completada. Ningún endpoint debe devolver un objeto ORM en crudo.
>
> #### Qué significa hacerlo bien
>
> Más allá del mínimo, espero optimización del payload donde importa: relaciones anidadas aplanadas cuando el cliente no necesita el objeto completo, endpoints de listado que devuelven solo los campos que los consumidores realmente usan, y endpoints de escritura que aceptan únicamente los campos que deben aceptar.

Este es el tipo de revisión que diferencia una API que funciona de una API en la que se puede confiar. Asume la responsabilidad de toda la superficie de tu backend y llévala al nivel que merecen tu frontend — y tus usuarios.

### ¿Qué son los serializers y por qué importan aquí?

Los serializers definen el contrato entre tu backend y todo lo que lo consume. En FastAPI, los modelos Pydantic cumplen este rol: validan la entrada, dan forma a la salida y hacen que el comportamiento de la API sea explícito y testeable. Sin ellos, tu API devuelve implícitamente lo que produce el ORM, lo que puede incluir IDs internas, contraseñas hasheadas, ruido relacional y nombres de campos inestables. Con alto tráfico, esto también significa serializar más datos de los que el cliente jamás solicitó.

Una capa de serializers bien diseñada implica:
- **Los clientes reciben solo lo que necesitan** — payloads más pequeños, respuestas más rápidas.
- **Los cambios internos del modelo no rompen el contrato de la API** — el serializer absorbe la diferencia.
- **Los campos sensibles nunca se exponen accidentalmente** — el esquema es la fuente de verdad.

Al auditar, piensa en tres niveles: _qué recibe este endpoint_, _qué debería devolver_ y _qué está devolviendo realmente hoy_.

---

## 🌱 Cómo iniciar el proyecto

Este proyecto se construye sobre el monorepo existente de tu empresa. No necesitas forkear un repositorio nuevo.

1. Abre tu monorepo en tu entorno de desarrollo (Codespaces o local).
2. Navega a tu aplicación FastAPI — normalmente en `/apps/<nombre-de-tu-app>/` o en la carpeta de backend establecida en milestones anteriores.
3. Asegúrate de que tu entorno está en funcionamiento y tus endpoints existentes son accesibles antes de comenzar la auditoría.
4. Trabaja en una rama dedicada: `git checkout -b feature/serialization-audit`.

---

## 💻 Qué debes hacer

### Fase 1 — Auditoría

- [ ] Lista todos los endpoints de tu aplicación FastAPI (ruta, método y propósito).
- [ ] Para cada endpoint, documenta su comportamiento de respuesta actual: ¿usa `response_model`? ¿Devuelve un objeto ORM en crudo, un dict o un esquema tipado?
- [ ] Clasifica cada endpoint en uno de estos tres estados:
  - **✅ Ya serializado** — tiene un `response_model` explícito y el esquema es adecuado.
  - **⚠️ Parcialmente serializado** — tiene un response model pero está incompleto, expone campos innecesarios o no coincide con lo que necesita el cliente.
  - **❌ Sin serializar** — devuelve un objeto ORM en crudo o un dict sin tipado.
- [ ] Registra los resultados de la auditoría en un archivo Markdown en `docs/serialization-audit.md`.

### Fase 2 — Implementación

- [ ] Crea o actualiza los esquemas Pydantic para cada endpoint clasificado como ❌ o ⚠️.
- [ ] Asegúrate de que cada endpoint tiene un `response_model` explícito declarado en su decorador de ruta.
- [ ] Para endpoints de listado: define un esquema que devuelva solo los campos que los consumidores necesitan. Evita devolver objetos anidados completos cuando una representación plana es suficiente.
- [ ] Para endpoints de escritura (POST, PUT, PATCH): define un esquema de entrada separado que acepte únicamente los campos que deben poder escribirse. No reutilices el esquema de respuesta como esquema de entrada.
- [ ] Asegúrate de que ningún endpoint exponga campos sensibles (por ejemplo, contraseñas hasheadas, tokens internos, claves foráneas en bruto cuando hay un objeto anidado disponible).
- [ ] Cuando una relación sea necesaria en la respuesta, decide explícitamente: devolver el objeto anidado completo, devolver solo el ID relacionado o devolver una proyección plana — y documenta esa decisión en tu archivo de auditoría.

### Fase 3 — Verificación

- [ ] Confirma que todos los endpoints siguen pasando los tests existentes tras los cambios de esquema.
- [ ] Prueba manualmente al menos tres endpoints usando la documentación interactiva de FastAPI (`/docs`) y verifica que el shape de la respuesta coincide con el esquema definido.
- [ ] Actualiza el documento de auditoría para marcar todos los endpoints como ✅ una vez completada la implementación.

---

## ✅ Qué vamos a evaluar

- [ ] Cada endpoint de la aplicación tiene un `response_model` explícito declarado.
- [ ] Los esquemas Pydantic están definidos tanto para entrada como para salida donde corresponde — los esquemas de entrada y salida no se confunden entre sí.
- [ ] Los esquemas de endpoints de listado devuelven solo los campos necesarios para el consumidor — sin anidado innecesario ni over-fetching.
- [ ] Ningún endpoint expone campos sensibles del modelo en su esquema de respuesta.
- [ ] El documento de auditoría de serialización (`docs/serialization-audit.md`) existe, lista todos los endpoints, su estado original y los cambios aplicados.
- [ ] La aplicación sigue funcionando correctamente después de todos los cambios de esquema — sin regresiones.

> **Nota:** La calidad del documento de auditoría se evalúa como un entregable en sí mismo. Una implementación completa sin registro de auditoría no es suficiente.

---

## 📦 Cómo entregar

Sube tu rama a GitHub y abre un pull request contra `main` con el título `feat: serialization audit and implementation`. Comparte la URL del PR según las instrucciones de tu instructor.

---

Este y muchos otros proyectos son construidos por estudiantes como parte de los [Coding Bootcamps](https://4geeksacademy.com/) de 4Geeks Academy. Encuentra más acerca de los [cursos](https://4geeksacademy.com/es/comparar-programas) de [Ingeniería de IA](https://4geeksacademy.com/es/coding-bootcamps/ingenieria-ia), [Data Science & Machine Learning](https://4geeksacademy.com/es/coding-bootcamps/curso-datascience-machine-learning), [Ciberseguridad](https://4geeksacademy.com/es/coding-bootcamps/curso-ciberseguridad) y [Full-Stack Software Developer con IA](https://4geeksacademy.com/es/coding-bootcamps/programador-full-stack).
