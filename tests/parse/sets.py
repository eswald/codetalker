#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import STRING, ID, NUMBER, WHITE, NEWLINE
from codetalker.pgm.special import star, plus
from codetalker.pgm.grammar import ParseError

def start(rule):
    rule | star({"a", value})

def value(rule):
    rule | ("b", {"c", ("d", "e")}, "f")
    rule | {star("g"), "h"}

grammar = pgm.Grammar(start=start, tokens=[ID], ignore=[WHITE, NEWLINE])

def test_one():
    text = 'a b c f g g h b d e f a'
    tree = grammar.process(text)
    assert str(tree) == text

if __name__ == '__main__':
    for name, fn in globals().items():
        if name.startswith('test_'):
            fn()
            print 'test passed'
    print 'Finished!'

# vim: et sw=4 sts=4
