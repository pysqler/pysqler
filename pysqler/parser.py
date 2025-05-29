import ast
from dataclasses import dataclass

import sqlparse
from sqlparse.sql import Statement


@dataclass
class SqlAstNode:
    stmt: Statement
    node: ast.Constant
    has_placeholders: bool


def extract_sql_nodes(tree: ast.AST) -> list[SqlAstNode]:
    nodes: list[SqlAstNode] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant):
            continue

        if not isinstance(node.value, str):
            continue

        nodes.extend(
            SqlAstNode(stmt=stmt, node=node, has_placeholders=_find_placeholder(stmt))
            for stmt in _maybe_extract_sql_query(node)
        )

    return nodes


def _maybe_extract_sql_query(node: ast.Constant) -> list[Statement]:
    sql_str = ast.unparse(node)[1:-1]

    parsed = sqlparse.parse(sql_str)
    assert isinstance(parsed, tuple)
    result = []
    for stmt in parsed:
        for token in stmt:
            if token.is_keyword:
                result.append(stmt)
                break
    return result


def _find_placeholder(stmt: Statement) -> bool:
    q = [stmt.tokens]

    while q:
        tokens = q.pop()
        for token in tokens:
            if repr(token.ttype) == "Token.Name.Placeholder":
                return True
            if hasattr(token, "tokens"):
                q.append(token.tokens)

    return False
