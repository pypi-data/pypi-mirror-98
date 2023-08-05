# -*- coding: future_annotations -*-
import logging

from nbsafety.singletons import nbs
from .utils import assert_bool, make_safety_fixture, skipif_known_failing

logging.basicConfig(level=logging.ERROR)

# Reset dependency graph before each test
_safety_fixture, run_cell_ = make_safety_fixture(setup_cells=['from nbsafety.utils import DotDict'])
run_cell = run_cell_


def stale_detected():
    return nbs().test_and_clear_detected_flag()


def assert_detected(msg=''):
    assert_bool(stale_detected(), msg=msg)


def assert_not_detected(msg=''):
    assert_bool(not stale_detected(), msg=msg)


def lookup_symbol(val):
    safety = nbs()
    val_id = id(val)
    if val_id not in safety.aliases:
        return None
    alias_set = safety.aliases[val_id]
    if len(alias_set) == 0:
        return None
    return next(iter(alias_set))


def test_basic():
    run_cell('d = DotDict()')
    run_cell('d.x = DotDict()')
    run_cell('d.y = DotDict()')
    run_cell('d.x.a = 5')
    # run_cell('d.x.b = 6')
    run_cell('logging.info(d.x.a)')
    assert_not_detected()
    run_cell('logging.info(d.x)')
    assert_not_detected()
    run_cell('d.y.a = 7')
    # run_cell('d.y.b = 8')
    run_cell('logging.info(d.y.a)')
    assert_not_detected()
    run_cell('logging.info(d.y)')
    assert_not_detected()
    run_cell('x = d.x.a + 9')
    run_cell('y = d.y.a + 9')
    run_cell('d.y.a = 9')
    run_cell('logging.info(x)')
    assert_not_detected('`x` independent of changed `d.y.a`')
    run_cell('logging.info(y)')
    assert_detected('`y` depends on changed `d.y.a`')
    run_cell('logging.info(d.x.a)')
    assert_not_detected()
    run_cell('logging.info(d.x)')
    assert_not_detected()
    run_cell('logging.info(d)')
    assert_not_detected()
    run_cell('d.y = 10')
    run_cell('logging.info(x)')
    assert_not_detected('`x` independent of changed `d.y`')
    run_cell('logging.info(y)')
    assert_detected('`y` depends on changed `d.y`')


def test_nested_readable_name():
    run_cell('d = DotDict()')
    run_cell('d.x = DotDict()')
    run_cell('d.x.a = 5')
    run_cell('d.x.b = 6')
    d_x_a = lookup_symbol(5)
    assert d_x_a.readable_name == 'd.x.a'
    d_x_b = lookup_symbol(6)
    assert d_x_b.readable_name == 'd.x.b'
    run_cell('d.y = DotDict()')
    run_cell('d.y.a = 7')
    run_cell('d.y.b = 8')
    d_y_a = lookup_symbol(7)
    assert d_y_a.readable_name == 'd.y.a'
    d_y_b = lookup_symbol(8)
    assert d_y_b.readable_name == 'd.y.b'


def test_nested_readable_name_dict_literal():
    run_cell('d = {"x": {"y": 42}}')
    d_x_y = lookup_symbol(42)
    assert d_x_y.readable_name == 'd[x][y]', 'got %s when expected d[x][y]' % d_x_y.readable_name


def test_nested_readable_name_list_literal():
    run_cell('lst = [0, [1, 2, 3]]')
    lst_1_1 = lookup_symbol(2)
    assert lst_1_1.readable_name == 'lst[1][1]', 'got %s when expected lst[1][1]' % lst_1_1.readable_name


def test_nested_readable_name_tuple_in_list():
    run_cell('lst = [0, (1, 2, 3)]')
    lst_1_1 = lookup_symbol(2)
    assert lst_1_1.readable_name == 'lst[1][1]', 'got %s when expected lst[1][1]' % lst_1_1.readable_name


def test_nested_readable_name_list_in_tuple():
    run_cell('lst = (0, [1, 2, 3])')
    lst_1_1 = lookup_symbol(2)
    assert lst_1_1.readable_name == 'lst[1][1]', 'got %s when expected lst[1][1]' % lst_1_1.readable_name
