import ast
from dataclasses import dataclass

import sqlparse
from sqlparse.sql import Statement


@dataclass
class SqlAstNode:
    query: tuple[Statement, ...]
    node: ast.Constant


def extract_sql_nodes(tree: ast.AST) -> list[SqlAstNode]:
    nodes = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant):
            continue

        if not isinstance(node.value, str):
            continue

        if query := _maybe_extract_sql_query(node):
            nodes.append(SqlAstNode(query = query, node = node))

    return nodes


def _maybe_extract_sql_query(node: ast.Constant) -> None | tuple[Statement, ...]:
    sql_str = ast.unparse(node)[1:-1]

    parsed = sqlparse.parse(sql_str)
    assert isinstance(parsed, tuple)
    for stmt in parsed:
        for token in stmt:
            if token.is_keyword:
                return parsed
    return None

def _find_placeholder(stmt: Statement) -> bool:
    q = [stmt.tokens]

    while q:
        tokens = q.pop()
        for token in tokens:
            if repr(token.ttype) == "Token.Name.Placeholder":
                return True
            if hasattr(token, "tokens"):
                q.append(getattr(token, "tokens"))

    return False