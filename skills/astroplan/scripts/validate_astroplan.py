#!/usr/bin/env python3
"""Validate the portable core of an AstroPlan draft version 1 document."""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def parse_timestamp(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{path}: expected an ISO 8601 string")
        return
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        errors.append(f"{path}: invalid ISO 8601 timestamp")
        return
    if parsed.tzinfo is None:
        errors.append(f"{path}: timestamp must include an offset or Z")


def require_string(
    container: dict[str, Any],
    key: str,
    path: str,
    errors: list[str],
) -> None:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}.{key}: expected a non-empty string")


def optional_number(
    container: dict[str, Any],
    key: str,
    path: str,
    errors: list[str],
    minimum: float,
    maximum: float,
    maximum_inclusive: bool = True,
) -> None:
    if key not in container:
        return
    value = container[key]
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
    ):
        errors.append(f"{path}.{key}: expected a finite number")
        return
    exceeds_maximum = value > maximum if maximum_inclusive else value >= maximum
    if value < minimum or exceeds_maximum:
        upper = "]" if maximum_inclusive else ")"
        errors.append(f"{path}.{key}: expected range [{minimum}, {maximum}{upper}")


def require_number(
    container: dict[str, Any],
    key: str,
    path: str,
    errors: list[str],
    minimum: float,
    maximum: float,
    maximum_inclusive: bool = True,
) -> None:
    if key not in container:
        errors.append(f"{path}.{key}: required")
        return
    optional_number(
        container,
        key,
        path,
        errors,
        minimum,
        maximum,
        maximum_inclusive,
    )


def optional_integer(
    container: dict[str, Any],
    key: str,
    path: str,
    errors: list[str],
    minimum: int | None = None,
) -> None:
    if key not in container:
        return
    value = container[key]
    if isinstance(value, bool) or not isinstance(value, int):
        errors.append(f"{path}.{key}: expected an integer")
        return
    if minimum is not None and value < minimum:
        errors.append(f"{path}.{key}: expected a value >= {minimum}")


def validate_capture_studio_framing(
    framing: Any,
    path: str,
    errors: list[str],
) -> None:
    if not isinstance(framing, dict):
        errors.append(f"{path}: expected an object")
        return

    if framing.get("schemaVersion") != 1:
        errors.append(f"{path}.schemaVersion: expected integer 1")

    for key in (
        "source",
        "subjectCatalogId",
        "subjectDisplayName",
        "panelId",
        "panelTitle",
        "telescopeId",
        "telescopeName",
        "frameRotationConvention",
    ):
        require_string(framing, key, path, errors)

    if framing.get("frameRotationConvention") != "degreesEastOfJ2000North":
        errors.append(
            f"{path}.frameRotationConvention: "
            "expected 'degreesEastOfJ2000North'"
        )

    require_number(
        framing,
        "panelCenterRightAscensionHoursJ2000",
        path,
        errors,
        0,
        24,
        maximum_inclusive=False,
    )
    require_number(
        framing,
        "panelCenterDeclinationDegreesJ2000",
        path,
        errors,
        -90,
        90,
    )

    for key in ("frameWidthDegrees", "frameHeightDegrees", "frameScale"):
        require_number(
            framing,
            key,
            path,
            errors,
            0,
            math.inf,
            maximum_inclusive=True,
        )
        value = framing.get(key)
        if (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and value <= 0
        ):
            errors.append(f"{path}.{key}: expected a value > 0")

    for key in ("frameRotationDegrees", "frameOffsetXDegrees", "frameOffsetYDegrees"):
        require_number(
            framing,
            key,
            path,
            errors,
            -math.inf,
            math.inf,
        )

    for key in ("filterIds", "filterNames"):
        value = framing.get(key)
        if not isinstance(value, list) or not all(
            isinstance(item, str) for item in value
        ):
            errors.append(f"{path}.{key}: expected an array of strings")


def validate_payload(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["$: expected one JSON object"]

    if payload.get("version") != 1:
        errors.append("$.version: expected integer 1")
    require_string(payload, "title", "$", errors)
    if "created" not in payload:
        errors.append("$.created: required")
    else:
        parse_timestamp(payload["created"], "$.created", errors)

    schedule_context = payload.get("scheduleContext")
    if schedule_context is not None:
        if not isinstance(schedule_context, dict):
            errors.append("$.scheduleContext: expected an object")
        else:
            require_string(
                schedule_context,
                "timeZone",
                "$.scheduleContext",
                errors,
            )
            for key in ("windowStart", "windowEnd"):
                if key in schedule_context:
                    parse_timestamp(
                        schedule_context[key],
                        f"$.scheduleContext.{key}",
                        errors,
                    )

    targets = payload.get("targets")
    if not isinstance(targets, list):
        errors.append("$.targets: expected an array")
        return errors

    entry_ids: set[str] = set()
    for index, target in enumerate(targets):
        path = f"$.targets[{index}]"
        if not isinstance(target, dict):
            errors.append(f"{path}: expected an object")
            continue
        require_string(target, "name", path, errors)
        require_string(target, "catalogId", path, errors)

        entry_id = target.get("entryId")
        if entry_id is not None:
            if not isinstance(entry_id, str) or not entry_id.strip():
                errors.append(f"{path}.entryId: expected a non-empty string")
            elif entry_id in entry_ids:
                errors.append(f"{path}.entryId: duplicate entry identity {entry_id!r}")
            else:
                entry_ids.add(entry_id)

        optional_number(
            target,
            "rightAscensionHours",
            path,
            errors,
            0,
            24,
            maximum_inclusive=False,
        )
        optional_number(
            target,
            "declinationDegrees",
            path,
            errors,
            -90,
            90,
        )
        optional_integer(target, "startOffsetMinutes", path, errors)
        optional_integer(target, "durationMinutes", path, errors, minimum=0)

        for key in ("startTime", "endTime"):
            if key in target:
                parse_timestamp(target[key], f"{path}.{key}", errors)

        if "captureStudioFraming" in target:
            validate_capture_studio_framing(
                target["captureStudioFraming"],
                f"{path}.captureStudioFraming",
                errors,
            )

    return errors


def validate_file(path: Path) -> list[str]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"{path}: file not found"]
    except UnicodeDecodeError:
        return [f"{path}: expected UTF-8 text"]
    except json.JSONDecodeError as error:
        return [f"{path}:{error.lineno}:{error.colno}: {error.msg}"]
    return validate_payload(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    arguments = parser.parse_args()

    failed = False
    for path in arguments.files:
        errors = validate_file(path)
        if errors:
            failed = True
            print(f"{path}: invalid", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
        else:
            print(f"{path}: valid AstroPlan draft v1")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
