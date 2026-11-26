#!/bin/sh
set -eu

# Bind-mounted files retain host ownership; StrictModes requires trusted owners.
install -d -o root -g root -m 0755 /probe-keys
install -o root -g root -m 0600 /probe-keys-input/host /probe-keys/host
for partner in partner_a partner_b; do
    install -o root -g root -m 0644 "/probe-keys-input/$partner.pub" "/probe-keys/$partner.pub"
done
exec /usr/sbin/sshd -D -e -f /etc/ssh/epi_probe_config
