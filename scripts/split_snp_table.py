import os
import sys

snp_file = sys.argv[1]

outs = [None]
for i in range(1,21):
	op = open("%s.%s" % (snp_file, i), 'w')
	outs.append(op)

with open(snp_file) as fh:
	for line in fh:
		cols = line.strip().split()
		idx = int(cols[-1])
		outs[idx].write(line)

for op in outs[1:]:
	op.close()
