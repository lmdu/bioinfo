#!/usr/bin/env python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bioinfo.settings")

import django
django.setup()

out = open('statistics.table', 'w')
num = 0

from macaca.models import *

#calculate individual SNP counts
for i in range(1, 21):
	model = Variants.shard(i).objects
	Snps.shard(1)

	for j in range(0, 21):
		filters = {}

		if j:
			filters['individual'] = j

		for feat in range(6):
			for gt in range(3):
				for mt in range(3):
					if feat:
						filters['snp__gannot__feature'] = feat

					if gt:
						filters['genotype'] = gt

					if mt:
						filters['snp__mutation__synonymous'] = mt

					if filters:
						count = model.filter(**filters).count()
					else:
						count = model.count()

					num += 1
					out.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(num, 1, feat, gt, mt, count, i, j))

#calculate non-redundant SNP counts
for i in range(1, 21):
	model = Snps.shard(i).objects
	filters = {}

	for feat in range(6):
		for mt in range(3):
			if feat:
				filters['gannot__feature'] = feat

			if mt:
				filters['mutation__synonymous'] = mt

			if filters:
				count = model.filter(**filters).count()
			else:
				count = model.count()

			num += 1
			out.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(num, 2, feat, 0, mt, count, i, 0))

#calculate specific SNP counts
filters = {}
for i in range(1, 21):
	Snps.shard(i)
	filters['chromosome'] = i
	for gid in range(4):
		for feat in range(6):
			for mt in range(3):
				if gid:
					filters['group'] = gid

				if feat:
					filters['snp__gannot__feature'] = feat

				if mt:
					filters['snp__mutation__synonymous'] = mt

				count = GroupSpecific.objects.filter(**filters).count()

				num += 1
				out.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(num, 3, feat, 0, mt, count, i, gid))


#calculate specific SNP counts
filters = {}
for i in range(1, 21):
	Snps.shard(i)
	filters['chromosome'] = i
	for sid in range(11):
		for feat in range(6):
			for mt in range(3):
				if sid:
					filters['species'] = sid

				if feat:
					filters['snp__gannot__feature'] = feat

				if mt:
					filters['snp__mutation__synonymous'] = mt

				count = SpeciesSpecific.objects.filter(**filters).count()

				num += 1
				out.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(num, 4, feat, 0, mt, count, i, sid))

