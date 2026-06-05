---
name: platformio-embedded
description: Use for ESP32, Raspberry Pi Pico, Arduino-compatible firmware, PlatformIO builds, hardware upload workflows, serial monitor debugging, embedded CI, and board-environment changes. Do not use for unrelated web/backend tasks.
---

# PlatformIO Embedded Skill

Use this skill when working on a PlatformIO-based embedded project, especially ESP32 or Raspberry Pi Pico firmware.

## Core workflow

1. Inspect the project structure.
   - Find `platformio.ini`.
   - Identify all `[env:*]` environments.
   - Identify whether there is a `native` or host-test environment.

2. Validate cheaply before hardware-specific work.
   - Prefer native build/test first when available.
   - Then build the specific embedded environment.

3. Use the repository helper when present.
   - Environment check: `python tools/pio_agent.py doctor`
   - List serial ports: `python tools/pio_agent.py ports`
   - Build: `python tools/pio_agent.py build --project <project-dir> --env <env>`
   - Test: `python tools/pio_agent.py test --project <project-dir> --env <env>`
   - Upload: `python tools/pio_agent.py upload --project <project-dir> --env <env> --port <port>`
   - Monitor: `python tools/pio_agent.py monitor --project <project-dir> --port <port> --baud 115200 --duration 15`

4. Upload safety.
   - Do not upload firmware unless the user explicitly asks.
   - Do not invent a serial port.
   - If the port is unknown, run `ports` or ask for it.

5. Serial-log debugging.
   - Ask for or capture logs.
   - State the exact observed symptom.
   - Make the smallest code/config change that addresses the symptom.
   - Rebuild after changes.

6. CI changes.
   - Keep default CI hardware-free.
   - Use `pio run` for normal PlatformIO projects.
   - Add embedded environment builds only when CI time remains reasonable.

## Common PlatformIO commands

```bash
pio run -d examples/blink-dual -e native
pio test -d examples/blink-dual -e native
pio run -d examples/blink-dual -e esp32dev
pio run -d examples/blink-dual -e pico
pio run -d examples/blink-dual -e esp32dev -t upload --upload-port COM3
pio device monitor --port COM3 --baud 115200
```

## Failure handling

When a command fails:

1. Quote the failing command.
2. Summarize the relevant error lines.
3. Do not hide missing-toolchain problems.
4. Make one focused fix.
5. Run the closest validation command again.

## Boundaries

Do not add cloud services, telemetry, OTA update infrastructure, Wi-Fi credentials, or hidden network calls unless the user explicitly requests them and the security implications are documented.
