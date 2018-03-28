from django.apps import apps
from django.db import models

# Create your models here.
class Chromosome(models.Model):
	name = models.CharField(max_length=5, help_text="Chromosome name, chr1-chr20")
	size = models.IntegerField(help_text = "Chromosome sequence length")

class Group(models.Model):
	name = models.CharField(max_length=15, help_text="Group name that species belongs to")

class Species(models.Model):
	taxonomy = models.IntegerField(help_text="NCBI taxonomy number")
	scientific = models.CharField(max_length=50, help_text="Scientific name")
	common = models.CharField(max_length=50, help_text="Common name")
	group = models.ForeignKey(Group, on_delete=models.CASCADE, help_text="Species group information")

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

class Snp(models.Model):
	position = models.IntegerField(db_index=True, help_text="Position in chromosome sequence")
	reference = models.CharField(max_length=1, help_text="Reference base")
	alteration = models.CharField(max_length=1, help_text="SNP alteration base")
	five = models.CharField(max_length=50, help_text="Five flanking sequence 50 bp")
	three = models.CharField(max_length=50, help_text="Three flanking sequence 50 bp")
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)

	class Meta:
		index_together = ['position', 'chromosome']

class Variant(models.Model):
	@classmethod
	def get_sharding_model(cls, individual, chrom):
		try:
			return apps.get_registered_model('macaca', 'Variant_{}_{}'.format(individual, chrom))
		except LookupError:
			class Meta:
				db_table = 'variant_{0}_{1}'.format(individual, chrom)
				ordering = ['id']

			attrs = {
				'__module__': cls.__module__,
				'Meta': Meta,
			}

			return type(str('Variant_{0}_{1}'.format(individual, chrom)), (cls,), attrs)

	GENOTYPES = (
		(1, 'Homozygote'),
		(2, 'Heterozygote')
	)
	genotype = models.IntegerField(choices=GENOTYPES, db_index=True, help_text="Alteration genotype")
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

class Transcript(models.Model):
	ensembl = models.CharField(max_length=18, help_text="Transcript ensembl id")
	protein = models.CharField(max_length=18, help_text="Protein ensembl id")
	start = models.IntegerField(help_text="Transcript start position")
	end = models.IntegerField(help_text="Transcript end position")
	strand = models.CharField(max_length=1, help_text="Transcript strand")
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE, help_text="which gene for this transcript")

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
		ordering = ['id']
		index_together = ['feature', 'snp']

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

class Mutation(models.Model):
	'''Synonymous or non-synonymous mutations'''
	MUTATION_TYPES = (
		(1, 'Non-synonymous'),
		(2, 'Synonymous'),
	)
	synonymous = models.IntegerField(choices=MUTATION_TYPES, db_index=True, help_text="Mutation type")
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)

	class Meta:
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
	source = models.IntegerField(choices=FUNC_TYPES, help_text="The function source database name")
	accession = models.CharField(max_length=15, help_text="Functional database accession id")
	description = models.CharField(max_length=200, help_text="Function description")
	supplement = models.CharField(max_length=80, help_text="Other information")

class Funcannot(models.Model):
	'''Functional annotations'''
	function = models.ForeignKey(Function, on_delete=models.CASCADE)
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE)

	class Meta:
		index_together = ['function', 'gene']

class GroupSpecific(models.Model):
	#the order of foreinkey field is sorted by alphabet
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)

	class Meta:
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
		ordering = ['id']
		index_together = [
			['snp', 'species'],
			['snp', 'chromosome'],
			['snp', 'species', 'chromosome']
		]

class Statistics(models.Model):
	feature = models.IntegerField()
	genotype = models.IntegerField()
	mutation = models.IntegerField()
	counts = models.IntegerField()
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)
	individual = models.ForeignKey(Individual, on_delete=models.CASCADE)

class Orthology(models.Model):
	human_ensembl = models.CharField(max_length=18, help_text="human ensembl gene id")
	human_hgnc = models.CharField(max_length=10, help_text="human gene hgnc id")
	human_name = models.CharField(max_length=200, help_text="human gene name")
	human_symbol = models.CharField(max_length=20, help_text="human gene symbol")
	support = models.CharField(max_length=255, help_text="orthology support database")
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE)

class Drug(models.Model):
	DRUG_TYPES = (
		(1, 'biotech'),
		(2, 'small molecule')
	)
	partner = models.CharField(max_length=10, help_text="drugbank target gene id")
	drug_id = models.CharField(max_length=7, help_text="drugbank durg id")
	drug_name = models.CharField(max_length=255, help_text="drugbank drug name")
	drug_type = models.IntegerField(choices=DRUG_TYPES, help_text="drugbank drug type")
	orthology = models.ForeignKey(Orthology, on_delete=models.CASCADE)

#class Disease(models.Model):
#	omim_id = models.IntegerField(help_text="omim id")
#	orthology = models.ForeignKey(Orthology, on_delete=models.CASCADE)

	