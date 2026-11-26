#!/usr/bin/env bash
# Real SSH/SFTP probe in a disposable loopback-only container.
set -euo pipefail

scratch="$(mktemp -d)"
scratch="$(cd "$scratch" && pwd -P)"
image=epi-m00-sftp
container=
cleanup() {
    if [[ -n "$container" ]]; then
        docker rm -f "$container" >/dev/null
    fi
    rm -rf "$scratch"
}
trap cleanup EXIT

mkdir "$scratch/server"
chmod 0755 "$scratch/server"
ssh-keygen -q -N '' -t ed25519 -f "$scratch/server/host"
for partner in partner_a partner_b; do
    ssh-keygen -q -N '' -t ed25519 -f "$scratch/$partner"
    cp "$scratch/$partner.pub" "$scratch/server/$partner.pub"
done
chmod 0644 "$scratch/server/"*.pub

docker build -t "$image" scripts/m00/sftp
container="$(docker run -d -p 127.0.0.1::22 \
    --mount "type=bind,source=$scratch/server,target=/probe-keys-input,readonly" "$image")"
port_mapping="$(docker port "$container" 22/tcp)"
port="${port_mapping##*:}"
printf '[127.0.0.1]:%s %s\n' "$port" "$(cut -d ' ' -f 1,2 "$scratch/server/host.pub")" \
    > "$scratch/known_hosts"

transfer() {
    local key="$1"
    local account="$2"
    sftp -q -F /dev/null -o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=5 \
        -o StrictHostKeyChecking=yes -o UserKnownHostsFile="$scratch/known_hosts" \
        -i "$scratch/$key" -P "$port" -b - "$account@127.0.0.1"
}

printf '%s\n' 'id,minor_units' 'SYN-1,75000' > "$scratch/source.csv"
for attempt in 1 2 3 4 5; do
    if printf 'pwd\n' | transfer partner_a partner_a; then
        break
    fi
    if [[ "$attempt" == 5 ]]; then
        docker logs "$container" >&2
        exit 1
    fi
    sleep 1
done
printf 'put %s/source.csv /inbox/source.part\nrename /inbox/source.part /inbox/source.ready\nget /inbox/source.ready %s/result.csv\n' \
    "$scratch" "$scratch" | transfer partner_a partner_a
cmp "$scratch/source.csv" "$scratch/result.csv"

# A wrong pinned host key must be rejected even with a valid partner key.
ssh-keygen -q -N '' -t ed25519 -f "$scratch/untrusted_host"
printf '[127.0.0.1]:%s %s\n' "$port" "$(cut -d ' ' -f 1,2 "$scratch/untrusted_host.pub")" > "$scratch/untrusted_hosts"
if printf 'pwd\n' | sftp -q -F /dev/null -o BatchMode=yes -o IdentitiesOnly=yes \
    -o ConnectTimeout=5 -o StrictHostKeyChecking=yes -o UserKnownHostsFile="$scratch/untrusted_hosts" \
    -i "$scratch/partner_a" -P "$port" -b - "partner_a@127.0.0.1"; then
    echo "Untrusted host key was accepted" >&2
    exit 1
fi

printf 'pwd\n' | transfer partner_b partner_b
if ssh -F /dev/null -o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=5 \
    -o StrictHostKeyChecking=yes -o UserKnownHostsFile="$scratch/known_hosts" \
    -i "$scratch/partner_a" -p "$port" partner_a@127.0.0.1 'id' >/dev/null 2>&1; then
    echo "Interactive shell command was accepted" >&2
    exit 1
fi
if printf 'pwd\n' | transfer partner_a partner_b; then
    echo "Invalid partner key was accepted" >&2
    exit 1
fi
if printf 'get /inbox/source.ready %s/cross.csv\n' "$scratch" | transfer partner_b partner_b; then
    echo "Partner B could read partner A's transfer" >&2
    exit 1
fi
if printf 'get /probe-keys/host.pub %s/outside.pub\n' "$scratch" | transfer partner_a partner_a; then
    echo "Partner A could read the host path outside its chroot" >&2
    exit 1
fi
echo "SSH public-key authentication, verified host key, SFTP transfer and directory separation passed"
