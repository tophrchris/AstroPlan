# Implement AstroPlan in Kotlin

Implement AstroPlan draft version 1 in this Kotlin codebase.

Use `SPECIFICATION.md`, `schema/astroplan-v1.schema.json`, and every file in
`examples/` as the compatibility contract.

Requirements:

1. Create `kotlinx.serialization` models for the payload, schedule context, and
   ordered target entries.
2. Configure JSON parsing to ignore unknown keys. For an editor or converter,
   retain the original `JsonElement` data needed to preserve unknown fields.
3. Preserve entry order, repeated subjects, overlapping timing, and optional
   `entryId`.
4. Do not use `catalogId` as a unique collection key.
5. Parse timestamps with explicit offsets and keep interchange strings
   lossless where possible.
6. Validate J2000 coordinate ranges and required fields with actionable errors.
7. Separate serialization from Android UI, persistence, and networking layers.
8. Add tests using all shared examples plus duplicate-subject, unknown-field,
   unsupported-version, and round-trip fixtures.

Document and namespace any app-specific extensions rather than adding private
required fields to the core payload.
