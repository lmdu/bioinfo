#!/usr/bin/env python
i = 0
with open('statistics.table') as fh:
	for line in fh:
		i += 1

		cols = line.strip().split()

		print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (i, cols[0], cols[1], cols[2], cols[5], cols[3], cols[4])
