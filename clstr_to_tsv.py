#!/usr/bin/python

import os
import re
from optparse import OptionParser

# Converts clstr file format to tab seperated value.
#
# Output columns are:
# Cluster	Identifier 1	Identifier 2	Percentage

class Cluster(object):
	def __init__(self):
		self.current_state = 'start'
		self.states = {
			'start': _parse_cluster,
			'cluster': _parse_cluster,
			'type1': _parse_type1,
			'type2': _parse_type2,
			'final': None
		}
		self.data = []

	def _parse_cluster(self, string):
		pass

	def _parse_type1(self, string):
		pass

	def _parse_type2(self, string):
		pass

	def read_file(self, file_name):
		pass

	def write_file(self, file_name):
		pass

	def write(self):
		pass

class ClusterData(object):
	def __init__(self):
		self.cluster_id = 0
		self.ident_1 = None
		self.ident_2 = None
		self.percentage = 0

def main():
	# Populate option parser.
	usage = "usage: %prog [options] infile"
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename", help="write data to file")

	# Parse arguments.
	(options, args) = parser.parse_args()

	# Expect only one argument: input filename.
	if len(args) != 1:
		parser.error("input filename is required")

	cluster = Cluster()

	cluster.read_file(args[0])

	if options['filename']:
		cluster.write_file(options['filename'])
	else:
		cluster.write()

if __name__ == '__main__':
	main()