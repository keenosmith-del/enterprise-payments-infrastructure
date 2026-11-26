"""Isolated synthetic feasibility checks. No application or payment adapter."""
import csv
from decimal import Decimal
from hashlib import sha256
import io
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


class LocalProbes(unittest.TestCase):
    def test_exact_minor_units(self):
        amounts = ("0.10", "0.20", "750.01")
        total = sum((Decimal(value) for value in amounts), Decimal(0))
        self.assertEqual(Decimal("750.31"), total)
        self.assertEqual(75031, int(total * 100))

    def test_provider_commit_then_lost_ack(self):
        provider = Path(__file__).with_name("provider_fixture.py")
        with TemporaryDirectory(prefix="epi-provider-") as scratch:
            database = Path(scratch) / "provider.sqlite3"

            def call(*args):
                return subprocess.run(
                    [sys.executable, str(provider), str(database), *args],
                    capture_output=True,
                    text=True,
                    check=False,
                )

            self.assertEqual(3, call("enquire", "absent").returncode)
            lost_ack = call("submit", "op-42", "75000", "--lose-ack")
            self.assertEqual(75, lost_ack.returncode)
            self.assertEqual("", lost_ack.stdout)
            result = call("enquire", "op-42")
            self.assertEqual(0, result.returncode, result.stderr)
            expected = {"operation": "op-42", "minor_units": 75000, "status": "executed"}
            self.assertEqual(expected, json.loads(result.stdout))
            replay = call("submit", "op-42", "75000")
            self.assertEqual(0, replay.returncode, replay.stderr)
            self.assertEqual(expected, json.loads(replay.stdout))
            self.assertEqual(4, call("submit", "op-42", "75001").returncode)
            with sqlite3.connect(database) as connection:
                observed = connection.execute("SELECT count(*), sum(minor_units) FROM execution").fetchone()
            self.assertEqual((1, 75000), observed)

    def test_sftp_subsystem_readiness_and_duplicate_file(self):
        candidates = (Path("/usr/libexec/sftp-server"), Path("/usr/lib/openssh/sftp-server"))
        server = next((path for path in candidates if path.is_file()), None)
        self.assertIsNotNone(server, "An installed OpenSSH sftp-server is required")
        self.assertIsNotNone(shutil.which("sftp"), "An installed OpenSSH client is required")
        original = b"reference,minor_units\nSYN-1,75000\n"
        with TemporaryDirectory(prefix="epi-sftp-") as directory:
            root = Path(directory)
            inbox = root / "inbox"
            inbox.mkdir()
            source = root / "source.csv"
            source.write_bytes(original)

            def transfer(*commands):
                subprocess.run(
                    ["sftp", "-q", "-D", str(server), "-b", "-"],
                    input="\n".join(commands) + "\n",
                    text=True,
                    check=True,
                    capture_output=True,
                    cwd=root,
                    timeout=15,
                )

            transfer("put source.csv inbox/batch.part")
            self.assertEqual([], list(inbox.glob("*.ready")))
            transfer(
                "rename inbox/batch.part inbox/batch.ready",
                "get inbox/batch.ready received.csv",
                "put source.csv inbox/replay.ready",
                "get inbox/replay.ready replay.csv",
            )
            expected_digest = sha256(original).hexdigest()
            processed = set()
            for name in ("received.csv", "replay.csv"):
                received = (root / name).read_bytes()
                digest = sha256(received).hexdigest()
                self.assertEqual(expected_digest, digest)
                processed.add(digest)
                reader = csv.DictReader(io.StringIO(received.decode("ascii")), strict=True)
                self.assertEqual(["reference", "minor_units"], reader.fieldnames)
                self.assertEqual([{"reference": "SYN-1", "minor_units": "75000"}], list(reader))
            self.assertEqual(1, len(processed))
