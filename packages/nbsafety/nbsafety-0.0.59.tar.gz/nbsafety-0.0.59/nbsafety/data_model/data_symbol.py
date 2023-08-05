# -*- coding: future_annotations -*-
import ast
from collections import defaultdict
from enum import Enum
import logging
from typing import cast, TYPE_CHECKING
import weakref

from nbsafety.data_model.update_protocol import UpdateProtocol
from nbsafety.singletons import nbs

if TYPE_CHECKING:
    from typing import Any, Dict, Optional, Set, Union

    # avoid circular imports
    from nbsafety.data_model.scope import Scope, NamespaceScope

logger = logging.getLogger(__name__)


class DataSymbolType(Enum):
    DEFAULT = 'default'
    SUBSCRIPT = 'subscript'
    FUNCTION = 'function'
    CLASS = 'class'
    IMPORT = 'import'


class DataSymbol(object):
    def __init__(
        self,
        name: Union[str, int],
        symbol_type: DataSymbolType,
        obj: Any,
        containing_scope: Scope,
        stmt_node: Optional[ast.AST] = None,
        parents: Optional[Set[DataSymbol]] = None,
        refresh_cached_obj: bool = False,
        implicit: bool = False,
    ):
        if refresh_cached_obj:
            # TODO: clean up redundancies
            assert implicit
            assert stmt_node is None
        # print(containing_scope, name, obj, is_subscript)
        self.name = name
        self.symbol_type = symbol_type
        tombstone, obj_ref, has_weakref = self._update_obj_ref_inner(obj)
        self._tombstone = tombstone
        self._obj_ref = obj_ref
        self._has_weakref = has_weakref
        self.cached_obj_ref = None
        self._cached_has_weakref = None
        self.cached_obj_id = None
        self.cached_obj_type = None
        if refresh_cached_obj:
            self._refresh_cached_obj()
        self.containing_scope = containing_scope
        self.stmt_node = self.update_stmt_node(stmt_node)
        self._funcall_live_symbols = None
        if parents is None:
            parents = set()
        self.parents: Set[DataSymbol] = parents
        self.children_by_cell_position: Dict[int, Set[DataSymbol]] = defaultdict(set)

        self.call_scope: Optional[Scope] = None
        if self.is_function:
            self.call_scope = self.containing_scope.make_child_scope(self.name)

        self.defined_cell_num = nbs().cell_counter()

        # The notebook cell number this is required to have to not be considered stale
        self.required_cell_num = self.defined_cell_num

        self.fresher_ancestors: Set[DataSymbol] = set()
        self.namespace_stale_symbols: Set[DataSymbol] = set()

        # if implicitly created when tracing non-store-context ast nodes
        self._implicit = implicit

        # Will never be stale if no_warning is True
        self.disable_warnings = False

        nbs().aliases[id(obj)].add(self)

    @staticmethod
    def create_implicit(
        name: Union[str, int], obj: Any, containing_scope: Scope, symbol_type: Optional[DataSymbolType] = None
    ) -> DataSymbol:
        if symbol_type is None:
            symbol_type = DataSymbolType.DEFAULT
        dsym = DataSymbol(name, symbol_type, obj, containing_scope, refresh_cached_obj=True, implicit=True)
        # FIXME: hack to circumvent circular import
        if containing_scope.__class__.__name__ == 'NamespaceScope':
            containing_scope = cast('NamespaceScope', containing_scope)
            # this is to prevent refs to the scope object from being considered as stale if we just load it
            dsym.defined_cell_num = dsym.required_cell_num = containing_scope.max_defined_timestamp
        containing_scope.put(name, dsym)
        return dsym

    def __repr__(self) -> str:
        return f'<{self.readable_name}>'

    def __str__(self) -> str:
        return self.readable_name

    def __hash__(self):
        return hash(self.full_path)

    @property
    def readable_name(self) -> str:
        return self.containing_scope.make_namespace_qualified_name(self)

    @property
    def is_subscript(self):
        return self.symbol_type == DataSymbolType.SUBSCRIPT

    @property
    def is_class(self):
        return self.symbol_type == DataSymbolType.CLASS

    @property
    def is_function(self):
        return self.symbol_type == DataSymbolType.FUNCTION

    @property
    def is_import(self):
        return self.symbol_type == DataSymbolType.IMPORT

    @property
    def is_implicit(self):
        return self._implicit

    def _get_obj(self) -> Any:
        if self._has_weakref:
            return self._obj_ref()
        else:
            return self._obj_ref

    def _get_cached_obj(self) -> Any:
        if self._cached_has_weakref:
            return self.cached_obj_ref()
        else:
            return self.cached_obj_ref

    def shallow_clone(self, new_obj, new_containing_scope, symbol_type):
        return self.__class__(self.name, symbol_type, new_obj, new_containing_scope)

    @property
    def obj_id(self):
        return id(self._get_obj())

    @property
    def obj_type(self):
        return type(self._get_obj())

    @property
    def namespace(self):
        return nbs().namespaces.get(self.obj_id, None)

    @property
    def full_path(self):
        return self.containing_scope.full_path + (self.name,)

    @property
    def full_namespace_path(self):
        return self.containing_scope.make_namespace_qualified_name(self)

    @property
    def is_garbage(self):
        return (
            self._tombstone
            or self.containing_scope.is_garbage
            or not self.containing_scope.is_globally_accessible
            or (self._has_weakref and self._get_obj() is None)
        )

    @property
    def is_globally_accessible(self):
        return self.containing_scope.is_globally_accessible

    def _obj_reference_expired_callback(self, *_):
        # just write a tombstone here; we'll do a batch collect after the main part of the cell is done running
        # can potentially support GC in the background further down the line
        self._tombstone = True

    def collect_self_garbage(self):
        for parent in self.parents:
            for parent_children in parent.children_by_cell_position.values():
                parent_children.discard(self)
        for self_children in self.children_by_cell_position.values():
            for child in self_children:
                child.parents.discard(self)
        # kill the alias but leave the namespace
        # namespace needs to stick around to properly handle the staleness propagation protocol
        self._handle_aliases(readd=False)

    # def update_type(self, new_type):
    #     self.symbol_type = new_type
    #     if self.is_function:
    #         self.call_scope = self.containing_scope.make_child_scope(self.name)
    #     else:
    #         self.call_scope = None

    def update_obj_ref(self, obj, refresh_cached=True):
        tombstone, obj_ref, has_weakref = self._update_obj_ref_inner(obj)
        self._tombstone = tombstone
        self._obj_ref = obj_ref
        self._has_weakref = has_weakref
        if self.cached_obj_id is not None and self.cached_obj_id != self.obj_id:
            old_ns = nbs().namespaces.get(self.cached_obj_id, None)
            if old_ns is not None:
                old_ns.update_obj_ref(obj)
            self._handle_aliases()
        if refresh_cached:
            self._refresh_cached_obj()

    def _handle_aliases(self, readd=True):
        old_aliases = nbs().aliases.get(self.cached_obj_id, None)
        if old_aliases is not None:
            old_aliases.discard(self)
            if len(old_aliases) == 0:
                del nbs().aliases[self.cached_obj_id]
        if readd:
            nbs().aliases[self.obj_id].add(self)

    def _update_obj_ref_inner(self, obj):
        tombstone = False
        try:
            obj_ref = weakref.ref(obj, self._obj_reference_expired_callback)
            has_weakref = True
        except TypeError:
            obj_ref = obj
            has_weakref = False
        return tombstone, obj_ref, has_weakref

    def update_stmt_node(self, stmt_node):
        self.stmt_node = stmt_node
        self._funcall_live_symbols = None
        if self.is_function:
            nbs().statement_to_func_cell[id(stmt_node)] = self
        return stmt_node

    def _refresh_cached_obj(self):
        self.cached_obj_ref = self._obj_ref
        self.cached_obj_id = self.obj_id
        self.cached_obj_type = self.obj_type
        self._cached_has_weakref = self._has_weakref

    def get_call_args(self):
        # TODO: handle lambda, objects w/ __call__, etc
        args = set()
        if self.is_function:
            assert isinstance(self.stmt_node, ast.FunctionDef)
            for arg in self.stmt_node.args.args + self.stmt_node.args.kwonlyargs:
                args.add(arg.arg)
            if self.stmt_node.args.vararg is not None:
                args.add(self.stmt_node.args.vararg.arg)
            if self.stmt_node.args.kwarg is not None:
                args.add(self.stmt_node.args.kwarg.arg)
        return args

    def create_symbols_for_call_args(self):
        for arg in self.get_call_args():
            # TODO: ideally we should try to pass the object here
            self.call_scope.upsert_data_symbol_for_name(arg, None, set(), self.stmt_node, False, propagate=False)

    @property
    def is_stale(self):
        if self.disable_warnings:
            return False
        return self.defined_cell_num < self.required_cell_num or len(self.namespace_stale_symbols) > 0

    def should_mark_stale(self, updated_dep):
        if self.disable_warnings:
            return False
        if updated_dep is self:
            return False
        return True

    def update_deps(
        self, new_deps: Set['DataSymbol'], overwrite=True, mutated=False, propagate=True
    ):
        # skip updates for imported symbols
        if self.is_import:
            return
        # if we get here, no longer implicit
        self._implicit = False
        # quick last fix to avoid overwriting if we appear inside the set of deps to add
        overwrite = overwrite and self not in new_deps
        new_deps.discard(self)
        if overwrite:
            for parent in self.parents - new_deps:
                for parent_children in parent.children_by_cell_position.values():
                    parent_children.discard(self)
            self.parents = set()

        for new_parent in new_deps - self.parents:
            if new_parent is None:
                continue
            new_parent.children_by_cell_position[nbs().active_cell_position_idx].add(self)
            self.parents.add(new_parent)
        self.required_cell_num = -1
        UpdateProtocol(nbs(), self, new_deps, mutated)(propagate=propagate)
        self._refresh_cached_obj()
        nbs().updated_symbols.add(self)

    def refresh(self: DataSymbol):
        self.fresher_ancestors = set()
        self.defined_cell_num = nbs().cell_counter()
        self.namespace_stale_symbols = set()

    def _propagate_refresh_to_namespace_parents(self, seen: Set[DataSymbol]):
        if self in seen:
            return
        # print('refresh propagate', self)
        seen.add(self)
        for self_alias in nbs().aliases[self.obj_id]:
            containing_scope: NamespaceScope = cast('NamespaceScope', self_alias.containing_scope)
            if not containing_scope.is_namespace_scope:
                continue
            # if containing_scope.max_defined_timestamp == nbs().cell_counter():
            #     return
            containing_scope.max_defined_timestamp = nbs().cell_counter()
            containing_namespace_obj_id = containing_scope.obj_id
            # print('containing namespaces:', nbs().aliases[containing_namespace_obj_id])
            for alias in nbs().aliases[containing_namespace_obj_id]:
                alias.namespace_stale_symbols.discard(self)
                if not alias.is_stale:
                    alias.defined_cell_num = nbs().cell_counter()
                    alias.fresher_ancestors = set()
                # print('working on', alias, '; stale?', alias.is_stale, alias.namespace_stale_symbols)
                alias._propagate_refresh_to_namespace_parents(seen)
