import ast
from pathlib import Path

from pysqler.parser import extract_sql_nodes
from pysqler.tester import inspect_nodes

ASSETS_PATH = Path(__file__).parent / "assets"
UNDERTEST = (ASSETS_PATH / "sql_queries.py").read_text()
SCHEMA = (ASSETS_PATH / "schema.sql").read_text().split(";\n")


def test_valid_query() -> None:
    tree = ast.parse(UNDERTEST)
    nodes = extract_sql_nodes(tree)
    invalid = inspect_nodes(nodes, schema=SCHEMA)

    assert invalid == []
