"""Run against dedicated, disposable M00 services only."""
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from hashlib import sha256
import io
import os
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Barrier
from time import monotonic
import unittest
from uuid import uuid4

import duckdb
import pika
import psycopg
from psycopg import errors, sql
import pyarrow as pa
import pyarrow.parquet as pq


class ServiceProbes(unittest.TestCase):
    def test_postgres_atomicity_constraints_isolation_and_retry(self):
        dsn = os.environ["EPI_M00_POSTGRES_DSN"]
        scope = uuid4().hex[:12]
        hub, other, writer = (f"epi_probe_{suffix}_{scope}" for suffix in ("hub", "pas", "writer"))
        password = uuid4().hex
        with psycopg.connect(dsn, autocommit=True) as admin:
            admin.execute(sql.SQL("CREATE ROLE {} LOGIN PASSWORD {}").format(
                sql.Identifier(writer), sql.Literal(password)
            ))
            try:
                for database in (hub, other):
                    admin.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))
                    admin.execute(sql.SQL("REVOKE CONNECT ON DATABASE {} FROM PUBLIC").format(
                        sql.Identifier(database)
                    ))
                admin.execute(sql.SQL("GRANT CONNECT ON DATABASE {} TO {}").format(
                    sql.Identifier(hub), sql.Identifier(writer)
                ))
                with self.assertRaisesRegex(psycopg.OperationalError, "permission denied for database"):
                    with psycopg.connect(dsn, dbname=other, user=writer, password=password):
                        self.fail("The application role unexpectedly connected to a foreign database")
                with psycopg.connect(dsn, dbname=hub, autocommit=True) as owner:
                    owner.execute(
                        "CREATE TABLE posting (id text PRIMARY KEY, debit bigint NOT NULL CHECK (debit > 0), "
                        "credit bigint NOT NULL, CHECK (debit = credit))"
                    )
                    owner.execute(
                        "CREATE TABLE outbox (id text PRIMARY KEY REFERENCES posting, "
                        "payload text NOT NULL)"
                    )
                    owner.execute("CREATE TABLE capacity (id int PRIMARY KEY, available bigint NOT NULL)")
                    owner.execute("INSERT INTO capacity VALUES (1, 100)")
                    owner.execute(sql.SQL("GRANT SELECT, INSERT ON posting, outbox TO {}").format(
                        sql.Identifier(writer)
                    ))
                    owner.execute(sql.SQL("GRANT SELECT, UPDATE ON capacity TO {}").format(
                        sql.Identifier(writer)
                    ))

                def connect():
                    return psycopg.connect(
                        dsn, dbname=hub, user=writer, password=password, autocommit=True
                    )

                with connect() as connection:
                    self.assertEqual((75031,), connection.execute(
                        "SELECT (sum(amount) * 100)::bigint "
                        "FROM (VALUES (0.10::numeric), (0.20::numeric), (750.01::numeric)) AS n(amount)"
                    ).fetchone())
                    with self.assertRaises(errors.CheckViolation):
                        connection.execute("INSERT INTO posting VALUES ('unbalanced', 1, 2)")
                    with self.assertRaises(errors.ForeignKeyViolation):
                        connection.execute("INSERT INTO outbox VALUES ('missing', 'event')")
                    with self.assertRaises(errors.NotNullViolation):
                        with connection.transaction():
                            connection.execute("INSERT INTO posting VALUES ('p1', 75000, 75000)")
                            connection.execute("INSERT INTO outbox VALUES ('p1', NULL)")
                    self.assertEqual((0,), connection.execute("SELECT count(*) FROM posting").fetchone())
                    self.assertEqual((0,), connection.execute("SELECT count(*) FROM outbox").fetchone())
                    with connection.transaction():
                        connection.execute("INSERT INTO posting VALUES ('p1', 75000, 75000)")
                        connection.execute("INSERT INTO outbox VALUES ('p1', 'posted')")
                    with self.assertRaises(errors.UniqueViolation):
                        connection.execute("INSERT INTO posting VALUES ('p1', 75000, 75000)")
                    with self.assertRaises(errors.InsufficientPrivilege):
                        connection.execute("UPDATE posting SET debit = 1 WHERE id = 'p1'")
                    self.assertEqual(("p1", 75000, 75000, "posted"), connection.execute(
                        "SELECT id, debit, credit, payload FROM posting JOIN outbox USING (id)"
                    ).fetchone())

                ready = Barrier(2, timeout=10)

                def reserve():
                    with connect() as connection:
                        connection.execute("SET statement_timeout = '15s'")
                        for attempt in (1, 2):
                            try:
                                with connection.transaction():
                                    connection.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
                                    available, = connection.execute(
                                        "SELECT available FROM capacity WHERE id = 1"
                                    ).fetchone()
                                    if attempt == 1:
                                        ready.wait()
                                    if available < 80:
                                        return ("rejected", attempt)
                                    connection.execute("UPDATE capacity SET available = %s WHERE id = 1",
                                                       (available - 80,))
                                return ("reserved", attempt)
                            except errors.SerializationFailure:
                                if attempt == 2:
                                    raise

                with ThreadPoolExecutor(max_workers=2) as pool:
                    results = list(pool.map(lambda _: reserve(), range(2)))
                self.assertCountEqual([("reserved", 1), ("rejected", 2)], results)
                with connect() as connection:
                    self.assertEqual((20,), connection.execute("SELECT available FROM capacity").fetchone())
            finally:
                for database in (hub, other):
                    admin.execute(sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(
                        sql.Identifier(database)
                    ))
                admin.execute(sql.SQL("DROP ROLE {}").format(sql.Identifier(writer)))

    def test_rabbitmq_confirmation_redelivery_duplicate_and_dead_letter(self):
        params = pika.URLParameters(os.environ["EPI_M00_AMQP_URL"])
        params.socket_timeout = 5
        params.blocked_connection_timeout = 10
        name = f"epi.probe.{uuid4().hex}"
        dead = f"{name}.dead"
        holder = pika.BlockingConnection(params)
        with TemporaryDirectory(prefix="epi-inbox-") as scratch, holder:
            management = holder.channel()
            management.queue_declare(dead, durable=True)
            management.queue_declare(name, durable=True, arguments={
                "x-dead-letter-exchange": "", "x-dead-letter-routing-key": dead,
            })
            try:
                management.confirm_delivery()
                for _ in range(2):
                    management.basic_publish(
                        "", name, b"op-42", mandatory=True,
                        properties=pika.BasicProperties(delivery_mode=2, message_id="op-42"),
                    )

                ledger = Path(scratch) / "inbox.db"
                with sqlite3.connect(ledger) as connection:
                    connection.execute("CREATE TABLE inbox (id TEXT PRIMARY KEY)")
                    worker = pika.BlockingConnection(params)
                    try:
                        channel = worker.channel()
                        delivery, props, body = channel.basic_get(name, auto_ack=False)
                        self.assertIsNotNone(delivery)
                        self.assertFalse(delivery.redelivered)
                        self.assertEqual(b"op-42", body)
                        connection.execute("INSERT INTO inbox VALUES (?)", (props.message_id,))
                        connection.commit()
                        # Close with delivery outstanding after the durable effect.
                    finally:
                        worker.close()
                    channel = holder.channel()
                    for redelivered in (True, False):
                        delivery, props, body = self.get_delivery(holder, channel, name)
                        self.assertIsNotNone(delivery)
                        self.assertEqual(redelivered, delivery.redelivered)
                        self.assertEqual(b"op-42", body)
                        with connection:
                            connection.execute("INSERT OR IGNORE INTO inbox VALUES (?)", (props.message_id,))
                        channel.basic_ack(delivery.delivery_tag)
                    self.assertEqual((1,), connection.execute("SELECT count(*) FROM inbox").fetchone())

                management.basic_publish("", name, b"poison", mandatory=True)
                channel = holder.channel()
                for retry in (False, True):
                    delivery, _, body = channel.basic_get(name, auto_ack=False)
                    self.assertIsNotNone(delivery)
                    self.assertEqual(retry, delivery.redelivered)
                    self.assertEqual(b"poison", body)
                    channel.basic_nack(delivery.delivery_tag, requeue=not retry)
                delivery, props, body = self.get_delivery(holder, channel, dead)
                self.assertIsNotNone(delivery)
                self.assertEqual(b"poison", body)
                self.assertEqual("rejected", props.headers["x-death"][0]["reason"])
                channel.basic_ack(delivery.delivery_tag)
                self.assertIsNone(channel.basic_get(name)[0])
                self.assertIsNone(channel.basic_get(dead)[0])
            finally:
                management.queue_delete(name)
                management.queue_delete(dead)

    def get_delivery(self, connection, channel, queue):
        deadline = monotonic() + 5
        while monotonic() < deadline:
            delivery = channel.basic_get(queue, auto_ack=False)
            if delivery[0] is not None:
                return delivery
            connection.sleep(0.1)
        self.fail(f"No delivery received from {queue} within five seconds")

    def test_parquet_exact_incremental_replay_and_lineage(self):
        source = {
            "2026-11-01": b"a,75000\nb,25000\n",
            "2026-11-02": b"a,75000\nc,-10000\n",
        }
        schema = pa.schema([
            ("event_id", pa.string()), ("minor_units", pa.int64()),
            ("source_date", pa.date32()), ("source_hash", pa.string()),
            ("transform_version", pa.string()),
        ])
        with TemporaryDirectory(prefix="epi-parquet-") as scratch, duckdb.connect() as query:
            root = Path(scratch)

            def ingest(day, payload):
                digest = sha256(payload).hexdigest()
                published = root / f"{day}-{digest}.parquet"
                if published.exists():
                    return False
                rows = []
                for record in io.StringIO(payload.decode("ascii")):
                    event_id, amount = record.strip().split(",")
                    rows.append({
                        "event_id": event_id, "minor_units": int(amount),
                        "source_date": date.fromisoformat(day), "source_hash": digest,
                        "transform_version": "m00-v1",
                    })
                partial = published.with_suffix(".part")
                pq.write_table(pa.Table.from_pylist(rows, schema=schema), partial)
                partial.replace(published)
                return True

            self.assertTrue(ingest("2026-11-01", source["2026-11-01"]))
            self.assertFalse(ingest("2026-11-01", source["2026-11-01"]))
            self.assertTrue(ingest("2026-11-02", source["2026-11-02"]))
            self.assertEqual(2, len(list(root.glob("*.parquet"))))

            def replay():
                return query.execute(
                    "SELECT event_id, min(minor_units), max(minor_units), count(DISTINCT source_hash), "
                    "count(DISTINCT transform_version) FROM read_parquet(?) GROUP BY event_id ORDER BY event_id",
                    [str(root / "*.parquet")],
                ).fetchall()

            expected = [("a", 75000, 75000, 2, 1), ("b", 25000, 25000, 1, 1), ("c", -10000, -10000, 1, 1)]
            self.assertEqual(expected, replay())
            self.assertEqual(90000, sum(row[1] for row in replay()))
