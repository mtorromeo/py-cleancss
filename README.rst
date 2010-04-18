CleanCSS
--------

CleanCSS is a simple pythonic language for CSS inspired by
`CleverCSS <http://sandbox.pocoo.org/clevercss/>`_ but simpler and with less
obstrusive features.

Why
---
I really liked the idea behind CleverCSS but when used in production I realized
that I was trying to get away from its parser by escaping strings and unsupported
CSS properties way too often. Using vendor prefixes like -webkit-gradient and
values such as rgba resulted in a messy CSS, so I decided to write my own parser
for a similar syntax without all the complex features that I did not use anyway
and it now works fine for me in REAL modern websites.

Syntax examples
---------------

I'm going to keep the CleverCSS examples where possible since the syntax is really
similar.

A small example below.  Note the indentation based syntax and how you can nest rules::

	#header, #footer:
		margin: 0
		padding: 0
		font->
			family: Verdana, sans-serif
			size: .9em

		li:
			padding: 0.4em
			margin: 0.8em 0 0.8em

			h3:
				font-size: 1.2em
			p:
				padding: 0.3em
			p.meta:
				text-align: right
				color: #ddd

Of course you can do the very same in CSS, but because of its flat nature the
code would look more verbose.  The following piece of code is the CleanCSS
output of the above file::

	#header, #footer {
		margin: 0;
		padding: 0;
		font-family: Verdana, sans-serif
		font-size: .9em
	}

	#header li,
	#footer li {
		padding: 0.4em;
		margin: 0.8em 0 0.8em;
	}

	#header li h3,
	#footer li h3 {
		font-size: 1.2em;
	}

	#header li p,
	#footer li p {
		padding: 0.3em;
	}

	#header li p.meta,
	#footer li p.meta {
		text-align: right;
		color: #dddddd;
	}

Library usage
-------------
Import the cleancss module and call the convert() function with a file-like object.

Example::

	import cleancss
	with open('file.css') as f:
		print cleancss.convert(f)

Command line usage
------------------
Call the cleancss.py without parameters to show the usage instructions.
Pass any number of files to cleancss.py and the script will convert the files to CSS
and print the result to the console.

Example::

	cleancss.py file.css > result.css

LICENSE
-------
Copyright (c) 2010 Massimiliano Torromeo

CleanCSS is free software released under the terms of the BSD license.

See the LICENSE file provided with the source distribution for full details.

Contacts
--------

* Massimiliano Torromeo <massimiliano.torromeo@gmail.com>
