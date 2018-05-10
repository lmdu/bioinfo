#!/usr/bin/env python
import sys
orthology_table, human_drug_file = sys.argv[1:]

idmapping = {}
with open(orthology_table) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		idmapping[cols[1]] = cols[0]

types = {'biotech': 1, 'small molecule': 2}
count = 0
with open(human_drug_file) as fh:
	for line in fh:
		cols = line.strip().split('\t')

		if cols[0] not in idmapping:
			continue

		count += 1
		print("%s\t%s\t%s\t%s\t%s\t%s" % (count, cols[1], cols[2], cols[3], types[cols[4]], idmapping[cols[0]]))

