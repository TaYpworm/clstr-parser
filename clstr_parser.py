import re

class ClusterParser(object):
	"""
	Parses clstr file format for converstion to a tab separated file specified by UNR 
	Bioinformatics.  The parser pulls out clusters with percentages. There may be 
	multiple lines that list a percentage for each cluster.

	The desired output columns are:
	Cluster	Identifier 1	Identifier 2	Percentage

	Example:

	>Cluster 4
	0       13038nt, >iceplant_tr_11521... *
	1       637nt, >MCGI0001S00008421... at +/99.69%

	The desired output of this example is:
	'4\ticeplant_tr_11521\tMCGI0001S00008421\t0.9969'

	The parsed data is not generally usable because it ignores important clstr fields,
	and is designed to structure output data in a bizarre way.

	No clstr documentation was referenced in the creation of this parser.  Nomenclature
	is likely wrong.

	"""

	def __init__(self):
		# Regex patterns
		self.cluster_pat = re.compile('^>Cluster\s+(\d+)')
		self.type1_pat = re.compile('^0\s+\d+nt,\s+>(\w+)...')
		self.type2_pat = re.compile('^\d+\s+\d+nt,\s+>(\w+)...\s+at\s+([+-])/(\d+.\d+)')
		
		# Fields
		self.data = None
		self.current_cluster_id = None
		self.current_ident1 = None
		self.file = None
		self.error_msg = None

		# Simple state machine that transitions by setting self.current_state.
		# States
		self.current_state = 'start'
		self.states = {
			'start': self._parse_cluster_id,
			'cluster': self._parse_cluster_id,
			'type1': self._parse_type1,
			'type2': self._parse_type2,
			'error': self._error,
			'final': None
		}

	def _error(self):
		"""
		Formats an error string.
		"""
		print 'Error parsing file: {0}'.format(self.error_msg)

	def _parse_cluster_id(self):
		"""
		Parses the cluster ID from the clstr file.  'Cluster ID' may not be the correct term
		for this field, but is the term used by UNR Bioinformatics.

		IDs are of the following pattern:

		>Cluster 1

		Cluster IDs should be followed by a list of clusters and their data.

		It may not be a parsing failure if the Cluster ID fails to parse.
		"""
		retval = 'type1'

		string = self.file.readline()

		# Terminate successfully if at end of file.
		if string == '':
			retval = 'final'
		else:
			m = self.cluster_pat.match(string)
			self.current_cluster_id = int(m.group(1))

		return retval

	def _parse_type1(self):
		"""
		The following is an example of the Type 1 pattern:

		0	200nt, >iceplant_tr_178020... *

		UNR Bioinformatics requested the parsing of the 'iceplant_tr_178020' string as 
		Identifier 1.  All other fields are ignored.

		If an error occurs during the matching of a type 1 pattern the parsing is a failure.
		A Type 1 pattern must exist for each Cluster ID.
		"""
		retval = 'type2'	# Transition to Type 2 by default.

		string = self.file.readline()

		if string == '':
			self.error_msg = 'pattern type 1 could not be matched because of unexpected eof'
			retval = 'error'
		else:
			m = self.type1_pat.match(string)
			self.current_ident1 = m.group(1)

		return retval

	def _parse_type2(self):
		"""
		The following is an example of a Type 2 pattern:

		1       668nt, >MCGI0001S00004076... at -/100.00%

		UNR Bioinformatics requested the parsing of the 'MCGI0001S00004076' string as
		Identifier 2, and '-/100.00%' as the Percentage.  Percentage is converted to a
		float.

		Multiple type 2 patterns may exist per Cluster ID.

		An error parsing a Type 2 pattern does not imply failure.  Type 2 is optional.
		"""
		retval = 'type2'

		# Record the current position in the file.  This position will need to be reset
		# if a Type 2 pattern is not found.
		start = self.file.tell()
		string = self.file.readline()

		if string =='':
			# Reached the end of the file.
			# This is not a failure because Type 2 is optional
			retval = 'final'
		else:
			m = self.type2_pat.match(string)

			if m:
				cd = ClusterData()
				cd.cluster_id = self.current_cluster_id
				cd.ident1 = self.current_ident1
				cd.ident2 = m.group(1)
				cd.percentage = float(m.group(3)) / 100.0
				if m.group(2) == '-':
					cd.percentage *= -1
				self.data.append(cd)
				# Stay in self.current_state 'type2' because another Type 2 record may
				# follow
			else:
				# If a Type 2 pattern is not found, rewind to the start position in the
				# file, and transition to finding a Cluster ID.
				self.file.seek(start)
				retval = 'cluster'

		return retval

	def read_file(self, file_name):
		"""
		Read a clstr file.
		"""
		self.data = []
		self.current_cluster = None
		self.current_state = 'start'

		self.file = open(file_name)

		while self.current_state != 'final' and self.current_state != 'error':
			self.current_state = self.states[self.current_state]()

		if self.current_state == 'error':
			self.states[self.current_state]()

		self.file.close()

def write_tsv_file(cluster_parser, file_name):
	"""
	Write the data in a ClusterParser to tab separated file.
	"""
	if cluster_parser is None:
		raise ArgumentError('Cluster parser cannot be None.')

	if cluster_parser.error_msg:
		print 'Cannot write file because an error was encountered during parsing.'
	else:
		with open(file_name, 'w') as f:
			if len(cluster_parser.data) > 0:
				f.write('{0}\n'.format(cluster_data_header_to_tsv(cluster_parser.data[0])))
				for cluster in cluster_parser.data:
					f.write('{0}\n'.format(cluster))

def write_tsv(cluster_parser):
	"""
	Write the data in a ClusterParser to stdout as a tab separated string.
	"""
	if cluster_parser is None:
		raise ArgumentError('Cluster parser cannot be None.')

	if cluster_parser.error_msg:
		print 'Cannot write file because an error was encountered during parsing.'
	else:
		if len(cluster_parser.data) > 0:
			print cluster_data_header_to_tsv(cluster_parser.data[0])
			for cluster in cluster_parser.data:
				print cluster

class ClusterData(object):
	"""
	Data structure to hold clstr data.
	"""
	def __init__(self):
		# Fields
		self.cluster_id = 0
		self.ident1 = None
		self.ident2 = None
		self.percentage = 0

	def __str__(self):
		"""
		Return fields as a tab separated string.
		"""
		return '{0}\t{1}\t{2}\t{3}'.format(
			self.cluster_id, 
			self.ident1, 
			self.ident2, 
			self.percentage)

	def get_header(self):
		"""
		Return a list of column headers.
		"""
		return ['Cluster', 'Identifier 1', 'Identifier 2', 'Percentage']

def cluster_data_header_to_tsv(cluster_data):
	"""
	Convert ClusterData header into a tab separated string.
	"""
	return '\t'.join(cluster_data.get_header())

class ArgumentError(Exception):
	pass