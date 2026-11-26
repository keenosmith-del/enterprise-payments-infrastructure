# M01 implementation status

26 November 2026 | Status: in progress. M00 accepted for foundation implementation by the maintainer. This is an intermediate delivery, not M01 acceptance.

The starting baseline was `c51eca343fbbb0dbdee0833f230f41554a1b220d`. Four FastAPI entry points share technical health and application information code. Liveness does not contact a database; readiness fails closed without a reachable PostgreSQL database and the expected migration revision. Four separately built React shells show actual backend information and readiness when connected through their development proxy. There are no business operations or financial processing in these foundations.

The Python lock was generated under Python 3.14 with pip-tools 7.5.2 and pip 25.2. Node 24 is required for Vite 8. The lock files pin resolved dependencies and Python distributions include hashes. Local unit tests and frontend builds are preliminary checks only. The M01 foundation workflow checks these incremental artifacts and does not cover the full milestone.

Initial per-application migration files create tenant and legal entity foundation records. A hosted smoke test exercises each migration twice against disposable PostgreSQL. This does not establish database role isolation.

Outstanding: independent database bootstrap, identities and grants, fixtures, real PostgreSQL tests, Keycloak and OIDC, tenant authorization, RabbitMQ, development SFTP, Compose, container builds, browser tests, complete observability, data engineering, full verification and operating documentation. No readiness success or security isolation is claimed. The local Docker daemon was unavailable. M02 remains unauthorised.
