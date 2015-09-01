#!/usr/bin/python

import re
import sys

def main(args):
	"""
	Counts the number of 'type 2' patterns in the input file.

	See clstr_parser for a description of 'type 2'.
	"""
	if len(args) != 2:
		raise ArgumentError("File name is missing.")

	type2_pat = re.compile('^\d+\s+\d+nt,\s+>(\w+)...\s+at\s+([+-])/(\d+.\d+)')
	num_type2 = 0

	with open(args[1]) as f:
		for line in f:
			if type2_pat.match(line):
				num_type2 += 1

	print 'Number: {0}'.format(num_type2)

def ArgumentError(Exception):
	pass

if __name__ == '__main__':
	main(sys.argv)