# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Individual, Variant, Chromosome, Species, Snp, Group
from .models import GroupSpecific, SpeciesSpecific, Mutation

# Create your views here.
def index(request):
	return render(request, 'index.html')

def organism(request):
	samples = Individual.objects.all()
	return render(request, 'organism.html', {
		'samples': samples,
	})

def species(request, sid):
	one = Species.objects.get(id=sid)
	return render(request, 'species.html', {
		'species': one,
	})


def group(request, gid):
	one = Group.objects.get(id=gid)
	return render(request, 'group.html', {
		'group': one,
	})

def variants(request):
	chromos = Chromosome.objects.all()[:20]
	species = Individual.objects.all()

	paras = dict(
		page = int(request.GET.get('page', 1)),
		records = int(request.GET.get('records', 10)),
		chromosome = int(request.GET.get('chr', 1)),
		sample = int(request.GET.get('sample', 1)),
		feature = int(request.GET.get('feature', 0)),
		genotype = int(request.GET.get('genotype', 0)),
		mutation = int(request.GET.get('mutation', 0))
	)

	snps = Variant.get_sharding_model(paras['sample'],paras['chromosome']).objects.all()

	if paras['mutation']:
		snps = snps.filter(snp__mutation__synonymous=paras['mutation'])

	if paras['feature']:
		snps = snps.filter(snp__gannot__feature=paras['feature'])

	if paras['genotype']:
		snps = snps.filter(genotype=paras['genotype'])

	paginator = Paginator(snps, paras['records'])

	try:
		snps = paginator.page(paras['page'])
	except PageNotAnInteger:
		snps = paginator.page(1)
	except EmptyPage:
		snps = paginator.page(paginator.num_pages)

	return render(request, 'variants.html', {
		'snps': snps,
		'chromos': chromos,
		'species': species,
		'paras': paras
	})

#Get snp by variant id
def snp(request, sid):
	one = Variant.objects.get(id=sid)
	genes = one.snp.gannot_set.all()
	transcripts = one.snp.tannot_set.all()
	others = Variant.objects.filter(snp__id=one.snp.id).exclude(id=sid)
	return render(request, 'snp.html', {
		'snp': one,
		'genes': genes,
		'transcripts': transcripts,
		'others': others,
	})

#get snp by mac snp id
def snpid(request, indiv, sid):
	indiv = int(indiv)
	sid = int(sid)
	snp = Snp.objects.get(id=sid)
	one = Variant.get_sharding_model(indiv, snp.chromosome.id).objects.get(snp__id=sid)
	genes = one.snp.gannot_set.all()
	transcripts = one.snp.tannot_set.all()
	others = []
	#for i in range(1, 21):
	#	if i == indiv:
	#		continue
	#	other = Variant.get_sharding_model(i, snp.chromosome.id).objects.get(snp__id=sid)
	#	if other:
	#		others.append(other)

	return render(request, 'snp.html', {
		'snp': one,
		'genes': genes,
		'transcripts': transcripts,
		'others': others,
	})


def search(request):
	tag = request.GET.get('search')
	if tag.startswith('MACSNP'):
		i = int(tag[6:9])
		s = int(tag[9:])
		return snpid(request, i, s)
	
	chr_id = int(tag[3:5])
	start, end = map(int,tag.split(':')[1].split('-'))

	species = Individual.objects.all()
	chrom = Chromosome.objects.get(id=chr_id)
	paras = dict(
		chrname = chrom.name,
		start = start,
		end = end,
		tag = request.GET.get('search'),
		page = int(request.GET.get('page', 1)),
		records = int(request.GET.get('records', 10)),
		sample = int(request.GET.get('sample', 0)),
		feature = int(request.GET.get('feature', 0)),
		genotype = int(request.GET.get('genotype', 0)),
		mutation = int(request.GET.get('mutation', 0))
	)

	snps = Variant.objects.filter(snp__chromosome=chr_id).filter(snp__position__range=(start, end))

	if paras['sample']:
		snps = snps.filter(individual=paras['sample'])

	if paras['genotype']:
		snps = snps.filter(genotype=paras['genotype'])

	if paras['mutation']:
		snps = snps.filter(snp__mutation__synonymous=paras['mutation'])

	if paras['feature']:
		snps = snps.filter(snp__gannot__feature=paras['feature'])


	paginator = Paginator(snps, paras['records'])

	try:
		snps = paginator.page(paras['page'])
	except PageNotAnInteger:
		snps = paginator.page(1)
	except EmptyPage:
		snps = paginator.page(paginator.num_pages)

	return render(request, 'search.html', {
		'snps': snps,
		'species': species,
		'paras': paras,
	})

def specific(request):
	groups = Group.objects.all()
	species = Species.objects.all()
	paras = dict(
		page = int(request.GET.get('page', 1)),
		records = int(request.GET.get('records', 10)),
		chromosome = int(request.GET.get('chr', 0)),
		feature = int(request.GET.get('feature', 0)),
		mutation = int(request.GET.get('mutation', 0)),
		group = int(request.GET.get('group', -1)),
		species = int(request.GET.get('species', 0)),
	)

	if paras['group'] >= 0:
		if paras['group'] == 0:
			snps = GroupSpecific.objects.all()
		else:
			snps = GroupSpecific.objects.filter(group=paras['group'])
	elif paras['species'] >= 0:
		if paras['species'] == 0:
			snps = SpeciesSpecific.objects.all()
		else:
			snps = SpeciesSpecific.objects.filter(species=paras['species'])

	if paras['mutation']:
		snps = snps.filter(snp__mutation__synonymous=paras['mutation'])

	if paras['feature']:
		snps = snps.filter(snp__gannot__feature=paras['feature'])

	if paras['chromosome']:
		snps = snps.filter(snp__chromosome=paras['chromosome'])
	
	paginator = Paginator(snps, paras['records'])

	try:
		snps = paginator.page(paras['page'])
	except PageNotAnInteger:
		snps = paginator.page(1)
	except EmptyPage:
		snps = paginator.page(paginator.num_pages)

	return render(request, 'specific.html', {
		'snps': snps,
		'groups': groups,
		'species': species,
		'paras': paras,
	})

def snpspec(request, cat, cid, sid):
	cid = int(cid)
	sid = int(sid)
	if cat == 'G':
		category = Group.objects.get(id=cid)
	else:
		category = Species.objects.get(id=cid)
	snp = Snp.objects.get(id=sid)
	genes = snp.gannot_set.all()
	transcripts = snp.tannot_set.all()
	return render(request, 'snpspec.html', {
		'cat': cat,
		'snp': snp,
		'category': category,
		'genes': genes,
		'transcripts': transcripts
	})

def retrieve(request):
	if not request.GET:
		individuals = Individual.objects.all()
		groups = Group.objects.all()
		species = Species.objects.all()
		return render(request, 'retrieve.html', {
			'individuals': individuals,
			'groups': groups,
			'species': species,
		})

	
	#print(request.GET.getlist('individuals'))
	#return HttpResponse()
	paras = dict(
		page = int(request.GET.get('page', 1)),
		records = int(request.GET.get('records', 10)),
		chromosome = int(request.GET.get('chr')),
		start = request.GET.get('start', 0),
		end = request.GET.get('end', 0),
		category = request.GET.get('category', 'individual'),
		individual = int(request.GET.get('individual')),
		group = int(request.GET.get('group')),
		species = int(request.GET.get('species')),
		feature = int(request.GET.get('feature')),
		genotype = int(request.GET.get('genotype')),
		mutation = int(request.GET.get('mutation')),
		gene = request.GET.get('gene')
	)

	paras['start'] = int(paras['start']) if paras['start'] else 0
	paras['end'] = int(paras['end']) if paras['end'] else 0

	if paras['category'] == 'group':
		snps = GroupSpecific.objects.filter(group=paras['group'], snp__chromosome=paras['chromosome'])
	elif paras['category'] == 'species':
		snps = SpeciesSpecific.objects.filter(species=paras['species'], snp__chromosome=paras['chromosome'])	
	elif paras['category'] == 'individual':
		snps = Variant.get_sharding_model(paras['individual'], paras['chromosome']).objects.all()
		
		if paras['genotype']:
			snps = snps.filter(genotype=paras['genotype'])

	if paras['start'] and paras['end']:
		snps = snps.filter(snp__position__range=(paras['start'], paras['end']))

	if paras['feature']:
		snps = snps.filter(snp__gannot__feature=paras['feature'])

	if paras['mutation']:
		snps = snps.filter(snp__mutation__synonymous=paras['mutation'])

	if paras['gene']:
		snps = snps.filter(snp__gannot__gene__ensembl=paras['gene'])

	paginator = Paginator(snps, paras['records'])
	try:
		snps = paginator.page(paras['page'])
	except PageNotAnInteger:
		snps = paginator.page(1)
	except EmptyPage:
		snps = paginator.page(paginator.num_pages)

	return render(request, 'download.html', {
		'snps': snps,
		'paras': paras,
	})

def download(request):
	snp_ids = request.POST.getlist('snps')
	category = request.POST.get('category')
	chromosome = int(request.POST.get('chromosome'))
	individual = int(request.POST.get('individual'))

	if category == 'group':
		snps = GroupSpecific.objects.filter(snp__in=snp_ids)
	elif category == 'species':
		snps = SpeciesSpecific.objects.filter(snp__in=snp_ids)
	else:
		snps = Variant.get_sharding_model(individual, chromosome).objects.filter(snp__in=snp_ids)

	contents = ["SNP ID\tChromosome\tPosition\tReference\tAlteration\t%s\tGenotype\t5'flank\t3'flank\n" % category]
	out_formats = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
	for snp in snps:
		if category == 'group':
			sid = "MACSNPG%02d%09d" % (snp.group.id, snp.snp.id)
			organism = snp.group.name
			genotype = 'homozygote'
		elif category == 'species':
			sid = "MACSNPS%02d%09d" % (snp.species.id, snp.snp.id)
			organism = snp.species.common
			genotype = 'homozygote'
		else:
			sid = "MACSNP%03d%09d" % (snp.individual.id, snp.snp.id)
			organism = snp.individual.code
			genotype = 'homozygote' if snp.genotype == 1 else 'heterozygote'
		
		contents.append(out_formats % (
			sid, snp.snp.chromosome.name, snp.snp.position,
			snp.snp.reference, snp.snp.alteration, organism,
			genotype, snp.snp.five, snp.snp.three
		))

	return HttpResponse('<pre>'+''.join(contents)+'</pre>')

def gene(request, gid):
	pass

def pileup(request, sid):
	snp = Snp.objects.get(id=sid)
	variants = Variant.objects.filter(snp__id=sid)
	header = ["#CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO","FORMAT"]
	line = [snp.chromosome.name, str(snp.position), str(snp.id), snp.reference, snp.alteration, '.', 'PASS', '.', 'GT']
	genotypes = ['0/0', '1/1', '0/1']
	for var in variants:
		header.append(var.individual.code)
		line.append(genotypes[var.genotype])

	#header = "\t".join(header)
	line = "\t".join(line)

	vcf = "{1}".format(header, line)

	return render(request, 'pileup.html', {
		'vcf': vcf,
		'chromosome': snp.chromosome.name,
		'position': snp.position,
	})
	