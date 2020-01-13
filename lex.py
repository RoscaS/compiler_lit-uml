"""
Latino Nathan
Rosca Sol
HE-ARC
janvier 2020

DESCRIPTION
"""

import ply.lex as lex

reserved_words = (
	# 'i',
	# 'b'
)

tokens = (
	'IDENTIFIER',
	'SEPARATOR',
	'ARROW',
	'STRING'
) + tuple(map(lambda s:s.upper(),reserved_words))

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
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

lex.lex()


if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
