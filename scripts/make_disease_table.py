#!/usr/bin/env python
import sys
orthology_table, human_omim_file = sys.argv[1:]

idmapping = {}
with open(orthology_table) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		idmapping[cols[1]] = cols[0]

count = 0
with open(human_omim_file) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')

		if cols[0] not in idmapping:
			continue

		count += 1

		print("%s\t%s\t%s\t%s\t%s\t%s\t%s" % (count, cols[1], cols[2], cols[3], cols[4], cols[5], idmapping[cols[0]]))
		