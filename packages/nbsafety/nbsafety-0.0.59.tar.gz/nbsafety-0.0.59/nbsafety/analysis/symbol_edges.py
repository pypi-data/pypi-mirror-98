# -*- coding: future_annotations -*-
import ast
from collections import defaultdict
import logging
from typing import Any, List, Sequence, TYPE_CHECKING

from nbsafety.analysis.mixins import SaveOffAttributesMixin, SkipUnboundArgsMixin, VisitListsMixin

if TYPE_CHECKING:
    from typing import Dict, Optional, Set, Tuple, Union


logger = logging.getLogger(__name__)


class TiedTuple(tuple):
    """Just a marker class indicating that we should not unpack contents of this tuple"""
    pass


class LiteralInfo:
    def __init__(self, items, node_id):
        self.items = items
        self.node_id = node_id

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, item):
        return self.items[item]


_MULTIPLE_SYMBOL_TYPES = (tuple, LiteralInfo, TiedTuple)
_UNPACKABLE_SYMBOL_TYPES = (tuple, LiteralInfo)


def _flatten(vals):
    for v in vals:
        if isinstance(v, _UNPACKABLE_SYMBOL_TYPES):
            yield from _flatten(v)
        else:
            yield v


def _seek_literal_node_id(vals):
    if isinstance(vals, LiteralInfo):
        return vals.node_id
    elif isinstance(vals, _MULTIPLE_SYMBOL_TYPES):
        possible = [_seek_literal_node_id(v) for v in vals]
        possible = [v for v in possible if v is not None]
        if len(possible) == 1:
            return possible[0]
    return None


class GetSymbolEdges(SaveOffAttributesMixin, SkipUnboundArgsMixin, VisitListsMixin, ast.NodeVisitor):
    def __init__(self):
        # TODO: figure out how to give these type annotations
        self.lval_symbols: List[Any] = []
        self.rval_symbols: List[Any] = []
        self.literal_lval_symbols_to_node_id: Dict[Union[str, int]] = {}
        self.simple_edges: List[Any] = []
        self.gather_rvals = True
        self.should_overwrite = True
        self.assignment_seen = False

    def _edges(self, lvals, rvals):
        if isinstance(lvals, _MULTIPLE_SYMBOL_TYPES) and isinstance(rvals, _MULTIPLE_SYMBOL_TYPES):
            yield from self._edges_from_tuples(lvals, rvals)
        elif isinstance(lvals, _MULTIPLE_SYMBOL_TYPES):
            # TODO: yield edges with subscript symbols
            for left in _flatten(lvals):
                yield left, rvals
        elif isinstance(rvals, _MULTIPLE_SYMBOL_TYPES):
            # node_id = _seek_literal_node_id(rvals)
            # if node_id is not None:
            #     self.literal_lval_symbols_to_node_id[lvals] = node_id
            if isinstance(rvals, LiteralInfo):
                self.literal_lval_symbols_to_node_id[lvals] = rvals.node_id
            # TODO: yield edges with subscript symbols
            for right in _flatten(rvals):
                yield lvals, right
        else:
            yield lvals, rvals

    def _edges_from_tuples(self, lvals, rvals):
        if isinstance(rvals, TiedTuple):
            for lval in lvals:
                yield from self._edges(lval, rvals)
        elif len(lvals) == len(rvals):
            for left, right in zip(lvals, rvals):
                yield from self._edges(left, right)
        elif len(lvals) == 1:
            yield from self._edges(lvals[0], rvals)
        elif len(rvals) == 1:
            yield from self._edges(lvals, rvals[0])
        else:
            raise ValueError('Incompatible lists: %s, %s' % (lvals, rvals))

    def __call__(self, node: ast.AST):
        self.visit(node)
        if not self.assignment_seen:
            self._collect_simple_edges()
            self.lval_symbols = []
            self.rval_symbols = []
        yield from self.simple_edges
        for lval_list in self.lval_symbols:
            try:
                edges_for_lval = list(self._edges(lval_list, tuple(self.rval_symbols)))
            except Exception as e:
                # TODO: only show warning if not in prod mode
                logger.warning('Exception occurred while computing symbol edges: %s', e)
                continue
            if len(edges_for_lval) == 0:
                for lval in lval_list:
                    yield lval, None
            else:
                yield from edges_for_lval

    def _collect_simple_edges(self):
        if len(self.lval_symbols) == 0:
            self.lval_symbols.append(None)
        if len(self.rval_symbols) == 0:
            self.rval_symbols.append(None)
        for lval in set(_flatten(self.lval_symbols)):
            for rval in set(_flatten(self.rval_symbols)):
                if lval is None and rval is None:
                    continue
                self.simple_edges.append((lval, rval))

    def gather_lvals_context(self):
        return self.push_attributes(gather_rvals=False)

    def gather_rvals_context(self):
        return self.push_attributes(gather_rvals=True)

    @property
    def to_add_set(self):
        if self.gather_rvals:
            return self.rval_symbols
        else:
            return self.lval_symbols

    @to_add_set.setter
    def to_add_set(self, val):
        if self.gather_rvals:
            self.rval_symbols = val
        else:
            self.lval_symbols = val

    def visit_Name(self, node):
        self.to_add_set.append(node.id)

    def visit_Num(self, node):
        self.visit_Constant(node)

    def visit_Str(self, node):
        self.visit_Constant(node)

    def visit_Constant(self, node):
        self.to_add_set.append(None)

    def visit_NameConstant(self, node):
        self.to_add_set.append(None)

    def visit_Tuple(self, node):
        self.visit_List_or_Tuple(node)

    def visit_List(self, node):
        self.visit_List_or_Tuple(node)

    def visit_Dict(self, node):
        temp = self.to_add_set
        self.to_add_set = []
        self.visit(node.keys)
        self.visit(node.values)
        self.to_add_set, temp = temp, self.to_add_set
        self.to_add_set.append(LiteralInfo(tuple(temp), id(node)))

    def visit_List_or_Tuple(self, node):
        temp = self.to_add_set
        self.to_add_set = []
        self.visit(node.elts)
        self.to_add_set, temp = temp, self.to_add_set
        self.to_add_set.append(LiteralInfo(tuple(temp), id(node)))

    def visit_expr(self, node):
        if hasattr(ast, 'NamedExpr') and isinstance(node, getattr(ast, 'NamedExpr')):
            self.visit_NamedExpr(node)
            return
        assert self.gather_rvals
        temp = self.to_add_set
        self.to_add_set = []
        super().generic_visit(node)
        self.to_add_set, temp = temp, self.to_add_set
        self.to_add_set.append(tuple(temp))

    def generic_visit(self, node: Union[ast.AST, Sequence[ast.AST]]):
        # The purpose of this is to make sure we call our visit_expr method if we see an expr
        if node is None:
            return
        elif isinstance(node, ast.expr):
            self.visit_expr(node)
        else:
            super().generic_visit(node)

    def visit_Assign(self, node):
        self.assignment_seen = True
        with self.gather_lvals_context():
            for target in node.targets:
                target_lval_symbols = []
                with self.push_attributes(lval_symbols=target_lval_symbols):
                    self.visit(target)
                if isinstance(target, (ast.List, ast.Tuple)):
                    # not strictly necessary since we are robust to this later,
                    # but helps avoid unncessary double nesting, e.g., ((a, b, c),)
                    assert len(target_lval_symbols) == 1
                    assert isinstance(target_lval_symbols[0], _MULTIPLE_SYMBOL_TYPES)
                    self.lval_symbols.append(target_lval_symbols[0])
                else:
                    self.lval_symbols.append(tuple(target_lval_symbols))
        with self.gather_rvals_context():
            self.visit(node.value)

    def visit_AugAssign_or_AnnAssign(self, node):
        with self.push_attributes(lval_symbols=[], rval_symbols=[]):
            with self.gather_lvals_context():
                self.visit(node.target)
            with self.gather_rvals_context():
                self.visit(node.value)
            self._collect_simple_edges()

    def visit_AnnAssign(self, node):
        self.visit_AugAssign_or_AnnAssign(node)

    def visit_AugAssign(self, node):
        self.should_overwrite = False
        self.visit_AugAssign_or_AnnAssign(node)

    def visit_Call(self, node):
        extra_to_add = []
        if isinstance(node.func, (ast.Attribute, ast.Subscript, ast.Call)):
            # TODO: descend further down
            extra_to_add.append(id(node))
        else:
            assert isinstance(node.func, ast.Name)
            extra_to_add.append(node.func.id)
        temp = self.to_add_set
        self.to_add_set = []
        self.generic_visit([node.args, node.keywords])
        self.to_add_set, temp = temp, self.to_add_set
        temp = TiedTuple(set(_flatten(temp)) | set(extra_to_add))
        self.to_add_set.append(temp)

    def visit_Attribute_or_Subscript(self, node):
        # TODO: we'll ignore args inside of inner calls, e.g. f.g(x, y).h; need to descend further down
        self.to_add_set.append(id(node))

    def visit_Attribute(self, node):
        self.visit_Attribute_or_Subscript(node)

    def visit_Subscript(self, node):
        if self.gather_rvals:
            temp = self.to_add_set
            self.to_add_set = []
            self.visit_Attribute_or_Subscript(node)
            # add slice to RHS to avoid propagating to it
            self.visit(node.slice)
            self.to_add_set, temp = temp, self.to_add_set
            self.to_add_set.append(tuple(temp))
        else:
            self.visit_Attribute_or_Subscript(node)

    # def visit_Subscript(self, node):
    #     self.visit_Attribute_or_Subscript(node)
    #     # TODO: the reason we wanted this before is to avoid propagating to the slice
    #     #  add something back in to avoid propagating to everything on RHS
    #     # if self.gather_rvals:
    #     #     self.visit(node.slice)

    def visit_Keyword(self, node):
        self.visit(node.value)

    def visit_Starred(self, node):
        self.visit(node.value)

    def visit_Lambda(self, node):
        assert self.gather_rvals
        # remove node.arguments
        self.visit(node.body)
        self.visit(node.args)
        with self.push_attributes(rval_symbols=[]):
            self.visit(node.args.args)
            self.visit(node.args.vararg)
            self.visit(node.args.kwonlyargs)
            self.visit(node.args.kwarg)
            discard_set = set(self.rval_symbols)
        # throw away anything appearing in lambda body that isn't bound
        self.rval_symbols = list(set(self.rval_symbols) - discard_set)

    def visit_GeneratorExp(self, node):
        self.visit_GeneratorExp_or_DictComp_or_ListComp_or_SetComp(node)

    def visit_DictComp(self, node):
        self.visit_GeneratorExp_or_DictComp_or_ListComp_or_SetComp(node)

    def visit_ListComp(self, node):
        self.visit_GeneratorExp_or_DictComp_or_ListComp_or_SetComp(node)

    def visit_SetComp(self, node):
        self.visit_GeneratorExp_or_DictComp_or_ListComp_or_SetComp(node)

    def visit_GeneratorExp_or_DictComp_or_ListComp_or_SetComp(self, node):
        assert self.gather_rvals
        to_append = set()
        for gen in node.generators:
            if isinstance(gen, ast.comprehension):
                with self.push_attributes(rval_symbols=[]):
                    self.visit(gen.iter)
                    self.visit(gen.ifs)
                    to_append |= set(_flatten(self.rval_symbols))
                with self.push_attributes(rval_symbols=[]):
                    self.visit(gen.target)
                    discard_set = set(self.rval_symbols)
            else:
                with self.push_attributes(rval_symbols=[]):
                    self.visit(gen)
                    discard_set = set(self.rval_symbols)
            to_append -= discard_set
        self.rval_symbols.append(TiedTuple(to_append))

    def visit_arg(self, node):
        self.to_add_set.append(node.arg)

    def visit_For(self, node):
        # skip body -- will have dummy since this visitor works line-by-line
        with self.push_attributes(lval_symbols=[], rval_symbols=[]):
            with self.gather_lvals_context():
                self.visit(node.target)
            with self.gather_rvals_context():
                self.visit(node.iter)
            self._collect_simple_edges()

    def visit_If(self, node):
        # skip body here too
        self.visit(node.test)

    def visit_FunctionDef_or_AsyncFunctionDef(self, node):
        with self.push_attributes(lval_symbols=[], rval_symbols=[]):
            self.lval_symbols.append(node.name)
            with self.gather_rvals_context():
                self.visit(node.args)
                self.visit(node.decorator_list)
            self._collect_simple_edges()

    def visit_FunctionDef(self, node):
        self.visit_FunctionDef_or_AsyncFunctionDef(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef_or_AsyncFunctionDef(node)

    def visit_ClassDef(self, node):
        with self.push_attributes(lval_symbols=[], rval_symbols=[]):
            self.lval_symbols.append(node.name)
            with self.gather_rvals_context():
                self.visit(node.bases)
                self.visit(node.decorator_list)
            self._collect_simple_edges()

    def visit_With(self, node):
        # skip body
        self.visit(node.items)

    def visit_withitem(self, node):
        with self.gather_lvals_context():
            self.visit(node.optional_vars)
        with self.gather_rvals_context():
            self.visit(node.context_expr)

    def visit_Import(self, node: ast.Import):
        self.visit_Import_or_ImportFrom(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        self.visit_Import_or_ImportFrom(node)

    def visit_Import_or_ImportFrom(self, node: Union[ast.Import, ast.ImportFrom]):
        with self.push_attributes(lval_symbols=[], rval_symbols=[]):
            for name in node.names:
                if name.asname is None:
                    if name.name != '*' and '.' not in name.name:
                        self.lval_symbols.append(name.name)
                else:
                    self.lval_symbols.append(name.asname)
            self._collect_simple_edges()

    def visit_NamedExpr(self, node):
        with self.push_attributes(lval_symbols=[], rval_symbols=[]):
            with self.gather_lvals_context():
                self.visit(node.target)
            with self.gather_rvals_context():
                self.visit(node.value)
            rvals_to_extend = self.lval_symbols + self.rval_symbols
            self._collect_simple_edges()
        self.rval_symbols.extend(rvals_to_extend)


def get_assignment_lval_and_rval_symbol_refs(node: Union[str, ast.AST]):
    if isinstance(node, str):
        node = ast.parse(node).body[0]
    yield from GetSymbolEdges()(node)


# TODO: refine type sig
def get_symbol_edges(node: Union[str, ast.AST]) -> Tuple[Any, Any, bool]:
    if isinstance(node, str):
        node = ast.parse(node).body[0]
    visitor = GetSymbolEdges()
    edges: Dict[Optional[Union[str, int]], Set[Optional[Union[str, int]]]] = defaultdict(set)
    for edge in visitor(node):
        left, right = edge
        edges[left].add(right)
    return edges, visitor.literal_lval_symbols_to_node_id, visitor.should_overwrite
