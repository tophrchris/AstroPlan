# Implement AstroPlan in Python

Implement AstroPlan draft version 1 support in this Python project.

Use `SPECIFICATION.md`, `schema/astroplan-v1.schema.json`, and the files in
`examples/` as the compatibility contract.

Requirements:

1. Provide typed payload, schedule-context, and target-entry models using
   dataclasses or Pydantic, following the project's existing conventions.
2. Preserve target order, repeated subjects, overlapping entries, and optional
   `entryId` values.
3. Parse ISO 8601 timestamps with offsets correctly and never silently apply
   the host machine's local time zone.
4. Accept unknown fields. Preserve them during read-modify-write workflows.
5. Validate J2000 decimal coordinate ranges.
6. Prefer portable offset timing when it conflicts with absolute timestamps.
7. Expose clear parse and validation errors with a JSON path to the problem.
8. Add reader, writer, validator, and round-trip tests using every shared
   example plus fixtures for repeated catalog IDs and unknown fields.
9. Keep optional JSON Schema validation behind a documented dependency if the
   base project avoids third-party packages.

Do not deduplicate by `catalogId`, name, or coordinates. A target-array
occurrence is a schedule entry, not merely a catalog lookup result.
