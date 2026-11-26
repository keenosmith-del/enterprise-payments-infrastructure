"""Exercise synthetic analytical interchange without operational database access."""
from pathlib import Path
from tempfile import TemporaryDirectory

import duckdb
import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq


def run() -> tuple[int, int, int]:
    rows = [{"sample_id": "technical-1", "value": 7}, {"sample_id": "technical-2", "value": 3}]
    with TemporaryDirectory() as directory:
        target = Path(directory) / "synthetic.parquet"
        pq.write_table(pa.Table.from_pylist(rows), target)
        polars_total = int(pl.read_parquet(target).select(pl.col("value").sum()).item())
        with duckdb.connect() as db:
            count, total = db.execute("SELECT count(*), sum(value) FROM read_parquet(?)", [str(target)]).fetchone()
        return int(count), int(total), polars_total


if __name__ == "__main__":
    assert run() == (2, 10, 10)
    print("Synthetic Arrow, Parquet, Polars and DuckDB smoke passed")
