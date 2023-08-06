#!python
'''
A Python package for summarizing QC data from the ncov-tools pipeline.
'''

import argparse
import sys
import ncov.parser.qc as qc
import ncov.parser
import csv

parser = argparse.ArgumentParser(description="Tool for summarizing QC data")
parser.add_argument('-c', '--consensus', help='<sample>.consensus.fasta file to process')
parser.add_argument('-v', '--variants',
                    help='<sample>.variants.tsv file to process')
parser.add_argument('-e', '--coverage',
                    help='<sample>.per_base_coverage.bed file to process')
parser.add_argument('-i', '--indel', action='store_true',
                    help='flag to determine whether to count indels')
parser.add_argument('-m', '--meta', default=None,
                    help='full path to the metadata file')
parser.add_argument('-a', '--alleles',
                    help='full path to the alleles.tsv file')
parser.add_argument('-s', '--sample',
                    help='name of sample being processed')
parser.add_argument('-x', '--mixture', default=None,
                    help='full path to the mixture report')
parser.add_argument('-p', '--platform', default='illumina',
                    help='sequencing platform used')
parser.add_argument('-r', '--run_name',
                    help='run name for sample')
parser.add_argument('-l', '--lineage',
                    help='full path to the Pangolin lineage report')
parser.add_argument('-t', '--aa_table',
                    help='full path to the <sample>_aa_table.tsv file')
parser.add_argument('-u', '--mutations',
                    help='full path to the <run>_ncov_watch_variants.tsv file')
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit('Invalid number of arguments')
args = parser.parse_args()

qc_line = dict()
qc_line.update({'sample' : args.sample})

try:
    meta = ncov.parser.Meta(file=args.meta)
    meta.import_metadata()
    qc_line.update(meta.data[args.sample])
except:
    qc_line.update({'qpcr_ct' : 'NA', 'collection_date' : 'NA',
                    'num_months' : 'NA', 'num_weeks' : 'NA'})

if args.platform == 'illumina':
    if str(args.variants).endswith('.variants.tsv'):
        vars = ncov.parser.Variants(file=args.variants)
        qc_line.update(vars.get_total_variants())
    elif str(args.variants).endswith('.vcf') or str(args.variants).endswith('.vcf.gz'):
        vars = ncov.parser.Vcf(file=args.variants)
        qc_line.update(vars.get_variant_counts())
    else:
        sys.exit('Must be a valid variant.tsv or .vcf file for the Illumina platform')
elif args.platform == 'oxford-nanopore':
    if str(args.variants).endswith('.vcf') or str(args.variants).endswith('.vcf.gz'):
        vars = ncov.parser.Vcf(file=args.variants)
        qc_line.update(vars.get_variant_counts())
    else:
        sys.exit('Must be a valid VCF file for the Oxford-Nanopore platform')


alleles = ncov.parser.Alleles(file=args.alleles)
qc_line.update(alleles.get_variant_counts(sample=args.sample))

cons = ncov.parser.Consensus(file=args.consensus)
qc_line.update(cons.count_iupac_in_fasta())
qc_line.update(cons.get_genome_completeness())

coverage = ncov.parser.PerBaseCoverage(file=args.coverage)
qc_line.update(coverage.get_coverage_stats())

# Add the lineage from the Pangolin report
try:
    lineage = ncov.parser.Lineage(file=args.lineage)
    lineage.create_lineage_dictionary()
    qc_line.update({"lineage" : lineage.lineage_dict[args.sample]["lineage"]})
    qc_line.update({"lineage_notes" : lineage.lineage_dict[args.sample]["notes"]})
except:
    qc_line.update({"lineage" : "none"})
    qc_line.update({"lineage_notes" : "none"})

# Add the watch list mutations
try:
    watchlist = ncov.parser.WatchList(file=args.mutations)
    qc_line.update({"mutations" : watchlist.get_mutation_string(sample=args.sample)})
except:
    qc_line.update({"mutations" : "none"})

# Get a list of consequences from the SNPEff variant annotations
frameshift_indels = False
try:
    annotations = ncov.parser.Snpeff(file=args.aa_table)
    annotations.get_list_of_consequences()
    if annotations.has_frameshift():
        frameshift_indels = True
except:
    pass

# Produce warning flags
qc_flags = list()
if qc_line['genome_completeness'] < 0.5:
    qc_flags.append("INCOMPLETE_GENOME")
elif qc_line['genome_completeness'] < 0.9:
    qc_flags.append("PARTIAL_GENOME")

#num_indel_non_triplet = qc_line['num_variants_indel'] - qc_line['num_variants_indel_triplet']
#if num_indel_non_triplet > 0:
if frameshift_indels:
    qc_flags.append("POSSIBLE_FRAMESHIFT_INDELS")

if qc_line['num_consensus_iupac'] > 5:
    qc_flags.append("EXCESS_AMBIGUITY")

# the mixture report is currently generated for illuina runs, ont is
# not supported at this time
if args.mixture:
    if args.platform == 'illumina':
        mixture = set()
        with open(args.mixture, 'r') as mfh:
            reader = csv.DictReader(mfh, delimiter='\t')
            for record in reader:
                mixture.add(record['sample_a'])
        if args.sample in mixture:
            qc_flags.append("POSSIBLE_MIXTURE")

# Calculate number of variants per week, while accounting for incompleteness
if qc_line['num_weeks'] != 'NA':

    if qc_line['genome_completeness'] > 0.1:
        scaled_variants = qc_line['num_variants_snvs'] / qc_line['genome_completeness']

        # very conservative upper limit on the number of acceptable variants
        # samples that fail this check should be manually reviewed incorporating other
        # evidence (frameshift indels, not failed outright)
        # Removing EXCESS_VARIANTS flag due to discovery of lineage carrying
        # high number of mutations -- December 17, 2020.
        #variant_threshold = qc_line['num_weeks'] * 0.75 + 15
        #if scaled_variants > variant_threshold:
        #    qc_flags.append("EXCESS_VARIANTS")
        qc_line['scaled_variants_snvs'] = "%.2f" % (scaled_variants)
    else:
        qc_line['scaled_variants_snvs'] = "NA"
else:
    qc_line['scaled_variants_snvs'] = "NA"

qc_flag_str = "PASS"
if len(qc_flags) > 0:
    qc_flag_str = ",".join(qc_flags)

qc_line.update({'qc_pass' : qc_flag_str})
qc_line.update({'run_name' : args.run_name})

qc.write_qc_summary_header()
qc.write_qc_summary(summary=qc_line)
