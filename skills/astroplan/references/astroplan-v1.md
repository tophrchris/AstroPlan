# AstroPlan draft version 1 reference

AstroPlan files are UTF-8 JSON documents with a `.astroplan` extension.

Required root fields:

- `version`: integer `1`
- `title`: non-empty string
- `created`: ISO 8601 timestamp
- `targets`: ordered array

Optional root fields:

- `author`
- `notes`
- `scheduleContext`
- unknown extension fields

When present, `scheduleContext` requires an IANA `timeZone` and may include
`windowStart` and `windowEnd` ISO 8601 timestamps.

Every target occurrence is a separate schedule entry. Never deduplicate entries
by catalog identifier, name, or coordinates. Repeated visits and mosaic panels
may intentionally refer to the same subject.

Array order preserves the author's presentation order. When entries contain
timing, offsets or timestamps determine chronological execution order.

Required target fields:

- `name`
- `catalogId`

Recommended target fields:

- unique `entryId` for editable or round-tripped schedules
- `rightAscensionHours` in `[0, 24)`
- `declinationDegrees` in `[-90, 90]`

Optional target fields:

- `ra`, `dec`
- `startOffsetMinutes`, `durationMinutes`
- `startTime`, `endTime`, `timeZone`
- `notes`
- unknown extension fields

Coordinates are equatorial J2000. Prefer decimal coordinates over display
strings when both are present.

Core target coordinates identify the catalog subject. A registered framing
extension may provide a different scheduled pointing center; use the extension
center for pointing and preserve the core coordinates for subject identity.

When valid shared-window offsets conflict with absolute timestamps, prefer
`windowStart + startOffsetMinutes`.

Unknown fields must not prevent reading. Preserve them when editing or
round-tripping when practical. Use namespaced keys for experimental
application-specific fields.
