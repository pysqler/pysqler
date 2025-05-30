import ast
from collections.abc import Iterable
from dataclasses import dataclass

import sqlparse
from sqlparse.sql import (
    Identifier,
    IdentifierList,
    Parenthesis,
    Statement,
    Token,
    TokenList,
    Values,
)

TableName = str
SqlFieldName = str
SqlFieldType = str
SqlFieldsTypes = dict[SqlFieldName, SqlFieldType]


@dataclass
class Placeholder:
    value: str


@dataclass
class SQLPlaceHolder:
    table: TableName
    field_name: SqlFieldName
    sql_type: SqlFieldType


@dataclass
class SqlAstNode:
    stmt: Statement
    node: ast.Constant
    placeholders: list[SQLPlaceHolder]


def extract_sql_nodes(
    tree: ast.AST, schema: dict[TableName, SqlFieldsTypes]
) -> list[SqlAstNode]:
    nodes: list[SqlAstNode] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant):
            continue

        if not isinstance(node.value, str):
            continue

        nodes.extend(
            SqlAstNode(
                stmt=stmt, node=node, placeholders=_find_placeholders(schema, stmt)
            )
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


def _find_placeholders(
    schema: dict[TableName, SqlFieldsTypes], stmt: Statement
) -> list[SQLPlaceHolder]:
    placeholders = []
    table_name = _extract_table_name(stmt)
    fields = extract_fields(stmt)
    values = extract_values(stmt)
    assert len(fields) == len(values), f"{len(fields)=}, {len(values)=}"
    for idx, value in enumerate(values):
        if isinstance(value, Placeholder):
            placeholder = SQLPlaceHolder(
                table=table_name,
                field_name=fields[idx],
                sql_type=schema[table_name][fields[idx]],
            )
            placeholders.append(placeholder)
    return placeholders


def _extract_table_name(stmt: Statement) -> str:
    for token in walk_tokens(stmt):
        if isinstance(token, Identifier):
            return token.normalized
    raise ValueError


def extract_fields(stmt: Statement) -> list[str]:
    fields: list[str] = []
    for token in walk_tokens(stmt):
        if isinstance(token, Parenthesis):
            for identifier_list in token.tokens:
                if isinstance(identifier_list, IdentifierList):
                    fields.extend(
                        identifier.value
                        for identifier in identifier_list
                        if isinstance(identifier, Identifier)
                    )
    return fields


def extract_schema_types(schema: str) -> dict[TableName, SqlFieldsTypes]:
    schema_types: dict[TableName, SqlFieldsTypes] = {}
    parsed = sqlparse.parse(schema)
    for stmt in parsed:
        table_name = _extract_table_name(stmt)
        fields_types = extract_fields_types(stmt)
        schema_types[table_name] = fields_types
    return schema_types


def extract_fields_types(stmt: Statement) -> SqlFieldsTypes:
    result: SqlFieldsTypes = {}
    for token in walk_tokens(stmt):
        if isinstance(token, Parenthesis):
            field = None
            field_type = None
            for identifier in token.tokens:
                if isinstance(identifier, IdentifierList):
                    for deep_identifier in identifier.tokens:
                        if isinstance(deep_identifier, Identifier):
                            field = deep_identifier.value
                if isinstance(identifier, Identifier):
                    field = identifier.value
                if repr(identifier.ttype) == "Token.Name.Builtin":
                    field_type = identifier.value
                if field is not None and field_type is not None:
                    print(f"{field=}, {field_type=}")
                    result[field] = field_type
                    field = None
                    field_type = None
    return result


def extract_values(stmt: Statement) -> list[Placeholder | str]:
    values: list[Placeholder | str] = []
    for token in walk_tokens(stmt):
        if not isinstance(token, Values):
            continue
        for param in token.tokens:
            if not isinstance(param, Parenthesis):
                continue
            for identifier_list in param.tokens:
                if not isinstance(identifier_list, IdentifierList):
                    continue
                for identifier in identifier_list.tokens:
                    if (
                        repr(identifier.ttype) != "Token.Punctuation"
                        and repr(identifier.ttype) != "Token.Text.Whitespace"
                    ):
                        if repr(identifier.ttype) == "Token.Name.Placeholder":
                            values.append(Placeholder(value=identifier.value))
                        else:
                            values.append(identifier.value)
    return values


def walk_tokens(token_list: TokenList) -> Iterable[Token]:
    for token in token_list.tokens:
        yield token
        if isinstance(token, TokenList):
            yield from walk_tokens(token)
