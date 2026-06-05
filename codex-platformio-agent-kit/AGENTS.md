# AGENTS.md

## Project purpose

This repository helps Codex and other coding agents work safely on PlatformIO-based embedded projects for ESP32 and Raspberry Pi Pico.

The main deliverables are:

- reusable agent instructions in `.agents/skills/platformio-embedded/SKILL.md`
- a cross-platform helper script in `tools/pio_agent.py`
- a minimal PlatformIO sample in `examples/blink-dual`
- CI that proves the sample builds and tests without hardware

## Working rules for agents

1. Do not guess board identifiers. Inspect `platformio.ini` first.
2. Prefer the cheapest check first: `native` build/test before embedded builds.
3. Run validation after changing code:
   - `python tools/pio_agent.py build --project examples/blink-dual --env native`
   - `python tools/pio_agent.py test --project examples/blink-dual --env native`
4. Do not run upload/flash commands unless the user explicitly asks for hardware upload.
5. Do not assume a serial port. Use `python tools/pio_agent.py ports` or ask the user for the port if uploading is requested.
6. When debugging hardware behavior, treat serial logs as evidence. Avoid speculative fixes without a build or a log-based reason.
7. Keep examples small and copyable. Avoid adding large frameworks or unnecessary dependencies.
8. Do not store secrets, Wi-Fi passwords, API keys, or device credentials in this repository.
9. If changing CI, keep the default CI hardware-free.
10. If a command fails because PlatformIO or a toolchain is unavailable, report the exact command and the failure. Do not claim the project passed.

## Code style

- Python: standard library first, typed functions where practical, clear subprocess error handling.
- C++: keep sample firmware compatible with Arduino-style PlatformIO environments and native host builds.
- Documentation: write direct, operational instructions. Prefer copy/paste commands.

## Important paths

- `tools/pio_agent.py`: command wrapper for doctor/build/test/upload/monitor/ports
- `examples/blink-dual/platformio.ini`: sample environments
- `.agents/skills/platformio-embedded/SKILL.md`: Codex skill instructions
- `.github/workflows/platformio-ci.yml`: GitHub Actions workflow
