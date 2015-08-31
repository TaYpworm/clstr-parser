#!/usr/bin/python

import os
from clstr_parser import ClusterParser, write_tsv, write_tsv_file
from optparse import OptionParser

def main():
	# Populate option parser.
	usage = "usage: %prog [options] infile"
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename", help="write data to file")

	# Parse arguments.
	options, args = parser.parse_args()

	# Expect only one argument: input filename.
	if len(args) != 1:
		parser.error("input filename is required")

	parser = ClusterParser()

	parser.read_file(args[0])

	if options.filename:
		write_tsv_file(parser, options.filename)
	else:
		write_tsv(parser)

if __name__ == '__main__':
	main()