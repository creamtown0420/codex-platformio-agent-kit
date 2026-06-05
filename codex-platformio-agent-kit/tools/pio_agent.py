#!/usr/bin/env python3
"""Small, explicit PlatformIO helper for coding agents and humans.

This script intentionally wraps only common, safe commands. It does not hide the
underlying PlatformIO command; every subprocess call is printed before execution.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable, Sequence


class CommandError(RuntimeError):
    """Raised when an external command fails."""


def _print_command(cmd: Sequence[str], cwd: Path | None = None) -> None:
    location = f" (cwd={cwd})" if cwd else ""
    print("$ " + " ".join(cmd) + location)


def run_command(
    cmd: Sequence[str],
    cwd: Path | None = None,
    check: bool = True,
    timeout: int | None = None,
) -> int:
    _print_command(cmd, cwd)
    try:
        completed = subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=False, timeout=timeout)
    except FileNotFoundError as exc:
        raise CommandError(f"Command not found: {cmd[0]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise CommandError(f"Command timed out after {timeout}s: {' '.join(cmd)}") from exc

    if check and completed.returncode != 0:
        raise CommandError(f"Command failed with exit code {completed.returncode}: {' '.join(cmd)}")
    return completed.returncode


def pio_executable() -> str | None:
    return shutil.which("pio") or shutil.which("platformio")


def require_pio() -> str:
    pio = pio_executable()
    if not pio:
        raise CommandError(
            "PlatformIO Core was not found. Install it with: python -m pip install --upgrade platformio"
        )
    return pio


def normalize_project(path: str) -> Path:
    project = Path(path).expanduser().resolve()
    if not project.exists():
        raise CommandError(f"Project directory does not exist: {project}")
    if not (project / "platformio.ini").exists():
        raise CommandError(f"platformio.ini was not found in: {project}")
    return project


def command_doctor(_: argparse.Namespace) -> None:
    print(f"Python: {sys.version.split()[0]}")
    pio = pio_executable()
    if not pio:
        print("PlatformIO: NOT FOUND")
        print("Install: python -m pip install --upgrade platformio")
        raise SystemExit(1)
    print(f"PlatformIO executable: {pio}")
    run_command([pio, "--version"], check=False)


def command_ports(_: argparse.Namespace) -> None:
    pio = require_pio()
    rc = run_command([pio, "device", "list", "--json-output"], check=False)
    if rc != 0:
        print("Falling back to plain port listing.")
        run_command([pio, "device", "list"], check=False)


def pio_project_cmd(args: argparse.Namespace, base: Iterable[str]) -> list[str]:
    pio = require_pio()
    cmd = [pio, *base, "-d", str(normalize_project(args.project))]
    if getattr(args, "env", None):
        cmd.extend(["-e", args.env])
    return cmd


def command_build(args: argparse.Namespace) -> None:
    cmd = pio_project_cmd(args, ["run"])
    run_command(cmd)


def command_test(args: argparse.Namespace) -> None:
    cmd = pio_project_cmd(args, ["test"])
    run_command(cmd)


def command_upload(args: argparse.Namespace) -> None:
    cmd = pio_project_cmd(args, ["run"])
    cmd.extend(["-t", "upload"])
    if args.port:
        cmd.extend(["--upload-port", args.port])
    else:
        print("No --port was provided. PlatformIO will try auto-detection.")
    run_command(cmd)


def command_monitor(args: argparse.Namespace) -> None:
    require_pio()
    pio = require_pio()
    normalize_project(args.project)
    cmd = [pio, "device", "monitor", "--baud", str(args.baud)]
    if args.port:
        cmd.extend(["--port", args.port])
    if args.project:
        cmd.extend(["-d", str(normalize_project(args.project))])

    _print_command(cmd)
    if args.duration <= 0:
        run_command(cmd)
        return

    started = time.time()
    process = subprocess.Popen(cmd)
    try:
        while process.poll() is None:
            if time.time() - started >= args.duration:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                break
            time.sleep(0.2)
    except KeyboardInterrupt:
        process.terminate()
        process.wait(timeout=5)


def command_envs(args: argparse.Namespace) -> None:
    project = normalize_project(args.project)
    envs: list[str] = []
    for line in (project / "platformio.ini").read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("[env:") and stripped.endswith("]"):
            envs.append(stripped.removeprefix("[env:").removesuffix("]"))
    print(json.dumps({"project": str(project), "environments": envs}, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safe PlatformIO helper for agent workflows")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Check Python and PlatformIO availability")
    doctor.set_defaults(func=command_doctor)

    ports = sub.add_parser("ports", help="List connected serial devices")
    ports.set_defaults(func=command_ports)

    envs = sub.add_parser("envs", help="List PlatformIO environments from platformio.ini")
    envs.add_argument("--project", default=".", help="PlatformIO project directory")
    envs.set_defaults(func=command_envs)

    build = sub.add_parser("build", help="Run pio run")
    build.add_argument("--project", default=".", help="PlatformIO project directory")
    build.add_argument("--env", required=True, help="PlatformIO environment name")
    build.set_defaults(func=command_build)

    test = sub.add_parser("test", help="Run pio test")
    test.add_argument("--project", default=".", help="PlatformIO project directory")
    test.add_argument("--env", required=True, help="PlatformIO environment name")
    test.set_defaults(func=command_test)

    upload = sub.add_parser("upload", help="Upload firmware with pio run -t upload")
    upload.add_argument("--project", default=".", help="PlatformIO project directory")
    upload.add_argument("--env", required=True, help="PlatformIO environment name")
    upload.add_argument("--port", help="Serial/upload port, e.g. COM3 or /dev/ttyUSB0")
    upload.set_defaults(func=command_upload)

    monitor = sub.add_parser("monitor", help="Run PlatformIO serial monitor")
    monitor.add_argument("--project", default=".", help="PlatformIO project directory")
    monitor.add_argument("--port", help="Serial port, e.g. COM3 or /dev/ttyUSB0")
    monitor.add_argument("--baud", type=int, default=115200, help="Serial baud rate")
    monitor.add_argument("--duration", type=int, default=0, help="Stop after N seconds; 0 means run until interrupted")
    monitor.set_defaults(func=command_monitor)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except CommandError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
