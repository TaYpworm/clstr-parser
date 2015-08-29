import re

# Converts clstr file format to tab seperated value.
#
# Output columns are:
# Cluster	Identifier 1	Identifier 2	Percentage

class ClusterParser(object):
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
		print 'Error parsing file: {0}'.format(self.error_msg)

	def _parse_cluster_id(self):
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
		retval = 'type2'

		string = self.file.readline()

		if string == '':
			self.error_msg = 'pattern type 1 could not be matched because of unexpected eof'
			retval = 'error'
		else:
			m = self.type1_pat.match(string)
			self.current_ident1 = m.group(1)

		return retval

	def _parse_type2(self):
		retval = 'type2'

		start = self.file.tell()
		string = self.file.readline()

		if string =='':
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
			else:
				self.file.seek(start)
				retval = 'cluster'

		return retval

	def read_file(self, file_name):
		self.data = []
		self.current_cluster = None
		self.current_state = 'start'

		self.file = open(file_name)

		while self.current_state != 'final' and self.current_state != 'error':
			self.current_state = self.states[self.current_state]()

		if self.current_state == 'error':
			self.states[self.current_state]()

		self.file.close()

	# Write TSV to file.
	def write_tsv_file(self, file_name):
		if self.error_msg:
			print 'Cannot write file because an error was encountered during parsing.'
		else:
			with open(file_name, 'w') as f:
				if len(self.data) > 0:
					f.write('{0}\n'.format(self.data[0].get_header_tsv()))
					for cluster in self.data:
						f.write('{0}\n'.format(cluster))

	# Write TSV to stdout
	def write_tsv(self):
		if self.error_msg:
			print 'Cannot write file because an error was encountered during parsing.'
		else:
			if len(self.data) > 0:
				print self.data[0].get_header_tsv()
				for cluster in self.data:
					print cluster


class ClusterData(object):
	def __init__(self):
		self.cluster_id = 0
		self.ident1 = None
		self.ident2 = None
		self.percentage = 0

	def __str__(self):
		return '{0}\t{1}\t{2}\t{3}'.format(
			self.cluster_id, 
			self.ident1, 
			self.ident2, 
			self.percentage)

	def get_header(self):
		return ['Cluster', 'Identifier 1', 'Identifier 2', 'Percentage']

	def get_header_tsv(self):
		return 'Cluster\tIdentifier 1\tIdentifier 2\tPercentage'