import ast
import os
import re

SELECT_REGEX = re.compile(".*select.+from.*")
UPDATE_REGEX = re.compile(r".*update.*set.*=.*")
DELETE_REGEX = re.compile(r".*delete.*from.*")
SQL_QUERY_REGEXES = (SELECT_REGEX, UPDATE_REGEX, DELETE_REGEX)


def traverse_ast(tree: ast.AST) -> list[ast.Constant]:
    sql_nodes = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant):
            continue

        if not isinstance(node.value, str):
            continue

        if not has_sql_format(node.value):
            continue

        sql_nodes.append(node)

    return sql_nodes


def has_sql_format(s: str) -> bool:
    """
    >>> has_sql_format("UPDATE online_order SET status = $2 WHERE id = $1 and status < $2")
    True
    >>> has_sql_format("SELECT * FROM user_account WHERE id IN (SELECT user_account_id from dummy_user)")
    True
    >>> has_sql_format("delete from transaction where customer_id > 2;")
    True
    """
    s = s.lower()
    return any(regex.search(s) for regex in SQL_QUERY_REGEXES)


def main():
    py_modules = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                py_modules.append(os.path.join(root, file))

    for file in py_modules:
        with open(file) as f:
            tree = ast.parse(f.read())
        nodes = traverse_ast(tree)
        if not nodes:
            continue
        print(f"{file=}, {len(nodes)=}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        import doctest

        doctest.testmod()
    else:
        main()
