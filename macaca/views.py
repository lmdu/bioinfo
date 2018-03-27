# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from .models import *

# Create your views here.
def home(request):
	return render(request, 'macaca/home.html')

def organism(request):
	samples = Individual.objects.all()
	return render(request, 'macaca/organism.html', {
		'samples': samples,
	})

def species(request, sid):
	one = Species.objects.get(id=sid)
	return render(request, 'macaca/species.html', {
		'species': one,
	})


def group(request, gid):
	one = Group.objects.get(id=gid)
	return render(request, 'macaca/group.html', {
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

	return render(request, 'macaca/variants.html', {
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
	return render(request, 'macaca/snp.html', {
		'snp': one,
		'genes': genes,
		'transcripts': transcripts,
		'others': others,
	})

#get snp by mac snp id
def snpid(request, indiv, sid):
	indiv = int(indiv)
	sid = int(sid)
	try:
		snp = Snp.objects.get(id=sid)
		one = Variant.get_sharding_model(indiv, snp.chromosome.id).objects.get(snp__id=sid)
	except ObjectDoesNotExist:
		raise Http404('MACSNP%03d%09d does not exists in this database' % (indiv, sid))
	genes = one.snp.gannot_set.all()
	transcripts = one.snp.tannot_set.all()
	others = []
	for i in range(1, 21):
		if i == indiv:
			continue
		
		try:
			other = Variant.get_sharding_model(i, snp.chromosome.id).objects.get(snp__id=sid)
		except ObjectDoesNotExist:
			pass
		else:
			others.append(other)

	return render(request, 'macaca/snp.html', {
		'snp': one,
		'genes': genes,
		'transcripts': transcripts,
		'others': others,
	})


def search(request):
	q = request.GET.get('q')
	if q.startswith(('MACSNP', 'ENSMMUG')) and len(q) != 18:
		raise Http404("%s is not right SNP ID" % q)

	if q.startswith(('MACSNPG', 'MACSNPS')):
		cat, cid, sid = q[6], q[7:9], q[9:]
		return redirect('snpspec', cat, cid, sid)

	elif q.startswith('MACSNP'):
		indiv, sid= q[6:9], q[9:]
		return redirect('snpid', indiv, sid)

	elif q.startswith('ENSMMUG'):
		return redirect('gene', q)

	

def specific(request):
	groups = Group.objects.all()
	species = Species.objects.all()
	paras = dict(
		page = int(request.GET.get('page', 1)),
		records = int(request.GET.get('records', 10)),
		chromosome = int(request.GET.get('chr', 1)),
		feature = int(request.GET.get('feature', 0)),
		mutation = int(request.GET.get('mutation', 0)),
		group = int(request.GET.get('group', -1)),
		species = int(request.GET.get('species', 0)),
	)

	if paras['group'] >= 0:
		if paras['group'] == 0:
			snps = GroupSpecific.objects.all()
		else:
			snps = GroupSpecific.objects.filter(group=paras['group'], chromosome=paras['chromosome'])
	elif paras['species'] >= 0:
		if paras['species'] == 0:
			snps = SpeciesSpecific.objects.all()
		else:
			snps = SpeciesSpecific.objects.filter(species=paras['species'], chromosome=paras['chromosome'])

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

	return render(request, 'macaca/specific.html', {
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
	return render(request, 'macaca/snpspec.html', {
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
		return render(request, 'macaca/retrieve.html', {
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

	return render(request, 'macaca/download.html', {
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
	gene = Gene.objects.get(ensembl=gid)
	transcripts = gene.transcript_set.all()
	orthologys = gene.orthology_set.all()
	gos = gene.funcannot_set.filter(function__source=1)
	keggs = gene.funcannot_set.filter(function__source=2)
	ips = gene.funcannot_set.filter(function__source=3)
	pfams = gene.funcannot_set.filter(function__source=4)

	annots = Gannot.objects.filter(gene=gene.id, feature=1)
	snps = []
	for annot in annots:
		for i in range(1, 21):
			try:
				snp = Variant.get_sharding_model(i, annot.snp.chromosome.id).objects.get(snp__id=annot.snp.id)
			except ObjectDoesNotExist:
				pass
			else:
				snps.append(snp)

	return render(request, 'macaca/gene.html', {
		'gene': gene,
		'transcripts': transcripts,
		'orthologys': orthologys,
		'gos': gos,
		'keggs': keggs,
		'ips': ips,
		'pfams': pfams,
		'snps': snps,
	})

def drugs(request):
	drugs = Drug.objects.all()
	return render(request, 'macaca/drug.html', {
		'drugs': drugs,
	})

	

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

	return render(request, 'macaca/pileup.html', {
		'vcf': vcf,
		'chromosome': snp.chromosome.name,
		'position': snp.position,
	})

def statistics(request):
	paras = dict(
		feature = int(request.GET.get('feature', 0)),
		genotype = int(request.GET.get('genotype', 0)),
		mutation = int(request.GET.get('mutation', 0))
	)

	stat = Statistics.objects.filter(
		feature = paras['feature'],
		genotype = paras['genotype'],
		mutation = paras['mutation']
	).order_by('individual', 'chromosome')

	rows = []
	row = []
	indiv = 1
	for s in stat:
		if s.individual.id != indiv:
			rows.append(row)
			row = []
			indiv = s.individual.id

		if not row:
			row.append(s.individual.code)
		
		row.append(s.counts)

	rows.append(row)

	return render(request, 'macaca/statistics.html', {
		'paras': paras,
		'rows': rows,
	})

	