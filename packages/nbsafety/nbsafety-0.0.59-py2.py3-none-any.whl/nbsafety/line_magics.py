# -*- coding: future_annotations -*-
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, List
    from nbsafety.safety import NotebookSafety


# USAGE = """Options:
#
# show_graph:
#     - This will print out the dependency graph of global variables. Stale nodes are labeled red.
#       Notice that user might need to call this twice to have it to work.

USAGE = """Options:

show_dependency <variable_name> <variable_name2> ...: 
    - This will print out the dependencies for given global variables.
      Multiple variables should be separated with spaces.

show_stale: 
    - This will print out all the global variables that are stale. 

remove_dependency <parent_name> <child_name>:
    - This will remove the dependency between parent variable and the child variable.

add_dependency <parent_name> <child_name>:
    - This will add the dependency between parent variable and the child variable.

turn_off_warnings_for  <variable_name> <variable_name2> ...: 
    - This will turn off the warnings for given global variables. These variables will not be
      considered as stale anymore. Multiple variables should be separated with spaces.

turn_off_warnings_for  <variable_name> <variable_name2> ...: 
    - This will turn the warnings back on for given global variables. These variables could have
      stale dependencies now. Multiple variables should be separated with spaces."""


def show_deps(safety: NotebookSafety, line: List[str]):
    if len(line) == 1:
        print("Usage: %safety show_dependency <variable_name> <variable_name2> ...")
        return
    for data_sym_name in line[1:]:
        data_sym = safety.global_scope.lookup_data_symbol_by_name(data_sym_name)
        if data_sym:
            print("DataSymbol {} (defined {}; required {}) is dependent on {}".format(
                data_sym.readable_name,
                data_sym.defined_cell_num,
                data_sym.required_cell_num,
                [str(n) for n in data_sym.parents] if data_sym.parents else "Nothing"
            ))
        else:
            print("Cannot find DataSymbol", data_sym_name)


def show_stale(safety: NotebookSafety, line: List[str]):
    if len(line) < 2 or line[1] == 'global':
        dsym_sets: Any = [safety.global_scope.all_data_symbols_this_indentation()]
    elif line[1] == 'all':
        dsym_sets = safety.aliases.values()
    else:
        print("TODO: show usage statement")
        return
    stale_set = set()
    for dsym_set in dsym_sets:
        for data_sym in dsym_set:
            if data_sym.is_stale:
                stale_set.add(data_sym)
    if not stale_set:
        print("No DataSymbol has stale dependency for now!")
    elif len(stale_set) == 1:
        print("The only DataSymbol with stale dependencies is:", str(stale_set.pop()))
    else:
        print("DataSymbols with stale dependencies are:", [str(n) for n in stale_set])


def trace_messages(safety: NotebookSafety, line: List[str]):
    if len(line) != 2:
        print("Usage: %safety trace_messages [enabled|disabled] ...")
        return
    safety.settings.trace_messages_enabled = (line[1].lower().startswith("enable"))


def remove_dep(safety: NotebookSafety, line: List[str]):
    if len(line) != 3:
        print("Usage: %safety remove_dependency <parent_name> <child_name>")
        return
    parent_data_sym = safety.global_scope.lookup_data_symbol_by_name(line[1])
    if not parent_data_sym:
        print("Cannot find DataSymbol", line[1])
        return
    child_data_sym = safety.global_scope.lookup_data_symbol_by_name(line[2])
    if not child_data_sym:
        print("Cannot find DataSymbol", line[2])
        return
    if parent_data_sym not in child_data_sym.parents:
        print("Two DataSymbols do not have a dependency relation")
        return
    for children in parent_data_sym.children_by_cell_position.values():
        children.remove(child_data_sym)
    child_data_sym.parents.remove(parent_data_sym)


def add_dep(safety: NotebookSafety, line: List[str]):
    if len(line) != 3:
        print("Usage: %safety add_dependency <parent_name> <child_name>")
        return
    parent_data_sym = safety.global_scope.lookup_data_symbol_by_name(line[1])
    if not parent_data_sym:
        print("Cannot find DataSymbol", line[1])
        return
    child_data_sym = safety.global_scope.lookup_data_symbol_by_name(line[2])
    if not child_data_sym:
        print("Cannot find DataSymbol", line[2])
        return
    if parent_data_sym in child_data_sym.parents:
        print("Two DataSymbols already have a dependency relation")
        return
    parent_data_sym.children_by_cell_position[-1].add(child_data_sym)
    child_data_sym.parents.add(parent_data_sym)


def turn_off_warnings_for(safety: NotebookSafety, line: List[str]):
    if len(line) <= 1:
        print("Usage: %safety turn_off_warnings_for <variable_name> <variable_name2> ...")
        return
    for data_sym_name in line[1:]:
        data_sym = safety.global_scope.lookup_data_symbol_by_name(data_sym_name)
        if data_sym:
            data_sym.disable_warnings = True
            print("Warnings are turned off for", data_sym_name)
        else:
            print("Cannot find DataSymbol", data_sym_name)


def turn_on_warnings_for(safety: NotebookSafety, line: List[str]):
    if len(line) <= 1:
        print("Usage: %safety turn_on_warnings_for <variable_name> <variable_name2> ...")
        return
    for data_sym_name in line[1:]:
        data_sym = safety.global_scope.lookup_data_symbol_by_name(data_sym_name)
        if data_sym:
            data_sym.disable_warnings = False
            print("Warnings are turned on for", data_sym_name)
        else:
            print("Cannot find DataSymbol", data_sym_name)
