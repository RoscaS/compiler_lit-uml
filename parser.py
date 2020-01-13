"""
Latino Nathan
Rosca Sol
HE-ARC
janvier 2020

DESCRIPTION
"""


import ply.yacc as yacc
import AST

from lex import tokens
# from lex import tokens

from tools.helpers import get_arg, init_folders

vars = {}

def p_program(p):
	'''program : classes SEPARATOR links'''
	p[0] = AST.ProgramNode([p[1]] + [p[3]])

# Links part
def p_links(p):
	'''links : statement
		| link links'''
	try:
		p[0] = AST.LinksNode([p[1]] + p[2].children)
	except:
		p[0]=p[1]

def p_links_end(p):
	'''links : link '''
	try:
		p[0] = AST.LinksNode([p[1]])
	except:
		p[0] = p[1]

def p_link(p):
	'''link : IDENTIFIER ARROW IDENTIFIER'''
	p[0] = AST.LinkNode(p[2], [AST.TokenNode(p[1]), AST.TokenNode(p[3])])


# classes part
def p_classes(p):
	'''classes : statement
		| object classes'''
	try:
		p[0] = AST.ClassesNode([p[1]] + p[2].children)
	except:
		p[0]=p[1]

def p_classes_end(p):
	'''classes : object'''
	try:
		p[0] = AST.ClassesNode([p[1]])
	except:
		p[0]=p[1]


def p_object(p):
	''' object : IDENTIFIER ',' attributs_bloc
		| '{' IDENTIFIER  info ',' attributs_blocs '}' '''
	p[0] = AST.ClassNode(p[2], [p[3]] + [p[5]])

def p_attributs_blocs(p):
	''' attributs_blocs : statement
			| '[' attributs_bloc ']' ',' attributs_blocs'''
	try:
		p[0] = AST.AttributsBlocsNode([p[2]] + p[5].children)
	except:
		p[0]=p[1]

def p_attributs_blocs_end(p):
	''' attributs_blocs : '[' attributs_bloc ']' '''
	p[0] = AST.AttributsBlocsNode(p[2])

def p_attributs_bloc(p):
	''' attributs_bloc : statement
				| attributs attributs_bloc'''
	try:
		p[0] = AST.AttributsBlocNode([p[1]] + p[2].children)
	except:
		p[0]=p[1]

def p_attributs_bloc_end(p):
	''' attributs_bloc :  attributs '''
	p[0] = AST.AttributsBlocNode(p[1])

def p_attributs(p):
	''' attributs : STRING ',' '''
	p[0] = AST.TokenNode(p[1])


def p_info(p):
	''' info : '(' STRING ')' '''
	p[0] = AST.TokenNode(p[2])

# Permet de sortir sans avoir des erreurs de valeur null
def p_statement(p):
	''' statement : '' '''

def p_error(p):
	print(f"Syntax error in line {p.lineno}")

def parse(program):
	return yacc.parse(program)

init_folders()
yacc.yacc(outputdir='generated')

if __name__ == "__main__":
	OUTPUT = "out/ast.jpg"

	prog = get_arg()
	ast = yacc.parse(prog)
	graph = ast.makegraphicaltree()
	graph.write_jpg(OUTPUT)
	print("wrote AST representation to", OUTPUT)
