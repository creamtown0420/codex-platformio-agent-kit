# Security policy

## Supported versions

The current `main` branch is supported.

## Reporting a vulnerability

Open a private security advisory on GitHub if possible. If that is not available, open an issue with minimal public detail and mark it as security-related.

## Security principles

- Do not commit secrets, Wi-Fi passwords, tokens, or device credentials.
- Do not add telemetry.
- Do not upload firmware unless the user explicitly asks.
- Keep CI hardware-free by default.
- Treat serial logs as potentially sensitive if they include network names, device identifiers, or credentials.
