# Codex prompt templates

## Add a new board environment

```text
Use the platformio-embedded skill.
Add support for <BOARD NAME> to examples/blink-dual/platformio.ini.
Do not remove the native environment.
Run the native build/test first, then build the new environment.
Do not upload firmware.
```

## Debug a serial log

```text
Use the platformio-embedded skill.
Here is a serial log from my <BOARD>.
Identify the most likely cause, make the smallest code or config change, and run the relevant PlatformIO build.
Do not upload firmware.

<PASTE LOG HERE>
```

## Improve CI

```text
Use the platformio-embedded skill.
Improve the GitHub Actions workflow so it keeps hardware-free checks reliable and fast.
Keep native build/test as required.
Embedded matrix builds may be continue-on-error if toolchain downloads are unstable.
```

## Prepare a pull request

```text
Use the platformio-embedded skill.
Review this branch as if you were maintaining an OSS embedded repository.
Check docs, CI, PlatformIO environments, and upload safety.
Return a concise PR summary and testing notes.
```

## Release checklist

```text
Use the platformio-embedded skill.
Prepare a release checklist for this repository.
Confirm the CI commands, README quick start, and examples are consistent.
Do not change version numbers unless necessary.
```
