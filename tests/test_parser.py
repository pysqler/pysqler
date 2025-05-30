import ast
from pathlib import Path

from pysqler import parser

ASSETS_PATH = Path(__file__).parent / "assets"
UNDERTEST = (ASSETS_PATH / "sql_queries.py").read_text()


def test_extract_sql_nodes() -> None:
    tree = ast.parse(UNDERTEST)
    nodes = parser.extract_sql_nodes(tree)
    valid_sql_queries_amount = 9
    assert len(nodes) == valid_sql_queries_amount


def test_find_placeholder() -> None:
    tree = ast.parse(UNDERTEST)
    nodes = parser.extract_sql_nodes(tree)
    must_have_placeholders = [
        "INSERT INTO users (name, age, mode) VALUES (?, 123, ?);",
        "INSERT users (name, age, mode) VALUES (?, 123, 1);",
    ]
    for node in nodes:
        assert parser._find_placeholder(node.stmt) == (  # noqa: SLF001
            node.stmt.normalized in must_have_placeholders
        )
