"""Publish one disposable technical integration probe with the restricted producer."""
import os
import pika

with pika.BlockingConnection(pika.ConnectionParameters(
    host=os.getenv("EPI_RABBIT_HOST", "127.0.0.1"), port=int(os.getenv("EPI_RABBIT_PORT", "5672")),
    virtual_host="epi-development", credentials=pika.PlainCredentials(
        "payments_hub", os.environ["EPI_RABBIT_PAYMENTS_HUB_PASSWORD"]))) as connection:
    channel = connection.channel()
    channel.confirm_delivery()
    channel.basic_publish("epi.technical", "probe", b"synthetic-technical-probe", mandatory=True)
