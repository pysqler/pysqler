import ast
from pathlib import Path
from sqlite3 import OperationalError

from pysqler.parser import extract_sql_nodes
from pysqler.tester import inspect_nodes

ASSETS_PATH = Path(__file__).parent / "assets"
UNDERTEST = (ASSETS_PATH / "sql_queries.py").read_text()
SCHEMA = (ASSETS_PATH / "schema.sql").read_text().split(";\n")


def test_valid_query() -> None:
    tree = ast.parse(UNDERTEST)
    nodes = extract_sql_nodes(tree)
    invalids = inspect_nodes(nodes, schema=SCHEMA)
    expected = [
        OperationalError("no such table: non_existing_table"),
        OperationalError("no such table: non_existing_table"),
        OperationalError('near "SELEC": syntax error'),
        OperationalError("no such column: sda"),
        OperationalError("no such column: name"),
    ]
    assert len(invalids) == len(expected), invalids[len(expected)]
    for idx, invalid in enumerate(invalids):
        assert repr(invalid.cause) == repr(expected[idx]), repr(invalid.cause)
