# Contributing

Contributions should keep the repository small, practical, and safe for embedded developers.

## Before opening a PR

Run:

```bash
python tools/pio_agent.py build --project examples/blink-dual --env native
python tools/pio_agent.py test --project examples/blink-dual --env native
```

If you add or modify a board environment, also run the relevant build:

```bash
python tools/pio_agent.py build --project examples/blink-dual --env <env>
```

Do not run upload commands in CI.

## Good contributions

- safer Codex/agent instructions
- additional PlatformIO board examples
- clearer debugging workflows
- native tests
- documentation that removes ambiguity

## Avoid

- hidden network calls
- telemetry
- hard-coded Wi-Fi credentials
- large dependencies without clear need
- workflows that require physical hardware by default
