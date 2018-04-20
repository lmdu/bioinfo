#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb

conn = MySQLdb.connect(
	host = 'localhost',
	port = 3306,
	user = 'root',
	passwd = '',
	db = 'macaca'
)
c = conn.cursor()

prefix = 'macaca'

variant_sql = '''
CREATE TABLE IF NOT EXISTS variant{0} (
	id int(11) NOT NULL AUTO_INCREMENT,
	genotype tinyint(1) NOT NULL,
	chromosome_id int(11) NOT NULL,
	individual_id int(11) NOT NULL,
	snp_id int(11) NOT NULL,
	PRIMARY KEY (id),
	KEY variant_genotype_{0} (genotype),
	KEY variant_individual_{0} (individual_id),
	KEY variant_snp_{0} (snp_id),
	KEY variant_genotype_individual_{0} (genotype,individual_id),
	KEY variant_genotype_snp_{0} (genotype,snp_id),
	KEY variant_individual_snp_{0} (individual_id,snp_id),
	KEY variant_genotype_individual_snp_{0} (genotype,individual_id,snp_id)
) ENGINE=Aria DEFAULT CHARSET=utf8
'''

snp_sql = '''
CREATE TABLE IF NOT EXISTS snp{0} (
	id int(11) NOT NULL AUTO_INCREMENT,
	snp_id int(11) NOT NULL,
	position int(11) NOT NULL,
	chromosome_id int(11) NOT NULL,
	PRIMARY KEY (id),
	KEY snp_snp_id_{0} (snp_id),
	KEY snp_position_{0} (position),
	KEY snp_chromosome_id_{0} (chromosome_id),
	KEY snp_position_chromosome_id_{0} (position, chromosome_id),
	KEY snp_snp_chromosome_id_{0} (snp_id, chromosome_id)
) ENGINE=Aria DEFAULT CHARSET=utf8
'''

non_sql = '''
CREATE TABLE IF NOT EXISTS nonvariant{0} (
	id int(11) NOT NULL AUTO_INCREMENT,
	individual_id int(11) NOT NULL,
	snp_id int(11) NOT NULL,
	PRIMARY KEY (id),
	KEY non_individual_id_{0} (individual_id),
	KEY non_snp_id_{0} (snp_id),
	KEY non_indivdual_snp_{0} (individual_id, snp_id)
) ENGINE=Aria DEFAULT CHARSET=utf8
'''

for i in range(1, 21):
	c.execute(variant_sql.format(i))
	c.execute(snp_sql.format(i))
	c.execute(non_sql.format(i))

print('load base information')
c.execute("load data local infile 'chromosome.table' into table chromosome")
c.execute("load data local infile 'group.table' into table groups")
c.execute("load data local infile 'species.table' into table species")
c.execute("load data local infile 'individual.table' into table individual")
c.execute("load data local infile 'gene.table' into table gene")
c.execute("load data local infile 'transcript.table' into table transcript")
c.execute("load data local infile 'gene_annot.table' into table gannot")
c.execute("load data local infile 'transcript_annot.table' into table tannot")
c.execute("load data local infile 'mutation.table' into table mutation")
c.execute("load data local infile 'function.table' into table function")
c.execute("load data local infile 'funcannot.table' into table funcannot")
c.execute("load data local infile 'disease.table' into table disease")
c.execute("load data local infile 'drug.table' into table drug")
c.execute("load data local infile 'orthology.table' into table orthology")
c.execute("load data local infile 'statistics.table' into table statistics")
print('load specific snps')
c.execute("load data local infile 'group_specific.table' into table group_specific")
c.execute("load data local infile 'species_specific.table' into table species_specific")
print('load snps')
c.execute("load data local infile 'snp.table' into table snp")
print('load variants')

#for i in range(1, 21):
#	c.execute("load data local infile 'snp.table.{0}' into table snp_{0}".format(i))

for i in range(1, 21):
	print('load variant, {0}'.format(i))
	c.execute("load data local infile 'variant.table.{0}' into table variant{0}".format(i))

for j in range(1, 21):
	print('load snps, {}'.format(j))
	c.execute("load data local infile 'snp.table.{0}' into table snp{0}".format(j))

for k in range(1, 21):
	print('load non, {}'.format(k))
	c.execute("load data local infile 'non_variant.table.{0}' into table nonvariant{0}".format(k))

c.close()
conn.commit()
conn.close()
