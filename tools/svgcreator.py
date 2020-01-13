"""
Latino Nathan
Rosca Sol
HE-ARC
janvier 2020

DESCRIPTION

Class qui permet la création de balise svg
Il récupère les liens et les classes à afficher
"""


class SVG:
	def __init__(self):
		self.classes = []
		self.links = []
		self.id = 0

	def add_class(self, name, info):
		self.classes.append(Class(name, info, self.id))
		self.id += 1

	def __str__(self):
		w = 100
		h = 200
		s = 50
		font_size = 10
		i = 0
		j = 0
		globalw = len(self.classes) * w + s * len(self.classes)
		output = f'<?xml version="1.0" standalone="no"?>\n<svg width="{globalw}" height="400" version="1.1" xmlns="http://www.w3.org/2000/svg">\n'
		for _class in self.classes:
			output += self.print_class(w * i + s * i, h * j + s * j, w, h, font_size, _class)
			i += 1

		for link in self.links:
			id1 = self.find_id(link.class1)
			id2 = self.find_id(link.class2)
			output += self.print_link(w * id1 + s * id1 + w / 2, h * j + s * j + h, w * id2 + s * id2 + w / 2, h * j + s * j + h, ((id2+id1)*10))
		output += '</svg>'
		return output

	def print_class(self, x, y, w, h, size, _class):
		_info = _class.info.replace('<', '&lt;').replace('>', '&gt;')
		output = '<g>\n'
		output += f'\t<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="grey" style="stroke:rgb(0,0,0);stroke-width:1"/>\n'
		output += f'\t<text x="{x + w / 2}" y="{y + size}" text-anchor="middle" font-family="Verdana" font-size="{size}" fill="black">{ _class.name}</text>\n'
		output += f'\t<text x="{x + w / 2}" y="{y + 2 * size}" text-anchor="middle" font-family="Verdana" font-size="{size}" fill="black">{_info}</text>\n'
		output += self.print_attributs(x, y, w,  size,_class)
		output += '</g>\n'
		return output

	def print_attributs(self, x, y, w, size,_class):
		output = ""
		i = 3
		for blocs in _class.attributs_bloc.split("|"):
			output += f'\t<line x1="{x}" y1="{y + i * size}" x2="{x + w}" y2="{y +  i * size}" style="stroke:rgb(0,0,0);stroke-width:1" />\n'
			i+= 1
			for attribut in blocs.split("/"):
				output += f'\t<text x="{x+5}" y="{y + size * i}"  font-family="Verdana" font-size="{size}" fill="black">{attribut}</text>\n'
				i+=1
		return output

	def print_link(self, x1, y1, x2, y2, h):
		output = f'<polyline points = "{x1},{y1} {x1},{y1+h} {x2},{y1+h} {x2},{y2}" style = "fill:none;stroke:black;stroke-width:1"/>\n'
		output += f'<polyline points = "{x1-10},{y1+10} {x1},{y1} {x1+10},{y1+10}" style = "fill:none;stroke:black;stroke-width:1"/>\n'
		return output

	def add_link(self, class1, assign, class2):
		self.links.append(Link(class1,assign, class2))

	def find_id(self, name):
		for _class in self.classes:
			if _class.name == name:
				return _class.id
		return -1

	def add_attributs(self,_class, attribut):
		self.classes[self.find_id(_class)].attributs_bloc = attribut

class Class:
	def __init__(self, name, info, id):
		self.info = info
		self.name = name
		self.attributs_bloc = ""
		self.id = id


class Link:
	def __init__(self, class1, relation, class2):
		self.class1 = class1
		self.relation = relation
		self.class2 = class2
