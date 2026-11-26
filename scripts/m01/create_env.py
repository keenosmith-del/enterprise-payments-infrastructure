"""Create local, disposable development credentials without replacing existing state."""
import os
import secrets
from pathlib import Path

APPS = ("POLICY_ADMINISTRATION", "PAYMENTS_HUB", "BANKING_SIMULATOR", "PAYROLL_SIMULATOR")
path = Path(".local/epi.env")
path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
values = {"EPI_POSTGRES_ADMIN_PASSWORD": secrets.token_hex(24),
          "EPI_KEYCLOAK_ADMIN": "epi_admin", "EPI_KEYCLOAK_ADMIN_PASSWORD": secrets.token_hex(24),
          "EPI_KEYCLOAK_USER_PASSWORD": secrets.token_hex(24), "EPI_RABBIT_ADMIN": "epi_admin",
          "EPI_RABBIT_ADMIN_PASSWORD": secrets.token_hex(24), "EPI_GRAFANA_PASSWORD": secrets.token_hex(24)}
for app in APPS:
    for role in ("MIGRATION", "RUNTIME"):
        values[f"EPI_{app}_{role}_PASSWORD"] = secrets.token_hex(24)
    values[f"EPI_RABBIT_{app}_PASSWORD"] = secrets.token_hex(24)
values["EPI_RABBIT_INTEGRATION_PASSWORD"] = secrets.token_hex(24)
try:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
except FileExistsError:
    print(f"Keeping existing {path}; remove it explicitly to regenerate credentials.")
else:
    with os.fdopen(fd, "w") as output:
        output.writelines(f"{key}={value}\n" for key, value in values.items())
    print(f"Created {path} with synthetic development credentials.")
