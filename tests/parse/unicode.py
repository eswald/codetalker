#!/usr/bin/env python

from codetalker import pgm
from codetalker.pgm.tokens import ID, WHITE, NEWLINE, StringToken
from codetalker.pgm.special import star, plus, _or
from codetalker.pgm.grammar import ParseError

class DASH(StringToken):
    # Unicode symbols used in modal spells.
    strings = [
        u"\u2014".encode('utf8'),
        u"\u2022".encode('utf8'),
    ]
    
    def __str__(self):
        return repr(self.value).strip("'u")

def start(rule):
    rule | plus(value)

def value(rule):
    rule | ID | DASH
    rule.pass_single = True

grammar = pgm.Grammar(start=start, tokens=[ID, DASH, WHITE, NEWLINE], ignore=[WHITE, NEWLINE], ast_tokens=[ID, DASH])

t = pgm.Translator(grammar)

@t.translates(ID)
def start_handler(node):
    return node.value

@t.translates(DASH)
def start_handler(node):
    return node.value

@t.translates(list)
def start_handler(node):
    return [t.translate(item) for item in node]

def test_parsing():
    text = u'Before \u2014 Between \u2022 After'
    tree = grammar.process(text.encode('utf8'))
    assert str(tree) == repr(text).strip("'u")

def test_translation():
    text = u'Before \u2014 Between \u2022 After'
    result = t.from_string(text.encode('utf8'))
    assert result == text.split()

if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
            print('test passed')
    print('Finished!')

# vim: et sw=4 sts=4
