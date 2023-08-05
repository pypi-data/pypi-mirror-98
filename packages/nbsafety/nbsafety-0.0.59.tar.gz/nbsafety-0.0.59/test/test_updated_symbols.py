# -*- coding: future_annotations -*-
import logging

from nbsafety.singletons import nbs
from .utils import make_safety_fixture

logging.basicConfig(level=logging.ERROR)

# Reset dependency graph before each test
_safety_fixture, run_cell_ = make_safety_fixture()


def updated_symbol_names():
    return sorted(map(lambda sym: sym.readable_name, nbs().updated_symbols))


def run_cell(cell):
    # print()
    # print('*******************************************')
    # print('running', cell)
    # print('*******************************************')
    # print()
    run_cell_(cell)


def test_simplest():
    run_cell('a = 0')
    assert updated_symbol_names() == ['a']
    run_cell('a += 1')
    assert updated_symbol_names() == ['a']


def test_dict_hierarchy():
    run_cell('d = {}')
    assert updated_symbol_names() == ['d']
    run_cell('d["foo"] = {}')
    assert updated_symbol_names() == sorted(['d[foo]', 'd'])
    run_cell('d["foo"]["bar"] = []')
    assert updated_symbol_names() == sorted(['d[foo][bar]', 'd[foo]', 'd'])
    run_cell('d["foo"]["bar"] = 0')
    assert updated_symbol_names() == sorted(['d[foo][bar]', 'd[foo]', 'd'])
