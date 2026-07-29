# Contributing to AstroPlan

AstroPlan is a draft interoperability standard. Contributions are welcome,
especially from astronomy application developers, equipment integrations, and
observers testing real schedule exchanges.

## Before proposing a change

- Open an issue for new core fields, changed semantics, or registered
  extensions.
- Keep version 1 changes backward compatible whenever possible.
- Preserve unknown fields during round trips.
- Treat each target-array occurrence as a distinct schedule entry, even when
  multiple entries reference the same catalog subject.
- Keep J2000 coordinates and schedule timing at the highest available
  precision.

## Pull requests

Pull requests should explain the interoperability problem being solved and
identify which applications or workflows would use the change. Include or
update examples and schemas when the payload shape changes.

Before opening a pull request, run:

```bash
python3 skills/astroplan/scripts/validate_astroplan.py \
  examples/*.astroplan \
  conformance/valid/*.astroplan
```

Also verify that deliberately invalid conformance fixtures are rejected:

```bash
python3 skills/astroplan/scripts/validate_astroplan.py \
  conformance/invalid/*.astroplan
```

The second command should exit unsuccessfully and describe why each fixture is
invalid.

## Example data

Examples should be realistic enough to exercise interoperability without
containing private information, precise private-site coordinates, account
identifiers, access tokens, or other secrets. State whether an example is an
unmodified application export or a constructed conformance fixture.

## Licensing

By contributing, you agree that your contribution is licensed under this
repository's MIT License.
