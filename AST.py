# coding: latin-1

''' Petit module utilitaire pour la construction, la manipulation et la
repr�sentation d'arbres syntaxiques abstraits.

S�rement plein de bugs et autres surprises. � prendre comme un
"work in progress"...
Notamment, l'utilisation de pydot pour repr�senter un arbre syntaxique cousu
est une utilisation un peu "limite" de graphviz. �a marche, mais le layout n'est
pas toujours optimal...
'''

import pydot

class Node:
    count = 0
    type = 'Node (unspecified)'
    shape = 'ellipse'
    def __init__(self,children=None):
        self.ID = str(Node.count)
        Node.count+=1
        if not children: self.children = []
        elif hasattr(children,'__len__'):
            self.children = children
        else:
            self.children = [children]
        self.next = []

    def addNext(self,next):
        self.next.append(next)

    def asciitree(self, prefix=''):
        result = "%s%s\n" % (prefix, repr(self))
        prefix += '|  '
        for c in self.children:
            if not isinstance(c,Node):
                result += "%s*** Error: Child of type %r: %r\n" % (prefix,type(c),c)
                continue
            result += c.asciitree(prefix)
        return result

    def __str__(self):
        return self.asciitree()

    def __repr__(self):
        return self.type

    def makegraphicaltree(self, dot=None, edgeLabels=True):
            if not dot: dot = pydot.Dot()
            dot.add_node(pydot.Node(self.ID,label=repr(self), shape=self.shape))
            label = edgeLabels and len(self.children)-1
            for i, c in enumerate(self.children):
                c.makegraphicaltree(dot, edgeLabels)
                edge = pydot.Edge(self.ID,c.ID)
                if label:
                    edge.set_label(str(i))
                dot.add_edge(edge)
                #Workaround for a bug in pydot 1.0.2 on Windows:
                #dot.set_graphviz_executables({'dot': r'C:\Program Files\Graphviz2.38\bin\dot.exe'})
            return dot

    def threadTree(self, graph, seen = None, col=0):
            colors = ('red', 'green', 'blue', 'yellow', 'magenta', 'cyan')
            if not seen: seen = []
            if self in seen: return
            seen.append(self)
            new = not graph.get_node(self.ID)
            if new:
                graphnode = pydot.Node(self.ID,label=repr(self), shape=self.shape)
                graphnode.set_style('dotted')
                graph.add_node(graphnode)
            label = len(self.next)-1
            for i,c in enumerate(self.next):
                if not c: return
                col = (col + 1) % len(colors)
                col=0 # FRT pour tout afficher en rouge
                color = colors[col]
                c.threadTree(graph, seen, col)
                edge = pydot.Edge(self.ID,c.ID)
                edge.set_color(color)
                edge.set_arrowsize('.5')
                # Les arr�tes correspondant aux coutures ne sont pas prises en compte
                # pour le layout du graphe. Ceci permet de garder l'arbre dans sa repr�sentation
                # "standard", mais peut provoquer des surprises pour le trajet parfois un peu
                # tarabiscot� des coutures...
                # En commantant cette ligne, le layout sera bien meilleur, mais l'arbre nettement
                # moins reconnaissable.
                edge.set_constraint('false')
                if label:
                    edge.set_taillabel(str(i))
                    edge.set_labelfontcolor(color)
                graph.add_edge(edge)
            return graph

class ProgramNode(Node):
    type = 'Program'

class LinksNode(Node):
    type = 'Links'

class ClassesNode(Node):
    type = 'Classes'

class AttributsBlocNode(Node):
    type = 'AttributsBloc'

class AttributsNode(Node):
    type = 'Attributs'

class AttributNode(Node):
    type = 'Attribut'

class AttributsBlocsNode(Node):
    type = 'AttributsBlocs'

class StatementNode(Node):
    """
    extends Node and represent a statement in the tree
    """
    type = "Statement"

class ObjectNode(Node):
    """
    extends Node and represent a statement in the tree
    """
    type = "Object"

class ClassNode(Node):
    type = "Class"
    def __init__(self, name, children=None):
        """
        redefinition of __init__ with an operator
        :param op: arithmetic operation
        :param children: on what is done the operation
        """
        Node.__init__(self, children)
        self.name = name


    def __repr__(self):
        """
        representation of the node
        :return: the string of the operation
        """
        return f"{self.name}"


class AttributsNode(Node):
    type = "Attribut"
    def __init__(self, name, children=None):
        """
        redefinition of __init__ with an operator
        :param op: arithmetic operation
        :param children: on what is done the operation
        """
        Node.__init__(self, children)
        self.name = name


    def __repr__(self):
        """
        representation of the node
        :return: the string of the operation
        """
        return f"{self.name}"

class TokenNode(Node):
    """
    extends Node and represent a token in the tree
    """
    type = 'token'

    def __init__(self, tok, children=None):
        """
        redefinition of __init__
        store token in a variable
        :param tok: token to store
        :param children: children of the node
        """
        Node.__init__(self, children)
        self.tok = tok.replace('"', '')

    def __repr__(self):
        """
        representation of the node
        :return: the token of the node
        """
        return repr(self.tok)

class LinkNode(Node):
    type = '<--'

    def __init__(self, assign, children):
        """
        redefinition of __init__ with an operator
        :param op: arithmetic operation
        :param children: on what is done the operation
        """
        Node.__init__(self, children)
        self.assign = assign

    def __repr__(self):
        """
        representation of the node
        :return: the string of the operation
        """
        return f"{self.assign}"

def addToClass(cls):
    ''' D�corateur permettant d'ajouter la fonction d�cor�e en tant que m�thode
    � une classe.

    Permet d'impl�menter une forme �l�mentaire de programmation orient�e
    aspects en regroupant les m�thodes de diff�rentes classes impl�mentant
    une m�me fonctionnalit� en un seul endroit.

    Attention, apr�s utilisation de ce d�corateur, la fonction d�cor�e reste dans
    le namespace courant. Si cela d�range, on peut utiliser del pour la d�truire.
    Je ne sais pas s'il existe un moyen d'�viter ce ph�nom�ne.
    '''
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

