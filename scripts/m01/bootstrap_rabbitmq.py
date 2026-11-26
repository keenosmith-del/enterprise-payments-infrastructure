"""Provision synthetic development topology via the local management API."""
import base64
import json
import os
import urllib.parse
import urllib.request

BASE = os.environ.get("EPI_RABBIT_MANAGEMENT_URL", "http://127.0.0.1:15672/api")
VHOST = "epi-development"
USERS = ("policy_administration", "payments_hub", "banking_simulator", "payroll_simulator", "integration")


def request_api(path: str, payload: dict, method: str = "PUT") -> None:
    credentials = f'{os.environ["EPI_RABBIT_ADMIN"]}:{os.environ["EPI_RABBIT_ADMIN_PASSWORD"]}'.encode()
    request = urllib.request.Request(BASE + path, data=json.dumps(payload).encode(), method=method, headers={
        "Authorization": "Basic " + base64.b64encode(credentials).decode(), "Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=10) as response:
        if response.status not in (201, 204):
            raise RuntimeError("RabbitMQ provisioning failed")


def bootstrap() -> None:
    encoded_vhost = urllib.parse.quote(VHOST, safe="")
    passwords = [os.environ[f"EPI_RABBIT_{user.upper()}_PASSWORD"] for user in USERS]
    if any(not value for value in passwords) or len(set(passwords)) != len(passwords):
        raise RuntimeError("Distinct non-empty RabbitMQ passwords required")
    request_api(f"/vhosts/{encoded_vhost}", {})
    admin = urllib.parse.quote(os.environ["EPI_RABBIT_ADMIN"], safe="")
    request_api(f"/permissions/{encoded_vhost}/{admin}", {"configure": ".*", "write": ".*", "read": ".*"})
    for user, password in zip(USERS, passwords, strict=True):
        request_api(f"/users/{user}", {"password": password, "tags": ""})
        permission = {"configure": "^$", "write": "^$", "read": "^$"}
        if user == "payments_hub":
            permission["write"] = "^epi\\.technical$"
        if user == "integration":
            permission["read"] = "^epi\\.integration$"
        request_api(f"/permissions/{encoded_vhost}/{user}", permission)
    request_api(f"/exchanges/{encoded_vhost}/epi.technical", {"type": "direct", "durable": True, "auto_delete": False})
    request_api(f"/queues/{encoded_vhost}/epi.integration", {"durable": True, "auto_delete": False})
    request_api(f"/bindings/{encoded_vhost}/e/epi.technical/q/epi.integration", {"routing_key": "probe"}, method="POST")


if __name__ == "__main__":
    bootstrap()
