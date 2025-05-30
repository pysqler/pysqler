import ast
from pathlib import Path

import sqlparse

from pysqler import parser

ASSETS_PATH = Path(__file__).parent / "assets"
UNDERTEST = (ASSETS_PATH / "sql_queries.py").read_text()
SCHEMA = (ASSETS_PATH / "schema.sql").read_text()


def test_extract_sql_nodes() -> None:
    tree = ast.parse(UNDERTEST)
    nodes = parser.extract_sql_nodes(tree, parser.extract_schema_types(SCHEMA))
    valid_sql_queries_amount = 10
    assert len(nodes) == valid_sql_queries_amount


def test_find_placeholders() -> None:
    tree = ast.parse(UNDERTEST)
    nodes = parser.extract_sql_nodes(tree, parser.extract_schema_types(SCHEMA))
    must_have_placeholders = ["name", "age", "name", "age"]
    for node in nodes:
        placeholders = parser._find_placeholders(  # noqa: SLF001
            parser.extract_schema_types(SCHEMA), node.stmt
        )
        for idx, placeholder in enumerate(placeholders):
            print(placeholder.table)
            assert placeholder.field_name == must_have_placeholders[idx]


def test_extract_fields_types() -> None:
    parsed = sqlparse.parse(SCHEMA)
    expected = {"age": "INTEGER", "id": "INTEGER", "mood": "TEXT", "name": "TEXT"}
    assert parser.extract_fields_types(parsed[0]) == expected
