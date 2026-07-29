# AstroPlan draft specification

Status: Draft version 1  
File extension: `.astroplan`  
Encoding: UTF-8 JSON  
Recommended MIME type: `application/vnd.astroplan+json`

AstroPlan is a portable representation of an ordered astronomy observing plan.
It is intended to carry enough information for another application to identify
subjects, preserve sequence, and optionally reconstruct schedule timing without
requiring either application to understand every private feature of the other.

Normative terms such as **MUST**, **SHOULD**, and **MAY** are used in their
ordinary standards-document sense.

## 1. Document model

An AstroPlan file MUST contain one JSON object with these top-level fields.

| Field | Type | Use | Description |
| --- | --- | --- | --- |
| `version` | integer | Required | AstroPlan major schema version. This draft uses `1`. |
| `title` | string | Required | Human-readable plan title. |
| `author` | string | Optional | Application, service, or person that created the plan. |
| `created` | ISO 8601 timestamp | Required | File creation timestamp. |
| `notes` | string | Optional | Plan-level notes. |
| `scheduleContext` | object | Optional | Shared time zone and observing window. |
| `targets` | array | Required | Ordered schedule entries. |

The order of `targets` is the intended plan order.

Every occurrence in the `targets` array is a distinct schedule entry. Multiple
entries MAY refer to the same catalog subject and MAY use the same `catalogId`.
Readers MUST NOT deduplicate entries merely because their subject identifiers
or coordinates match. This supports repeated visits, mosaics, alternate
framings, filters, and overlapping schedule entries.

## 2. Schedule context

Applications exchanging only an ordered target list MAY omit
`scheduleContext`.

| Field | Type | Use | Description |
| --- | --- | --- | --- |
| `timeZone` | IANA time-zone string | Required when the object exists | Example: `America/New_York`. |
| `windowStart` | ISO 8601 timestamp | Optional | Start of the observing window. Required when target offsets are used. |
| `windowEnd` | ISO 8601 timestamp | Optional | End of the observing window. |

## 3. Target entries

| Field | Type | Use | Description |
| --- | --- | --- | --- |
| `entryId` | string | Optional, recommended for editors | Stable identity for this schedule occurrence. It identifies the entry, not the astronomical subject. |
| `name` | string | Required | Display name. |
| `catalogId` | string | Required | Stable catalog identifier or application-level subject key. |
| `ra` | string | Optional | Human-readable J2000 right ascension, preferably sexagesimal. |
| `dec` | string | Optional | Human-readable J2000 declination, preferably sexagesimal. |
| `rightAscensionHours` | number | Recommended | J2000 right ascension in decimal hours, normalized to `[0, 24)`. |
| `declinationDegrees` | number | Recommended | J2000 declination in decimal degrees, from `-90` to `+90`. |
| `startOffsetMinutes` | integer | Optional | Scheduled start offset from `scheduleContext.windowStart`. |
| `durationMinutes` | integer | Optional | Planned duration for this schedule entry. |
| `startTime` | ISO 8601 timestamp | Optional | Absolute scheduled start, used for display or import fallback. |
| `endTime` | ISO 8601 timestamp | Optional | Absolute scheduled end, used for display or import fallback. |
| `timeZone` | IANA time-zone string | Optional | Entry-level override, normally matching the schedule context. |
| `notes` | string | Optional | Entry-specific planning notes. |

Writers that support editing or round trips SHOULD provide a unique `entryId`
for every schedule entry. Readers MUST still preserve separate occurrences when
older files omit `entryId`.

Coordinates MUST describe the scheduled center point when the entry represents
a custom framing or mosaic panel. Applications MAY carry the parent subject's
identity and richer framing metadata in extension fields.

## 4. Coordinates

Machine-readable coordinates use the J2000 equatorial reference frame.

- `rightAscensionHours` is expressed in decimal hours.
- `declinationDegrees` is expressed in decimal degrees.
- Decimal fields are preferred for interchange.
- `ra` and `dec` are human-readable companions and fallbacks.

When decimal and display-string values disagree, readers SHOULD prefer the
decimal values.

## 5. Timing

- Target-array order defines sequence.
- When `windowStart` and `startOffsetMinutes` are both present, their
  combination is the preferred portable start time.
- `durationMinutes` describes how long the entry is scheduled.
- `startTime` and `endTime` are useful display and fallback values.
- If offset timing conflicts with absolute timestamps, a reader SHOULD prefer
  offsets when a valid shared schedule window exists.
- Overlapping entries are valid. Readers MUST NOT discard an entry solely
  because it overlaps another.

## 6. Extensions and forward compatibility

Readers MUST ignore unknown top-level and target-level fields when they can
safely continue. Editors SHOULD preserve unknown fields during a lossless
round trip.

Experimental application-specific fields SHOULD use a namespaced key, such as:

```json
{
  "vendor.example.framing": {
    "centerRightAscensionHours": 21.64,
    "centerDeclinationDegrees": 57.45,
    "rotationDegrees": 12.5
  }
}
```

This rule allows framing, mosaic, filter, exposure, equipment, and execution
metadata to evolve before every application supports the same feature set.
Candidate common extensions may graduate into a future revision of the core
specification after interoperability testing.

## 7. Target resolution

Importers SHOULD attempt to resolve a subject in this order:

1. exact or normalized `catalogId`;
2. exact `name`;
3. J2000 coordinates within an application-appropriate tolerance.

Importers SHOULD clearly surface unresolved entries instead of silently
dropping them. Resolving several entries to the same local catalog subject does
not make those schedule entries duplicates.

## 8. Version handling

Writers targeting this draft MUST include `version: 1`.

Readers SHOULD reject an unsupported major version only when they cannot safely
continue. Unknown fields alone are not a reason to reject a document.

## 9. Minimal example

```json
{
  "version": 1,
  "title": "Galaxy Starter Plan",
  "author": "Example Planner",
  "created": "2026-07-28T18:30:00Z",
  "targets": [
    {
      "entryId": "m81-first-pass",
      "name": "Bode's Galaxy",
      "catalogId": "M81",
      "rightAscensionHours": 9.925,
      "declinationDegrees": 69.065
    },
    {
      "entryId": "m82-first-pass",
      "name": "Cigar Galaxy",
      "catalogId": "M82",
      "rightAscensionHours": 9.9337,
      "declinationDegrees": 69.6797
    }
  ]
}
```

## 10. Media type and platform registration

Applications MAY register `.astroplan` as a document type and associate the
recommended MIME type. Platform-specific identifiers are outside the portable
payload specification.
