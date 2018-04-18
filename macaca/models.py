import copy
from django.apps import apps
from django.db import models

# Create your models here.
class Chromosome(models.Model):
	name = models.CharField(max_length=5, help_text="Chromosome name, chr1-chr20")
	size = models.IntegerField(help_text = "Chromosome sequence length")

	class Meta:
		db_table = 'chromosome'

class Groups(models.Model):
	name = models.CharField(max_length=15, help_text="Group name that species belongs to")

	class Meta:
		db_table = 'groups'

class Species(models.Model):
	taxonomy = models.IntegerField(help_text="NCBI taxonomy number")
	scientific = models.CharField(max_length=50, help_text="Scientific name")
	common = models.CharField(max_length=50, help_text="Common name")
	group = models.ForeignKey(Groups, on_delete=models.CASCADE, help_text="Species group information")

	class Meta:
		db_table = 'species'

class Individual(models.Model):
	code = models.CharField(max_length=5,help_text="Custom code number for species")
	sample = models.CharField(max_length=20, help_text="sample seria number")
	location = models.CharField(max_length=100, help_text="Where the sample collected")
	non_variant = models.BigIntegerField(help_text = "The number of non-variant sites")
	heterozygous = models.IntegerField(help_text="The number of heterozygous sites")
	homozygous = models.IntegerField(help_text="The number of homozygous sites")
	variants = models.IntegerField(help_text="The number of total variant sites")
	useable = models.BigIntegerField(help_text="The number of total useable sites")
	heterozygosity = models.FloatField(help_text="heterozygosity")
	snv_rate = models.FloatField(help_text="SNV rate")
	pcr_duplicate = models.FloatField(help_text="PCR duplicates (%)")
	mean_coverage = models.FloatField(help_text="Mean coverage")
	species = models.ForeignKey(Species, on_delete=models.CASCADE, help_text="Species information")

	class Meta:
		db_table = 'individual'

class Snp(models.Model):
	position = models.IntegerField(db_index=True, help_text="Position in chromosome sequence")
	reference = models.CharField(max_length=1, help_text="Reference base")
	alteration = models.CharField(max_length=1, help_text="SNP alteration base")
	five = models.CharField(max_length=50, help_text="Five flanking sequence 50 bp")
	three = models.CharField(max_length=50, help_text="Three flanking sequence 50 bp")
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)

	class Meta:
		abstract = False
		db_table = 'snp'
		ordering = ['id']
		index_together = ['position', 'chromosome']

class Variant(models.Model):
	@classmethod
	def get_sharding_model(cls, chrom):
		try:
			return apps.get_registered_model('macaca', 'Variant{}'.format(chrom))
		except LookupError:
			class Meta:
				db_table = 'variant{}'.format(chrom)
				ordering = ['id']

			attrs = {
				'__module__': cls.__module__,
				'Meta': Meta,
			}

			return type(str('Variant{}'.format(chrom)), (cls,), attrs)

	GENOTYPES = (
		(1, 'Homozygote'),
		(2, 'Heterozygote')
	)
	genotype = models.IntegerField(choices=GENOTYPES, db_index=True, help_text="Alteration genotype")
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)
	individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)

	class Meta:
		abstract = True
		ordering = ['id']
		index_together = [
			['genotype', 'snp'],
			['genotype', 'individual'],
			['individual', 'snp'],
			['genotype', 'individual', 'snp']
		]

class Nonvariant(models.Model):
	@classmethod
	def get_sharding_model(cls, chrom):
		try:
			return apps.get_registered_model('macaca', 'Nonvariant{}'.format(chrom))
		except LookupError:
			class Meta:
				db_table = 'nonvariant{}'.format(chrom)
				ordering = ['id']

			attrs = {
				'__module__': cls.__module__,
				'Meta': Meta,
			}

			return type(str('Nonvariant{}'.format(chrom)), (cls,), attrs)
	#chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)
	individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)

	class Meta:
		abstract = True
		ordering = ['id']
		index_together = ['individual', 'snp']

class Gene(models.Model):
	CODING_TYPES = (
		(1, 'protein coding'),
		(2, 'pseudogene'),
		(3, 'snRNA'),
		(4, 'rRNA'),
		(5, 'miRNA'),
		(6, 'miscRNA'),
		(7, 'snoRNA')
	)
	ensembl = models.CharField(max_length=18, db_index=True, help_text="Ensembl gene id")
	name = models.CharField(max_length=20, help_text="Gene symbol")
	description = models.CharField(max_length=200, help_text="Gene description")
	biotype = models.IntegerField(choices=CODING_TYPES, help_text="Gene coding types")
	start = models.IntegerField(help_text="Gene start position")
	end = models.IntegerField(help_text="Gene end position")
	strand = models.CharField(max_length=1, help_text="Gene strand")
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)

	class Meta:
		db_table = 'gene'

class Transcript(models.Model):
	ensembl = models.CharField(max_length=18, help_text="Transcript ensembl id")
	protein = models.CharField(max_length=18, help_text="Protein ensembl id")
	start = models.IntegerField(help_text="Transcript start position")
	end = models.IntegerField(help_text="Transcript end position")
	strand = models.CharField(max_length=1, help_text="Transcript strand")
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE, help_text="which gene for this transcript")

	class Meta:
		db_table = 'transcript'

class Gannot(models.Model):
	'''Gene annotation'''
	FEATURE_TYPES = (
		(1, 'CDS'),
		(2, 'Exon'),
		(3, "3'UTR"),
		(4, 'Intron'),
		(5, "5'UTR")
	)
	gene_pos = models.IntegerField(help_text="Relative position in gene")
	feature = models.IntegerField(choices=FEATURE_TYPES, db_index=True, help_text="Gene features")
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)

	class Meta:
		db_table = 'gannot'
		ordering = ['id']
		index_together = [
			['feature', 'snp'],
			['feature', 'gene'],
			['feature', 'gene', 'snp'],
		]

class Tannot(models.Model):
	'''Transcript annotation'''
	MUTATION_TYPES = (
		(1, 'Non-synonymous'),
		(2, 'Synonymous'),
	)
	transcript_pos = models.IntegerField(help_text="Relative position in transcript")
	ref_codon = models.CharField(max_length=3, help_text="SNP site reference codon")
	codon_pos = models.IntegerField(help_text="The SNP base position in codon")
	alt_codon = models.CharField(max_length=3, help_text="Altered SNP site codon")
	ref_aa = models.CharField(max_length=10, help_text="The reference amino acid for SNP codon")
	alt_aa = models.CharField(max_length=10, help_text="The alteration amino acid for SNP codon")
	protein_pos = models.IntegerField(help_text="Relative position of codon in protein")
	synonymous = models.IntegerField(choices=MUTATION_TYPES, db_index=True, help_text="Mutation type")
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)
	transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE)

	class Meta:
		db_table = 'tannot'

class Mutation(models.Model):
	'''Synonymous or non-synonymous mutations'''
	MUTATION_TYPES = (
		(1, 'Non-synonymous'),
		(2, 'Synonymous'),
	)
	synonymous = models.IntegerField(choices=MUTATION_TYPES, db_index=True, help_text="Mutation type")
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)

	class Meta:
		db_table = 'mutation'
		ordering = ['id']
		index_together = ['synonymous', 'snp']

class Function(models.Model):
	'''Functional Terms'''
	FUNC_TYPES = (
		(1, 'GO'),
		(2, 'KEGG'),
		(3, 'Pfam'),
		(4, 'InterPro')
	)
	source = models.IntegerField(choices=FUNC_TYPES, db_index=True, help_text="The function source database name")
	accession = models.CharField(max_length=15, help_text="Functional database accession id")
	description = models.CharField(max_length=200, help_text="Function description")
	supplement = models.CharField(max_length=80, help_text="Other information")

	class Meta:
		db_table = 'function'

class Funcannot(models.Model):
	'''Functional annotations'''
	function = models.ForeignKey(Function, on_delete=models.CASCADE)
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE)

	class Meta:
		db_table = 'funcannot'
		index_together = ['function', 'gene']

class GroupSpecific(models.Model):
	#the order of foreinkey field is sorted by alphabet
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)
	group = models.ForeignKey(Groups, on_delete=models.CASCADE)
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)

	class Meta:
		db_table = 'group_specific'
		ordering = ['id']
		index_together = [
			['snp', 'group'],
			['snp', 'chromosome'],
			['snp', 'group', 'chromosome']
		]

class SpeciesSpecific(models.Model):
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)
	species = models.ForeignKey(Species, on_delete=models.CASCADE)
	
	class Meta:
		db_table = 'species_specific'
		ordering = ['id']
		index_together = [
			['snp', 'species'],
			['snp', 'chromosome'],
			['snp', 'species', 'chromosome']
		]

class Statistics(models.Model):
	feature = models.IntegerField(db_index=True)
	genotype = models.IntegerField(db_index=True)
	mutation = models.IntegerField(db_index=True)
	counts = models.IntegerField()
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)
	individual = models.ForeignKey(Individual, on_delete=models.CASCADE)

	class Meta:
		db_table = 'statistics'
		index_together = ['feature', 'genotype', 'mutation']

class Orthology(models.Model):
	human_ensembl = models.CharField(max_length=18, db_index=True, help_text="human ensembl gene id")
	human_hgnc = models.CharField(max_length=10, help_text="human gene hgnc id")
	human_name = models.CharField(max_length=200, help_text="human gene name")
	human_symbol = models.CharField(max_length=20, help_text="human gene symbol")
	support = models.CharField(max_length=255, help_text="orthology support database")
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE)

	class Meta:
		db_table = 'orthology'
		index_together = ['human_ensembl', 'gene']

class Drug(models.Model):
	DRUG_TYPES = (
		(1, 'biotech'),
		(2, 'small molecule')
	)
	partner = models.CharField(max_length=10, help_text="drugbank target gene id")
	drug_id = models.CharField(max_length=7, db_index=True, help_text="drugbank durg id")
	drug_name = models.CharField(max_length=255, help_text="drugbank drug name")
	drug_type = models.IntegerField(choices=DRUG_TYPES, help_text="drugbank drug type")
	orthology = models.ForeignKey(Orthology, on_delete=models.CASCADE)

	class Meta:
		db_table = 'drug'
		index_together = ['drug_id', 'orthology']

class Disease(models.Model):
	gomim = models.IntegerField(help_text="Gene omim id")
	pomim = models.IntegerField(db_index=True, help_text="disease omim id")
	phenotype = models.CharField(max_length=255, help_text="disease phenotype description")
	symbol = models.CharField(max_length=20, help_text="disease phenotype symbol")
	orthology = models.ForeignKey(Orthology, on_delete=models.CASCADE)
	
	class Meta:
		db_table = 'disease'
		index_together = ['pomim', 'orthology']

