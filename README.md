# AstroPlan

AstroPlan is an open, portable JSON format for exchanging astronomy observing
plans between planning applications, smart-telescope apps, capture controllers,
and other astronomy tools.

The format is deliberately small:

- ordered observing targets
- J2000 equatorial coordinates
- optional schedule windows, start offsets, and durations
- forward-compatible extension fields

AstroPlan is currently a **draft standard**. Feedback and real-world
interoperability experiments are welcome before the version 1 specification is
declared stable.

## Start here

- [Draft version 1 specification](SPECIFICATION.md)
- [JSON Schema](schema/astroplan-v1.schema.json)
- [Example files](examples)
- [Registered extensions](extensions)
- [Implementation prompts](prompts)
- [AstroPlan Codex skill](skills/astroplan)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)

The public overview and developer introduction are also available at
[astroguide.space/standards/astroplan](https://astroguide.space/standards/astroplan/).

## Install the AstroPlan skill

The repository includes an actual OpenAI agent skill for creating, reading,
editing, validating, summarizing, and converting `.astroplan` files.

In Codex, ask the built-in installer:

```text
Use $skill-installer to install the skill from
https://github.com/tophrchris/AstroPlan/tree/main/skills/astroplan
```

For a manual user-level installation, place the `skills/astroplan` directory at:

```text
~/.agents/skills/astroplan
```

ChatGPT desktop can then select the skill with `@AstroPlan`. Codex can invoke it
with `$astroplan`. Start a new conversation after installation; if the skill
does not appear, restart the desktop application.

## Compatibility principles

AstroPlan readers should:

- preserve target order;
- treat every target-array occurrence as a distinct schedule entry, even when
  several entries refer to the same catalog subject;
- ignore unknown fields they do not understand;
- resolve targets by catalog identifier, then exact name, then coordinates;
- surface unresolved entries instead of silently dropping them.

AstroPlan writers should:

- emit UTF-8 JSON with a `.astroplan` extension;
- write `version: 1` while targeting this draft;
- use J2000 coordinates;
- use ISO 8601 timestamps with an offset or `Z`;
- use namespaced keys for experimental application-specific extensions.

## Contributing

Issues and pull requests are welcome from astronomy application developers,
equipment-controller authors, and observers testing interchange workflows.
Please include a small example file or fixture when proposing a behavioral
change.

## License

AstroPlan documentation, schemas, examples, prompts, and supporting code are
available under the [MIT License](LICENSE).
