#!/usr/bin/env bash
set -euo pipefail
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
printf '[127.0.0.1]:2222 %s\n' "$(cut -d ' ' -f 1,2 .local/sftp/input/host.pub)" > "$scratch/known_hosts"
printf 'synthetic technical payload\n' > "$scratch/source"
sftp -q -F /dev/null -o BatchMode=yes -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes \
  -o UserKnownHostsFile="$scratch/known_hosts" -i .local/sftp/clients/partner_a -P 2222 -b - partner_a@127.0.0.1 <<END
put $scratch/source /inbox/probe
get /inbox/probe $scratch/result
rm /inbox/probe
END
cmp "$scratch/source" "$scratch/result"
