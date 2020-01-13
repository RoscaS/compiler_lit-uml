"""
Latino Nathan
Rosca Sol
HE-ARC
janvier 2020

DESCRIPTION
"""

import AST
from AST import addToClass

from tools.helpers import get_arg, OUT_FOLDER, get_program_name
from tools.svgcreator import SVG

creator = SVG()
vars = {}

def children(children):
    return [c.compile() for c in children]


@addToClass(AST.ProgramNode)
def compile(self):
    """
    ProgramNode
    read each children and concatenate the output"""
    # output = ''
    # for c in self.children:
    #     out = c.compile()
    #
    #     if out is not None:
    #         output += out
    # return output

    return "".join(i for i in children(self.children) if i is not None)


@addToClass(AST.TokenNode)
def compile(self):
    """
    TokenNode
    """
    if self.tok in vars:
        return vars[self.tok]
    if len(self.children) > 0:
        return f"{self.tok} {self.children[0].compile()}"
    return self.tok

@addToClass(AST.ClassesNode)
def compile(self):
    """
    ClassesNode
    """
    # output = ""
    # for c in self.children:
    #     out = c.compile()
    #     if out is not None:
    #         output += out
    # return output
    return "".join(i for i in children(self.children) if i is not None)


# DOUBLON ???
@addToClass(AST.ClassNode)
def compile(self):
    """
    ClassNode
    """
    creator.add_class(self.name, self.children[0].compile())
    # output = ""
    # for c in self.children[1:]:
    #     out = c.compile()
    #     if out is not None:
    #         creator.add_attributs(self.name, out)
    #         output += out
    # return output
    output = [i for i in children(self.children[1:]) if i is not None]
    for i in output:
        creator.add_attributs(self.name, i)

    return "".join(output)


@addToClass(AST.LinksNode)
def compile(self):
    """
    LinksNode
    """
    replace = lambda c, idx: c.children[idx].tok.replace("'", "")
    link = lambda c: creator.add_link(replace(c, 0), c.assign, replace(c, 1))

    # output = ""
    # for c in self.children:
    #     out = c.compile()
    #     if out is not None:
    #         # _class1 = replace(c, 0)
    #         # _class2 = replace(c, 1)
    #         # creator.add_link(replace(c, 0), c.assign, replace(c, 1))
    #         link(c)
    #         output += out
    # return output

    # output = ["yes"]
    output = [i for i in children(self.children[1:]) if i is not None]
    for i in output:
        link(i)

    return "".join(output)

@addToClass(AST.LinkNode)
def compile(self):
    """
    LinkNode
    """
    # output = ""
    # for c in self.children:
    #     out = c.compile()
    #     if out is not None:
    #         output += out
    # return output

    return "".join(i for i in children(self.children) if i is not None)





@addToClass(AST.AttributsBlocNode)
def compile(self):
    """
    AttributsBlocNode
    """
    # output = ""
    # for c in self.children:
    #     out = c.compile()
    #     if out is not None:
    #         output += f"{out},"
    return "".join(f"{i}," for i in children(self.children) if i is not None)


@addToClass(AST.AttributsBlocsNode)
def compile(self):
    """
    AttributsBlocsNode
    """
    output = ""
    for c in self.children:
        out = c.compile()
        if out is not None:
            output += f"{out}-"
    return output


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
