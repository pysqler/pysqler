from dataclasses import dataclass
from typing import Any

from mimesis import Generic

from pysqler.parser import SqlAstNode
from pysqler.providers import _sqlite3


@dataclass
class InvalidSQL:
    node: SqlAstNode
    cause: Exception

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(node={self.node.stmt.normalized},"
            f" cause={self.cause!r})"
        )


def inspect_nodes(nodes: list[SqlAstNode], schema: list[str]) -> list[InvalidSQL]:
    conn = _sqlite3.mock_db(schema)
    invalid = []
    for node in nodes:
        args: tuple[Any, ...] = tuple(
            mock_data(_sqlite3.to_python_type(placeholder.sql_type))
            for placeholder in node.placeholders
        )

        query = node.stmt.normalized.replace("\\n", "")
        try:
            _sqlite3.execute(conn, query, args)
        except Exception as e:
            invalid.append(InvalidSQL(node=node, cause=e))

    return invalid


def mock_data[T](python_type: type[T]) -> T:
    generic = Generic()
    generators = {
        int: generic.numeric.integer_number,
        str: generic.text.text,
        bytes: generic.random.randbytes,
        float: generic.numeric.float_number,
    }
    result = generators[python_type]()  # type: ignore
    assert isinstance(result, python_type)
    return result
