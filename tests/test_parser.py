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


def test_find_placeholders() -> None:
    tree = ast.parse(UNDERTEST)
    nodes = parser.extract_sql_nodes(tree)
    must_have_placeholders = ["name", "age", "name", "age"]
    for node in nodes:
        placeholders = parser._find_placeholders(node.stmt)
        for idx, placeholder in enumerate(placeholders):
            print(placeholder.table)
            assert placeholder.field_name == must_have_placeholders[idx]
