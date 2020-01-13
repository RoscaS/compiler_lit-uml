"""
Latino Nathan
Rosca Sol
HE-ARC
janvier 2020

DESCRIPTION
Analyseur lexical, permet de tokenizer les chaînes de caractères
"""

import ply.lex as lex
from tools.helpers import get_arg

reserved_words = (
    # 'i',
    # 'b'
)

tokens = ('IDENTIFIER', 'SEPARATOR', 'ARROW', 'STRING')
tokens = tokens + tuple(map(lambda s: s.upper(), reserved_words))
literals = '(){}[],'

def t_STRING(t):
    r'".*"'
    return t

def t_SEPARATOR(t):
    r'[-]{3,}'
    return t

def t_ARROW(t):
    r'<--'
    return t

def t_IDENTIFIER(t):
    r'[A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore_tab = r'[ \t]'
t_ignore_comment = r'//.*\n'

def t_error(t):
    print(f"Illegal character '{repr(t.value[0])}'")
    t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
    prog = get_arg()
    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok:
            break
        print(f"line {tok.lineno}: {tok.type}({tok.value})")
