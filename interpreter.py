"""
Latino Nathan
Rosca Sol
HE-ARC
janvier 2020

DESCRIPTION
Module qui permet de récupérer les information de l'arbre.
Interprète les noeuds et les envoie dans le svgcreator
"""

import AST
from AST import addToClass

from tools.helpers import get_arg, OUT_FOLDER, get_program_name
from tools.svgcreator import SVG

creator = SVG()
vars = {}

def get_children(children):
    return [c.compile() for c in children]

def join_children(children, c=""):
    return f"{c}".join(f"{i}" for i in get_children(children) if i is not None)

@addToClass(AST.ProgramNode)
def compile(self):
    """ ProgramNode read each children and concatenate the output"""
    return join_children(self.children)

@addToClass(AST.TokenNode)
def compile(self):
    """ TokenNode """
    if self.tok in vars:
        return vars[self.tok]
    if len(self.children) > 0:
        return f"{self.tok} {self.children[0].compile()}"
    return self.tok

@addToClass(AST.ClassesNode)
def compile(self):
    """ ClassesNode """
    return join_children(self.children)

@addToClass(AST.ClassNode)
def compile(self):
    """ ClassNode """
    creator.add_class(self.name, self.children[0].compile())
    output = [i for i in get_children(self.children[1:]) if i is not None]
    for i in output:
        creator.add_attributs(self.name, i)

    return "".join(output)

@addToClass(AST.LinksNode)
def compile(self):
    """ LinksNode """
    replace = lambda c, idx: c.children[idx].tok.replace("'", "")
    output = ""

    for c in self.children:
        out = c.compile()
        if out is not None:
            creator.add_link(replace(c, 0), c.assign, replace(c, 1))
            output += out

    return output

@addToClass(AST.LinkNode)
def compile(self):
    """ LinkNode """
    return join_children(self.children)

@addToClass(AST.AttributsBlocNode)
def compile(self):
    """ AttributsBlocNode """
    return join_children(self.children, "/")

@addToClass(AST.AttributsBlocsNode)
def compile(self):
    """ AttributsBlocsNode """
    return join_children(self.children, "|")

if __name__ == '__main__':
    from parser import parse

    prog = get_arg()
    ast = parse(prog)
    compiled = ast.compile()
    program_name = get_program_name()
    destination = f"{OUT_FOLDER}/{program_name}.svg"
    with open(destination, 'w') as file:
        file.write(creator.__str__())
    print(f"Output wrote in {destination}")
