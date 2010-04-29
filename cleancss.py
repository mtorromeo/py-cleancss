# -*- coding: utf-8 -*-
"""
CleanCSS is a simple pythonic language for CSS inspired by
`CleverCSS <http://sandbox.pocoo.org/clevercss/>`_ but simpler and with less
obstrusive features.

Library usage
-------------
Import the cleancss module and call the convert() function with a file-like object.

Example::

	import cleancss
	with open('file.css') as f:
		print cleancss.convert(f)
"""
import sys, re

version = '1.3'
__all__ = ['convert']

class ParserError(Exception):
	"""
	Raised on syntax errors.
	"""

	def __init__(self, lineno, message):
		self.lineno = lineno
		Exception.__init__(self)
		self.message = message

	def __str__(self):
		return '%s (line %s)' % (
			self.message,
			self.lineno
		)

class Parser(object):
	_r_indentation = re.compile(r'^\s*')
	_r_selector = re.compile(r'^(.+)\s*:$')
	_r_property_prefix = re.compile(r'^([^:>\s]+)->$')
	_r_definition = re.compile(r'^([^\s]+)\s*:\s*(.+)$')

	def __init__(self, sourcestream):
		self.sourcestream = sourcestream

	def flattenSelectors(self, selectorTree):
		selectors = []
		base = selectorTree[0][:]
		tails = None
		if len(selectorTree)>1:
			tails = self.flattenSelectors(selectorTree[1:])
		for i, sel in enumerate(base):
			if tails is not None:
				for tail in tails:
					if tail[0] == '&':
						tail = tail[1:]
					else:
						tail = ' '+tail
					selectors.append( base[i] + tail )
			else:
				selectors.append( base[i] )
		return selectors

	def toCss(self):
		level = 0
		indenter = 0
		selectorsChanged = False
		rules = []
		cur_rule_tree = []
		rule_prefixes = []

		lineno = 0
		for line in self.sourcestream:
			lineno += 1

			if line.strip() == "":
				continue

			indentation = self._r_indentation.match(line).group(0)
			if indenter == 0 and len(indentation)>0:
				indenter = len(indentation)

			if indenter>0 and len(indentation) % indenter != 0:
				raise ParserError(lineno, 'Indentation error')

			newlevel = len(indentation) / indenter if indenter > 0  else 0
			line = line.strip()

			if newlevel-level>1:
				raise ParserError(lineno, 'Indentation error')

			# Pop to new level
			while len(cur_rule_tree)+len(rule_prefixes)>newlevel and len(rule_prefixes)>0:
				rule_prefixes.pop()
			while len(cur_rule_tree)>newlevel:
				cur_rule_tree.pop()
			level = newlevel

			match = self._r_selector.match(line)
			if match:
				selectors = match.group(1).split(',')
				for i, sel in enumerate(selectors):
					selectors[i] = sel.strip()
				cur_rule_tree.append(selectors)
				selectorsChanged = True
				continue

			match = self._r_property_prefix.match(line)
			if match:
				rule_prefixes.append(match.group(1))
				continue

			match = self._r_definition.match(line)
			if match:
				if len(cur_rule_tree) == 0:
					raise ParserError(lineno, 'Selector expected, found definition')
				if selectorsChanged:
					selectors = ',\n'.join( self.flattenSelectors(cur_rule_tree) )
					rules.append((selectors, []))
					selectorsChanged = False
				if len(rule_prefixes)>0:
					prefixes = '-'.join(rule_prefixes) + '-'
				else:
					prefixes = ''
				rules[-1][1].append("%s: %s;" % (prefixes + match.group(1), match.group(2)))
				continue

			raise ParserError(lineno, 'Unexpected item')

		return ''.join( [ "%s {\n\t%s\n}\n" % (selectors, '\n\t'.join(definitions)) for selectors, definitions in rules ] )

def convert(sourcestream):
	"""Convert a CleanCSS file into a normal stylesheet."""
	return Parser(sourcestream).toCss()

def main():
	if len(sys.argv) <= 1:
		print """Usage: %s <file 1> [ <file 2> ... <file n>]

Version %s
(c) 2010 Massimiliano Torromeo""" % (sys.argv[0], version)
	else:
		for filename in sys.argv[1:]:
			try:
				with open(filename) as f:
					print convert(f)
			except (IOError, ParserError) as e:
				sys.exit(e)

if __name__ == '__main__':
	main()
