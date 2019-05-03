#!/usr/bin/env python

from codetalker.pgm import Grammar
from codetalker.pgm.errors import ParseError
from codetalker.pgm.tokens import ID, WHITE
from codetalker.pgm.special import _or, plus

def start(rule):
    rule | plus(value)

def value(rule):
    rule | ("A", _or(("B", "C"), ("B", "D"), ("E")))

g = Grammar(start=start, ast_tokens=[ID], tokens=[ID, WHITE], ignore=[WHITE])

def test_one():
    tree = g.get_ast('A B C A B D A E')
    assert map(len, tree) == [3, 3, 2]

def test_two():
    tree = g.get_ast('A B D')
    assert map(len, tree) == [3]

def test_onother():
    try:
        tree = g.get_ast('A B B D')
    except ParseError:
        pass
    else:
        raise AssertionError('was supposed to fail')


# vim: et sw=4 sts=4
