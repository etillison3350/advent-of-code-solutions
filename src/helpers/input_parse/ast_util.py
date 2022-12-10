from typing import Any, Iterable, Optional
from typing import TypeVar

import ast


def ast_call_attr(
        target: ast.AST,
        attr_name: str,
        args: Optional[Iterable[ast.AST | Any]] = None,
        keyword_args: Optional[Iterable[ast.AST | Any]] = None
) -> ast.AST:
    # noinspection PyTypeChecker
    return ast.Call(ast.Attribute(target, attr_name),
                    [] if args is None else list(args),
                    [] if keyword_args is None else list(keyword_args))
