# M00 development environment

Revision 0.1 | 26 November 2026 | EPI 0.1.0 | Observed on the canonical development Mac.

## Host and installed tooling

- macOS 27.0.1, build 26A434, Darwin arm64. Apple M5 with 10 CPU cores and 16 GB RAM, inspected through `system_profiler SPHardwareDataType`. `df -h .` reported 282 GiB available at inspection. This is a host observation.
- Homebrew Python 3.12.15 and default Python 3.15.1; Node 24.21.0 with npm 11.19.0; Git 2.56.0; GitHub CLI 2.102.0; OpenSSH 10.3p1.
- Docker CLI 29.8.2, Darwin arm64, Compose v5.5.1. Docker Desktop context was present, but the daemon socket was unavailable. Opening the application failed and the CLI startup retry hit protected logs and timed out. No PostgreSQL or RabbitMQ host installation was found.
- Native OpenSSH client and SFTP subsystem are available. A transient TCP bind to 127.0.0.1 was denied. A subprocess-driven SFTP transfer worked without a listener.
- GitHub CLI could not reach the API. The GitHub integration returned 404 for the exact target. This can mean absence or insufficient access. The browser route reached GitHub sign-in. The canonical path disallowed creating `.git`. Git identity settings were inspected without recording their values.
- Power BI Desktop is a supported Windows workflow. No Windows runtime or Power BI account was verified in this execution. The browser reporting path remains part of the proposal.

## Reproduction approach

Use Python 3.12 in a temporary virtual environment for M00 probes and keep test dependencies out of global site packages. Use nonce credentials, disposable service containers and loopback-only ports. Resolve package hashes and image manifest digests on a network-enabled runner before adopting M01 pins. Inspect `linux/arm64` and `linux/amd64` manifests and run a cold Compose start. Measure each profile with container stats and capture startup time, disk and memory. Record identity, observability and analytics profiles independently. A working ARM64 Docker CLI does not establish Linux/ARM64 image compatibility.

For a 16 GB host, start with a core-only profile, then add identity and optional tools selectively. Track container limits separately from host resource use, plus memory pressure when running Playwright or BI. Treat profiles and resource limits as measurement inputs. No capacity or throughput result was derived.

The local command, initial failures and runner recipe appear in [M00 architecture verification](M00_ARCHITECTURE_VERIFICATION.md).
