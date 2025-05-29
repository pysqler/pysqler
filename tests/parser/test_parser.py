import ast
from pathlib import Path

from pysqler import parser

from . import sql_queries

UNDERTEST = Path(sql_queries.__file__).read_text()

def test_extract_sql_nodes() -> None:
    tree = ast.parse(UNDERTEST)
    nodes = parser.extract_sql_nodes(tree)
    valid_sql_queries_amount = 3
    assert len(nodes) == valid_sql_queries_amount
