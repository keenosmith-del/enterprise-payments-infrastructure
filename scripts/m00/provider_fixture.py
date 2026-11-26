"""Process-isolated operation identity fixture for M00. No funds move."""
import argparse
import json
import os
import sqlite3
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("database")
    actions = parser.add_subparsers(dest="action", required=True)
    actions.add_parser("enquire").add_argument("operation")
    submit = actions.add_parser("submit")
    submit.add_argument("operation")
    submit.add_argument("minor_units", type=int)
    submit.add_argument("--lose-ack", action="store_true")
    args = parser.parse_args()
    if args.action == "submit" and not 0 < args.minor_units < 2**63:
        parser.error("minor_units must be a positive signed 64-bit integer")

    with sqlite3.connect(args.database, isolation_level=None) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS execution "
            "(operation TEXT PRIMARY KEY, minor_units INTEGER NOT NULL CHECK (minor_units > 0))"
        )
        if args.action == "submit":
            connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT minor_units FROM execution WHERE operation = ?", (args.operation,)
        ).fetchone()
        if args.action == "enquire":
            if row is None:
                return 3
            amount = row[0]
        else:
            amount = args.minor_units
            if row is not None and row[0] != amount:
                connection.rollback()
                return 4
            if row is None:
                connection.execute("INSERT INTO execution VALUES (?, ?)", (args.operation, amount))
            connection.commit()
            if args.lose_ack:
                os._exit(75)

    print(json.dumps({"operation": args.operation, "minor_units": amount, "status": "executed"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
