"""Consume one synthetic technical probe and acknowledge it, without financial authority."""
import os

import pika


def receive_one() -> bytes:
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv("EPI_RABBIT_HOST", "127.0.0.1"), port=int(os.getenv("EPI_RABBIT_PORT", "5672")),
        virtual_host="epi-development", credentials=pika.PlainCredentials(
            "integration", os.environ["EPI_RABBIT_INTEGRATION_PASSWORD"])))
    try:
        channel = connection.channel()
        method, _, body = channel.basic_get("epi.integration", auto_ack=False)
        if method is None:
            raise RuntimeError("No technical message available")
        channel.basic_ack(method.delivery_tag)
        return body
    finally:
        connection.close()


if __name__ == "__main__":
    print(receive_one().decode("utf-8"))
