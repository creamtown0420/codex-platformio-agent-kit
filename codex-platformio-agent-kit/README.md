# Codex PlatformIO Agent Kit

A small, practical open-source starter kit for using Codex with ESP32, Raspberry Pi Pico, and PlatformIO projects.

The goal is not to replace PlatformIO. The goal is to give AI coding agents a safe, repeatable embedded-development workflow:

- understand the repository rules from `AGENTS.md`
- use a repository skill from `.agents/skills/platformio-embedded/SKILL.md`
- build with PlatformIO before changing more code
- prefer host/native validation before flashing hardware
- upload to a board only when the user explicitly asks for it
- capture serial logs in a structured way when debugging firmware
- keep CI green with a minimal native PlatformIO example

## Why this exists

Embedded projects are harder for coding agents than normal web projects because the agent often cannot see the device. A useful agent workflow needs clear rules:

1. inspect `platformio.ini`
2. identify the board environment
3. run the cheapest local check first
4. build before upload
5. ask before flashing hardware
6. use serial logs as evidence instead of guessing

This repository packages those rules into files that can be copied into real ESP32/Pico repositories.

## Repository layout

```text
.
├── AGENTS.md                                  # Codex repository instructions
├── .agents/skills/platformio-embedded/        # Reusable Codex skill
├── tools/pio_agent.py                         # Cross-platform PlatformIO helper
├── examples/blink-dual/                       # Native + ESP32 + Pico sample project
├── .github/workflows/platformio-ci.yml        # CI for the sample project
└── docs/                                      # Prompts, roadmap, OSS application draft
```

## Quick start

### 1. Install PlatformIO Core

```bash
python -m pip install --upgrade platformio
```

### 2. Check the local environment

```bash
python tools/pio_agent.py doctor
```

### 3. Build the sample without hardware

```bash
python tools/pio_agent.py build --project examples/blink-dual --env native
```

### 4. Run the native test

```bash
python tools/pio_agent.py test --project examples/blink-dual --env native
```

### 5. Build for ESP32 or Pico

```bash
python tools/pio_agent.py build --project examples/blink-dual --env esp32dev
python tools/pio_agent.py build --project examples/blink-dual --env pico
```

### 6. Upload only when you have a board connected

```bash
python tools/pio_agent.py upload --project examples/blink-dual --env esp32dev --port COM3
# or macOS/Linux example:
python tools/pio_agent.py upload --project examples/blink-dual --env esp32dev --port /dev/ttyUSB0
```

## Using with Codex

Ask Codex something like:

```text
Use the platformio-embedded skill. Add support for an ESP32-S3 board to the sample project.
Run the native build first, then build the new board environment. Do not upload firmware.
```

or:

```text
Use the platformio-embedded skill. I pasted a serial log from my ESP32 below.
Identify the likely firmware issue, propose the smallest fix, and update the code.
Run the PlatformIO build after changes.
```

More prompt templates are in [`docs/CODEX_PROMPTS.md`](docs/CODEX_PROMPTS.md).

## What this project is not

- It is not a cloud flashing service.
- It does not bypass USB permissions or OS security prompts.
- It does not upload firmware unless the user explicitly runs an upload command.
- It does not collect telemetry.

## Roadmap

See [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Contributing

See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).

## Security

See [`docs/SECURITY.md`](docs/SECURITY.md).

## License

MIT.
