#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bioinfo.settings")
import django
if django.VERSION >= (1, 7):
	django.setup()

from macaca.models import Variant

for i in range(1, 21):
	for j in range(1, 21):
		sys.stderr.write("variant\t%s\t%s\n" % (i,j))
		sys.stderr.flush()
		model = Variant.get_sharding_model(i, j).objects
		for f in range(6):
			for g in range(3):
				for m in range(3):
					snps = model

					if f:
						snps = snps.filter(snp__gannot__feature=f)

					if g:
						snps = snps.filter(genotype=g)

					if m:
						snps = snps.filter(snp__mutation__synonymous=m)

					count = snps.count()

					print("%s\t%s\t%s\t%s\t%s\t%s" % (f, g, m, j, i, count))
