---
name: astroplan
description: Read, create, edit, validate, summarize, and convert AstroPlan astronomy observing-plan files. Use when Codex works with .astroplan files, portable observing schedules, AstroPlan JSON payloads, schedule interchange, or an implementation that must follow the AstroPlan draft standard.
---

# AstroPlan

Work from the draft specification in `references/astroplan-v1.md`. Preserve
schedule-entry identity, order, timing, coordinates, and extension data.

## Inspect or summarize

1. Parse the file as UTF-8 JSON.
2. Run `scripts/validate_astroplan.py <path>`.
3. Report the title, schedule window, entry count, malformed data, and repeated
   catalog subjects.
4. Treat repeated catalog subjects as intentional separate schedule entries.
5. Describe unknown extension fields without deleting or normalizing them.
6. When `captureStudioFraming` is present, read
   `references/capture-studio-framing-v1.md`. Report the scheduled panel center,
   effective frame dimensions, position angle, telescope, and filters
   separately from the parent catalog subject.

## Create

1. Read `references/astroplan-v1.md`.
2. Use version 1, UTF-8 JSON, J2000 coordinates, and ISO 8601 timestamps.
3. Keep targets in intended execution order.
4. Assign unique `entryId` values when the plan may be edited or round-tripped.
5. Permit the same `catalogId` more than once.
6. Use namespaced keys for experimental application-specific metadata.
7. Write to a new `.astroplan` file unless the user explicitly requests an
   in-place update.
8. Validate the result with the bundled validator.

## Edit

Preserve:

- unknown top-level and entry fields;
- target-array order unless reordering is requested;
- duplicate subjects as distinct entries;
- existing `entryId` values;
- original coordinates and timing fields unless the requested edit changes
  them.

After editing, validate and summarize the material changes.

## Convert

When converting another format into AstroPlan:

- retain source ordering and repeated subjects;
- retain J2000 coordinates at the highest available precision;
- represent timing with offsets from a shared window when possible;
- keep source-only data in a clearly namespaced extension rather than dropping
  it;
- report fields that cannot be represented.

When converting AstroPlan to a less expressive format, warn which timing,
framing, equipment, or extension fields will be lost.

## Validate

Run:

```bash
python3 scripts/validate_astroplan.py plan.astroplan
```

The validator checks the portable core without rejecting unknown extension
fields. It also validates the registered Capture Studio framing extension when
present. A successful structural validation does not prove that every
unregistered extension is understood by the consuming application.
