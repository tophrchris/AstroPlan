# Implement AstroPlan in Swift

Implement AstroPlan draft version 1 support in this Swift codebase.

Use these authoritative inputs:

- `SPECIFICATION.md`
- `schema/astroplan-v1.schema.json`
- every file under `examples/`

Requirements:

1. Model the payload, schedule context, and ordered target entries with
   `Codable`, `Equatable`, and `Sendable` where appropriate.
2. Decode and encode ISO 8601 timestamps consistently.
3. Preserve target-array order and allow multiple entries with the same
   `catalogId`. Treat entry identity separately from subject identity.
4. Ignore unknown fields while reading. If the feature edits and rewrites
   arbitrary AstroPlan files, preserve unknown fields using a lossless JSON
   representation or documented extension container.
5. Prefer decimal J2000 coordinates over display strings when both exist.
6. Prefer `windowStart + startOffsetMinutes` over conflicting absolute target
   timestamps.
7. Surface unresolved entries instead of silently removing them.
8. Keep the import boundary independent from UI and persistence models.
9. Add fixtures and tests for:
   - both shared example files;
   - a minimal target list;
   - repeated entries for the same catalog subject;
   - overlapping schedule entries;
   - unknown top-level and target fields;
   - unsupported major versions;
   - encode/decode round trips.

Do not invent required fields beyond the draft specification. Document any
application-specific extension and namespace it.
