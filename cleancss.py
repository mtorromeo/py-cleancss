# -*- coding: utf-8 -*-
"""
Documentattion here
"""
import re

version = '0.1'
__all__ = ['convert']

class ParserError(Exception):
	"""
	Raised on syntax errors.
	"""

	def __init__(self, lineno, message):
		self.lineno = lineno
		Exception.__init__(self, message)

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
		tail = selectorTree[-1][:]
		if len(selectorTree)>1:
			flattenedBase = self.flattenSelectors(selectorTree[:-1])
			for i, sel in enumerate(tail):
				if sel[0] == '&':
					sel = sel[1:]
				else:
					sel = ' '+sel
				tail[i] = flattenedBase.strip() + sel
		return ', '.join(tail)

	def toCss(self):
		level = 0
		ruleLevel = 0
		indenter = 0
		prevWasDefinition = False
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
				cur_rule_tree.append(match.group(1).split(','))
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
					selectors = self.flattenSelectors(cur_rule_tree)
					print cur_rule_tree, selectors
					rules.append((selectors, []))
					selectorsChanged = False
				if len(rule_prefixes)>0:
					prefixes = '-'.join(rule_prefixes) + '-'
				else:
					prefixes = ''
				rules[-1][1].append("{rule}: {definition};".format(rule=prefixes + match.group(1), definition=match.group(2)))
				continue

			raise ParserError(lineno, 'Unexpected item')
		
		return ''.join( [ "{selectors} {{\n\t{definitions}\n}}\n".format(selectors=selectors, definitions='\n\t'.join(definitions)) for selectors, definitions in rules ] )

def convert(sourcestream, context=None):
	"""Convert a CleanCSS file into a normal stylesheet."""
	return Parser(sourcestream).toCss()