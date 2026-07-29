# Implement AstroPlan in TypeScript

Implement AstroPlan draft version 1 for both browser and Node-compatible
TypeScript consumers.

Use `SPECIFICATION.md`, `schema/astroplan-v1.schema.json`, and `examples/` as
the source of truth.

Requirements:

1. Export TypeScript types for the root payload, schedule context, and target
   entries.
2. Add runtime validation using the project's existing validator, or a small
   schema-backed adapter if no validator exists.
3. Preserve unknown object properties when parsing and serializing. With Zod,
   use pass-through object behavior rather than stripping extensions.
4. Preserve array order and repeated `catalogId` values. Never key the schedule
   solely by subject identity.
5. Treat ISO 8601 strings as strings at the interchange boundary. Convert to
   `Date` only in application-facing helpers.
6. Validate coordinate ranges and timing field types.
7. Provide browser download and file-upload helpers without coupling the core
   models to React, Vue, Svelte, or another UI framework.
8. Test every shared example, duplicate-subject schedules, unknown fields,
   offset timing, and encode/decode round trips.

Keep application-specific framing or execution data in namespaced extension
fields until it is part of the common specification.
