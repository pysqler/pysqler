import ast
from dataclasses import dataclass

import sqlparse
from sqlparse.sql import Statement, Token, Identifier
from collections.abc import Iterable

@dataclass
class SQLPlaceHolder:
    table: str
    field_name: str

@dataclass
class SqlAstNode:
    stmt: Statement
    node: ast.Constant
    has_placeholders: list[SQLPlaceHolder]


def extract_sql_nodes(tree: ast.AST) -> list[SqlAstNode]:
    nodes: list[SqlAstNode] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant):
            continue

        if not isinstance(node.value, str):
            continue

        nodes.extend(
            SqlAstNode(stmt=stmt, node=node, has_placeholders=_find_placeholders(stmt))
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

def _find_placeholders(stmt: Statement) -> list[SQLPlaceHolder]:
    q = [stmt.tokens]
    placeholders = [SQLPlaceHolder]
    table_name = _extract_table_name(stmt)

    for token in walk_token(stmt):
        fields = []
        if repr(token.ttype) == "Token.Name.Placeholder":
            return []

    return []

def _extract_table_name(stmt: Statement) -> str:
    for token in walk_token(stmt):
        if isinstance(token, Identifier):
            return token.normalized
    raise ValueError

def walk_token(token_list: Statement.tokens) -> Iterable[Token]:
    q = [token_list.tokens]
    while q:
        for token in q.pop():
            yield token
            if hasattr(token, "tokens"):
                q.append(token.tokens)