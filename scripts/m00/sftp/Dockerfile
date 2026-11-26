FROM debian:13-slim@sha256:8aa5a7bf5a1955bddbe7d74fcdd0b91ab30e74362a8b73af672b0481b35b44a0
RUN apt-get update && apt-get install -y --no-install-recommends openssh-server \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -M -d /inbox -s /usr/sbin/nologin -p '*' partner_a \
    && useradd -M -d /inbox -s /usr/sbin/nologin -p '*' partner_b \
    && install -d -m 0755 /run/sshd /srv/sftp/partner_a /srv/sftp/partner_b \
    && install -d -m 0700 -o partner_a -g partner_a /srv/sftp/partner_a/inbox \
    && install -d -m 0700 -o partner_b -g partner_b /srv/sftp/partner_b/inbox
COPY sshd_config /etc/ssh/epi_probe_config
COPY entrypoint.sh /usr/local/bin/epi-probe-entrypoint
RUN chmod 0755 /usr/local/bin/epi-probe-entrypoint
CMD ["/usr/local/bin/epi-probe-entrypoint"]
