"""Exercise actual broker permissions and technical transport."""
import os
import subprocess
import sys

import pika
import pytest


def connect(user: str):
    return pika.BlockingConnection(pika.ConnectionParameters(
        host="127.0.0.1", port=5672, virtual_host="epi-development",
        credentials=pika.PlainCredentials(user, os.environ[f"EPI_RABBIT_{user.upper()}_PASSWORD"])))


def test_authorised_transport_and_denied_access():
    with connect("payments_hub") as connection:
        channel = connection.channel()
        channel.confirm_delivery()
        channel.basic_publish("epi.technical", "probe", b"synthetic-technical-probe", mandatory=True)
    result = subprocess.run([sys.executable, "services/enterprise-integration/technical_probe.py"],
                            check=True, capture_output=True, text=True)
    assert result.stdout.strip() == "synthetic-technical-probe"
    with connect("policy_administration") as connection:
        with pytest.raises(pika.exceptions.ChannelClosedByBroker) as error:
            connection.channel().basic_publish("epi.technical", "probe", b"unauthorised", mandatory=True)
            connection.process_data_events(time_limit=2)
        assert error.value.reply_code == 403
    with connect("banking_simulator") as connection:
        with pytest.raises(pika.exceptions.ChannelClosedByBroker) as error:
            connection.channel().basic_get("epi.integration")
        assert error.value.reply_code == 403
