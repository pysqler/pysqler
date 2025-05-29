from dataclasses import dataclass

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
        if node.has_placeholders:
            continue

        query = node.stmt.normalized.replace("\\n", "")
        try:
            _sqlite3.execute(conn, query)
        except Exception as e:
            invalid.append(InvalidSQL(node=node, cause=e))

    return invalid
