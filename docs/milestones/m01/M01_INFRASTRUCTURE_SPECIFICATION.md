# M01 infrastructure specification

26 November 2026 | Development foundation | Synthetic data only.

The root Compose configuration starts PostgreSQL, RabbitMQ, Keycloak, four independently built FastAPI backends and four independently built React frontends. One PostgreSQL cluster contains four separately owned application databases. RabbitMQ uses the `epi-development` virtual host and a technical exchange and queue. The Keycloak realm is provisioned from generated local credentials. Supporting SFTP, integration, analytics and observability services use explicit profiles. The SFTP profile requires `scripts/m01/create_sftp_keys.sh` before startup. No service connects to a real payment provider.

PostgreSQL and identity state use named volumes. Normal `make down` retains volumes. Application containers and frontend web servers use non-root users. Host ports are bound to loopback. Runtime credentials are generated locally in `.local/epi.env`; its permissions are restricted and the file is ignored by Git. The container build excludes local credentials from the build context. SFTP keys are generated separately under ignored `.local/sftp`.

The M01 Compose services and application build images use pinned multi-platform manifest digests alongside version tags. Registry manifest inspection on 26 November 2026 showed Linux amd64 and arm64 entries for Python, Node, PostgreSQL, RabbitMQ, Debian, nginx-unprivileged, Prometheus, Grafana and Keycloak. Docker selects the platform-specific image from each pinned index. The original M00 PostgreSQL and RabbitMQ feasibility Compose references retain their original tags. Registry index availability is not an ARM64 execution result; the hosted runtime evidence is Linux x86-64. Review image licences before distribution. The local stack requires sufficient memory and storage for PostgreSQL, Keycloak, RabbitMQ and eight application containers. Optional monitoring and analytical services add resource requirements.

## Licensing considerations

The stack includes open-source components with different terms. Keycloak is distributed under Apache 2.0; PostgreSQL uses the PostgreSQL licence; RabbitMQ uses MPL 2.0; and Grafana OSS uses AGPLv3. See the respective component notices, including [Grafana licensing](https://grafana.com/licensing/), when distributing images or modifications. Python and JavaScript locks include transitive components with their own notices. This inventory is not a legal clearance or a substitute for a distribution-specific licence review.
