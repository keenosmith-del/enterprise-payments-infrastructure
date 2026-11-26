"""Wait for the identity endpoint without printing credentials."""
import os
import time
import urllib.error
import urllib.request

url = os.getenv("EPI_KEYCLOAK_ORIGIN", "http://127.0.0.1:8180") + "/realms/master/.well-known/openid-configuration"
for attempt in range(90):
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            if response.status == 200:
                break
    except (urllib.error.URLError, TimeoutError):
        time.sleep(2)
else:
    raise RuntimeError("Keycloak did not become available")
