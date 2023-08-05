import ast
import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, List, Set


class StatementMapper(ast.NodeVisitor):
    def __init__(self, line_to_stmt_map: 'Dict[int, ast.stmt]', id_map: 'Dict[int, ast.AST]'):
        self.line_to_stmt_map = line_to_stmt_map
        self.id_map = id_map
        self.traversal: 'List[ast.AST]' = []

    def __call__(self, node: 'ast.AST') -> 'Dict[int, ast.AST]':
        # for some bizarre reason we need to visit once to clear empty nodes apparently
        self.visit(node)
        self.traversal.clear()
        
        self.visit(node)
        orig_traversal = self.traversal
        self.traversal = []
        self.visit(copy.deepcopy(node))
        copy_traversal = self.traversal
        orig_to_copy_mapping = {}
        for no, nc in zip(orig_traversal, copy_traversal):
            orig_to_copy_mapping[id(no)] = nc
            self.id_map[id(nc)] = nc
            if isinstance(nc, ast.stmt):
                self.line_to_stmt_map[nc.lineno] = nc
                # workaround for python >= 3.8 wherein function calls seem
                # to yield trace frames that use the lineno of the first decorator
                for decorator in getattr(nc, 'decorator_list', []):
                    self.line_to_stmt_map[decorator.lineno] = nc
        return orig_to_copy_mapping

    def visit(self, node):
        self.traversal.append(node)
        for name, field in ast.iter_fields(node):
            if isinstance(field, ast.AST):
                self.visit(field)
            elif isinstance(field, list):
                for inner_node in field:
                    if isinstance(inner_node, ast.AST):
                        self.visit(inner_node)
