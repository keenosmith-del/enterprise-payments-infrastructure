#!/usr/bin/env bash
# Generate disposable local credentials once; never overwrite existing keys.
set -euo pipefail
umask 077
root="${EPI_SFTP_KEYS_DIR:-.local/sftp}"
mkdir -p "$root/input" "$root/clients"
for name in host partner_a partner_b; do
    case "$name" in host) destination="$root/input/host" ;; *) destination="$root/clients/$name" ;; esac
    if [[ ! -e "$destination" && ! -e "$destination.pub" ]]; then
        ssh-keygen -q -N '' -t ed25519 -f "$destination"
    elif [[ ! -f "$destination" || ! -f "$destination.pub" ]]; then
        echo "Incomplete key pair: $destination" >&2
        exit 1
    fi
done
for partner in partner_a partner_b; do
    install -m 0644 "$root/clients/$partner.pub" "$root/input/$partner.pub"
done
chmod 0600 "$root/input/host" "$root/clients/partner_a" "$root/clients/partner_b"
echo "Development keys ready in $root; verify input/host.pub before connecting."
