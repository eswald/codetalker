#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import ANY, ID, NUMBER, STRING, WHITE
from codetalker.pgm.special import lookahead, notahead
from codetalker.pgm.grammar import ParseError

def sentence(rule):
    rule | (subjects, "verb", objects, ["and", subjects, "verb", objects], ".")

def subjects(rule):
    rule | ("noun", ["and", "noun"], lookahead("verb"))

def objects(rule):
    rule | ("noun", ["and", "noun", notahead("verb")])

grammar = pgm.Grammar(start=sentence, tokens=[ID, WHITE, ANY], ignore=[WHITE])

def test_one():
    text = 'noun verb noun.'
    tree = grammar.process(text)
    assert str(tree) == text

def test_two():
    text = 'noun and noun verb noun.'
    tree = grammar.process(text)
    assert str(tree) == text

def test_three():
    text = 'noun verb noun and noun.'
    tree = grammar.process(text)
    assert str(tree) == text

def test_four():
    text = 'noun verb noun and noun verb noun.'
    tree = grammar.process(text)
    assert str(tree) == text

if __name__ == '__main__':
    for name, fn in globals().items():
        if name.startswith('test_'):
            fn()
            print 'test passed'
    print 'Finished!'

# vim: et sw=4 sts=4
