# coding=utf-8

from argparse import ArgumentParser, Namespace, _ArgumentGroup, _SubParsersAction


def phasing(args):
    """Main function for phasing mode

    Args:
        args:
    """
    
    print('phasing mode')
    print(args)
    input_data = InputData(output_directory_path)
    input_data.add_haplotype_information_from_file(vcf_file_path)
    input_data.add_reads_from_file('hg001_alignment_sorted.bam', sample = 'HG001')
    for phasable_sample in input_data:
        print(phasable_sample.sample)
        for alignment in phasable_sample:
            phased_read = PhasedRead(alignment, ...)
        if phased_read.is_Phased:
            print(phased_read, phased_read.phase)
            phased_read.write_to_bam()
            
            
    return


def phasability(args):
    """Main function for phasability mode

    Args:
        args:
    """
    
    print('phasability mode')
    print(args)
    
    return


def error_analysis(args):
    """Main simulation mode

    Args:
        args:
    """
    
    print('simulation mode')
    print(args)
    
    return


def getArgs() -> object:
    """Parses arguments:"""
    
    ############## LRphase Arguments ##############
    
    lrphase_parser: ArgumentParser = ArgumentParser(
            prog = 'LRphase', description = 'Tools for phasing individual long reads using haplotype information.'
            )
    
    lrphase_parser.add_argument('--version', action = 'version', version = '%(prog)s 1.0')
    lrphase_parser.add_argument(
            '-q', '--quiet', help = 'stdout will be muted', action = 'store_true', dest = 'quiet_mode'
            )
    
    lrphase_subparsers: _SubParsersAction = lrphase_parser.add_subparsers(
            title = '[LRphase modes]', dest = 'mode', description = 'Choose which mode to run:',
            help = 'mode must be added as first argument (ex: LRphase phasing)', required = True
            )
    
    ############## Phasing Mode Arguments ############## 
    
    phasing_parser: ArgumentParser = lrphase_subparsers.add_parser(
            'phasing', description = "Tool for phasing individual long reads using haplotype information."
            )
    
    ############## Phasing Mode Required Arguments ##############
    
    phasing_parser_required: _ArgumentGroup = phasing_parser.add_argument_group('Required', 'Required for phasing')
    
    phasing_parser_required.add_argument(
            '-o', '--output_directory_name', required = True,
            help = 'Name given to directory where results will be output (ex: -o minion_GM12878_run3_phasing_output)',
            dest = 'output_directory_name', metavar = "output directory name"
            )
    
    phasing_parser_required.add_argument(
            '-v', '--vcf', required = True,
            help = 'Path to vcf file with haplotype information that will be used for phasing. (Must be in .vcf.gz format '
                   'with tabix index in same folder. If .vcf file is provided, bgzip and tabix must be installed and '
                   'available on PATH because LRphase will attempt to convert it.  EX: -v GM12878_haplotype.vcf.gz)',
            dest = 'vcf_file_name', metavar = 'vcf file'
            )
    
    phasing_parser_required.add_argument(
            '-i', required = True,
            help = 'Path to alignment file (.bam or .sam) of long reads that will be used for phasing. If either a .sam '
                   'file is provided or an index is not found, .sam and .bam file will be sorted and indexed using pysam. '
                   'Sorted.bam files should be in same directory as their index (.sorted.bam.bai). EX: -a '
                   'data/minion_GM12878_run3.sorted.bam, -i minion_GM12878_run3.sam) Path to long read file in .fastq '
                   'format that will be used for alignment and phasing (ex: -i minion_GM12878_run3.fastq)',
            dest = 'long_read_inputs', metavar = 'long-read input file', action = 'append', nargs = '*'
            )
    
    phasing_parser_required.add_argument(
            '-r', '--reference', required = False,
            help = 'Path to reference genome sequence file. REQUIRED if -i is used to specify reads in fastq format to be '
                   'aligned prior to phasing. (file types allowed: .fa, .fna, fasta. EX: -r data/reference_hg38.fna)',
            dest = 'reference_genome', metavar = 'reference genome'
            )
    
    ############## Phasing Mode Output Options ##############
    phasing_parser_output: _ArgumentGroup = phasing_parser.add_argument_group(
            'Output options', 'Add tags to phased reads and custom output options for phased BAM files.'
            )
    
    phasing_parser_output.add_argument(
            '-P', '--add_phase_set_tag_to_output',
            help = 'Use the --add_sample_tag_to_output option to add PS:i:x tags to the bam output to label reads '
                   'according to the phase set that was indicated in the vcf record used to assign the read to a phase.',
            action = 'store_false'
            )
    
    phasing_parser_output.add_argument(
            '-O', '--output_phased_bam',
            help = 'Use the --output_phased_bam option to output the reads submitted to phasing as a combined bam file.',
            action = 'store_false'
            )
    
    phasing_parser_output.add_argument(
            '--only_tag_output',
            help = 'Use the --only_tag_output option to output the reads submitted to phasing as a combined bam file.',
            action = 'store_false'
            )
    
    phasing_parser_output.add_argument(
            '-sep', '--ouput_phase_separated_bam',
            help = 'Use the --ouput_phase_separated_bam option to output the phased reads as individual bam files '
                   'separated according to phase.',
            action = 'store_true'
            )
    
    phasing_parser_output.add_argument(
            '-H', '--add_phasing_tag_to_output',
            help = 'Use the --add_phasing_tag_to_output option to add HP:i:1 and HP:i:2 tags to bam output.',
            action = 'store_false'
            )
    
    phasing_parser_output.add_argument(
            '-Q', '--add_phasing_quality_tag_to_output',
            help = 'Use the --add_phasing_quality_tag_to_output option to add PC:i:x tags to bam output where x is an '
                   'estimate of the accuracy of the phasing assignment in phred-scale.',
            action = 'store_false'
            )
    
    ############## Multiple sample handling/phase set options for phasing mode ##############
    phasing_parser_multiple_sample = phasing_parser.add_argument_group(
            'Sample options',
            'Phasing options for files containing multiple samples or haplotypes. By default the input files are assumed '
            'to belong to the same haplotype and from the same sample. '
            )
    
    # phasing_parser_multiple_sample.add_argument('-R', '--add_read_group_tag_to_input_reads', required = False,
    # help='Use the --add_read_group_tag_to_input_reads option to overwrite or add @RG ID:Z:x SM:Z:y DS:Z:z headers
    # and RG:Z:x tags to all input reads where x is the ID number, y is the name of the sample to which the read
    # belongs, and z is a description of the experimental sample that generated the reads. (-R x y z)', nargs = 3,
    # dest = 'add_read_group_tag_to_input_reads')
    
    phasing_parser_multiple_sample.add_argument(
            '-s', '--one_sample', required = False,
            help = 'Use the --one_sample option to phase a specific sample present in the input reads and vcf file. (-s '
                   'HG001)',
            metavar = 'sample name to exclusively phase'
            )
    
    phasing_parser_multiple_sample.add_argument(
            '--ignore_samples',
            help = 'Use the --ignore_samples option to ignore sample labels. The first sample column in the VCF will be '
                   'used and reads will not be matched using RG tags, samples, or phase sets.',
            action = 'store_true'
            )
    
    # ############## Additional methods for evaluating phasing accuracy using simulated reads  ##############
    
    # phasing_parser_simulation = phasing_parser.add_argument_group('Evaluation of phasing using simulated reads', 'Simulated reads are used to estimate the accuracy of phasing decisions and assign quality scores.')
    
    # phasing_parser_simulation.add_argument('--simulated', help='Use the --simulated option to enable extra analysis to be performed for determining correct phasing rates and selecting thresholds through iteration of phasing decisions over log likelihood thresholds 0-10. When --simulated is used, LRphase will skip phasing and process a per_read_phasing_stats.tsv results file located in the output folder specified by -o. ', action='store_true')
    
    # phasing_parser_simulation.add_argument('--simulated_bam', required = False, help = 'Path to file with phased reads to output results from simulated analyses.', dest = 'simulated_bam', metavar = 'phased output bam file')
    
    # phasing_parser_simulation.add_argument('--simulated_analysis_only', help='Use the --simulated option to enable extra analysis to be performed for determining correct phasing rates and selecting thresholds through iteration of phasing decisions over log likelihood thresholds 0-10.', action='store_true')
    
    # phasing_parser_simulation.add_argument('--simulated_phasing_stats', required = False, help = 'Path to file with phased reads to output results from simulated analyses.', dest = 'simulated_phasing_stats', metavar = 'phasing stats file')
    
    ############## Statistical and error options for phasing mode ##############
    
    phasing_parser_stats_error: _ArgumentGroup = phasing_parser.add_argument_group(
            'Statistical options for phasing model',
            'Options to modify thresholds and error parameters involved in phasing decisions.'
            )
    
    phasing_parser_stats_error.add_argument(
            '-E', '--error_rate_threshold', required = False, default = 0.05,
            help = 'error rate used for phasing decision',
            dest = 'error_rate_threshold', type = float, metavar = 'error rate threshold'
            )
    
    phasing_parser_stats_error.add_argument(
            '--error_model', required = False, default = 0,
            help = 'Use the --error_model option to choose how to estimate sequencing error rates: 0: estimate per-base '
                   'error rate as an average per read. 1: estimate per-base error rate locally around each het site. 2: '
                   'Calculate per-base error rate using base quality scores (WARNING: do not use option 2 unless you are '
                   'sure that the basecaller reported actual error rates). ',
            dest = 'error_model', type = int, metavar = 'error_model'
            )
    
    # phasing_parser_stats_error.add_argument('--read_average_error_model', help='Use the --read_average_error_model
    # option to estimate per-base error rate as an average per read.', action='store_false')
    
    phasing_parser_stats_error.add_argument(
            '--error_stats',
            help = 'Use the --error_stats option to enable extra analysis to be performed for per-base error statistics.',
            action = 'store_true'
            )
    
    phasing_parser_stats_error.add_argument(
            '--phasing_error_file_path', required = False,
            help = "Path to file with estimated error statistics from simulated analyses.",
            dest = 'phasing_error_file_path', metavar = 'phasing_error_file_path'
            )
    
    phasing_parser_stats_error.add_argument(
            '--error_stats_hets', required = False,
            default = 'simulated_reads_log_likelihood_ratio_iteration_hets_phasing_stats.tsv',
            help = "'Path to file with estimated error statistics from simulated analyses.",
            dest = 'simulated_log_likelihood_ratio_iteration_hets_file', metavar = 'error statistics hets file'
            )
    
    phasing_parser.set_defaults(func = phasing)
    
    ############## Phasability Mode Arguments ############## 
    
    phasability_parser = lrphase_subparsers.add_parser(
            'phasability',
            description = 'Tool that uses haplotype information as input and outputs predictions for how well LRphase '
                          'will perform. Can be used to evaluate phasability genome-wide or at optional regions. '
            )
    
    ############## Phasability Mode Required Arguments ##############
    
    phasability_parser_required: _ArgumentGroup = phasability_parser.add_argument_group(
            'Required', 'Required for phasability analysis'
            )
    
    phasability_parser_required.add_argument(
            '-o', '--output_directory_name', required = True,
            help = 'Name given to directory where results will be output (ex: -o GM12878_phasability)',
            dest = 'output_directory_name', metavar = 'output directory name'
            )
    
    phasability_parser_required.add_argument(
            '-v', '--vcf', required = True,
            help = 'Path to vcf file with haplotype information that will be used for phasability analysis. (Must be in '
                   '.vcf.gz format with tabix index in same folder. If .vcf file is provided, bgzip and tabix must be '
                   'installed and available on PATH because LRphase will attempt to convert it. EX: -v '
                   'GM12878_haplotype.vcf.gz)',
            dest = 'vcf_file_name', metavar = 'vcf file'
            )
    
    ############## Phasability Mode Optional Arguments ##############
    
    phasability_parser_optional = phasability_parser.add_argument_group('Optional', 'Optional for phasability mode')
    
    phasability_parser_optional.add_argument(
            '-C', '--chromosome_lengths', required = False,
            help = 'Length of each chromosome that will be included in genome wide phasability analysis (EX: -C '
                   'chr.lengths.txt)',
            dest = 'chromosome_lengths', metavar = 'Chromosome Lengths'
            )
    
    phasability_parser_optional.add_argument(
            '-L', '--log_likelihood_ratio', required = False, default = 2.0,
            help = 'Log likelihood ratio used for phasing decision', dest = 'log_likelihood_ratio', type = float,
            metavar = 'phasing score'
            )
    
    phasability_parser_optional.add_argument(
            '-l', '--read_length', required = False, default = 25000,
            help = 'Read length in bp used for phasability analysis (default = 25000)', dest = 'read_length',
            type = int,
            metavar = 'Read Length (bp)'
            )
    
    phasability_parser_optional.add_argument(
            '-i', '--intervals', required = False, default = 10000,
            help = 'Distance between intervals (bp) used for phasability analysis (default = 1000)',
            dest = 'interval_distance', type = int, metavar = 'Intervals (bp)'
            )
    
    phasability_parser_optional.add_argument(
            '-c', '--chromosome', required = False,
            help = 'LOCUS MODE: Evaluate phasability for a genomic region. Name of chromosome (EX: -c chr10)',
            dest = 'chr_locus', metavar = 'Chromosome'
            )
    
    phasability_parser_optional.add_argument(
            '-s', '--start', required = False,
            help = 'LOCUS MODE: Evaluate phasability for a genomic region. Locus start position (EX: -s 5674832)',
            dest = 'start_locus', type = int, metavar = 'Start Position'
            )
    
    phasability_parser_optional.add_argument(
            '-e', '--end', required = False,
            help = 'LOCUS MODE: Evaluate phasability for a genomic region. Locus end position (EX: -e 34256589)',
            dest = 'end_locus', type = int, metavar = 'End Position'
            )
    
    phasability_parser_optional.add_argument(
            '--locus',
            help = 'Use the --locus option to determine the phasability of a single region. Must specify the region of '
                   'interest using --chromosome, --start, end, OR -c, -s, -e, respectively. (EX: LRphase phasability '
                   '--locus --chromosome chr7 --start 10000000 --end 20000000 -v GM12878_haplotype.vcf.gz -o '
                   'locus_GM12878_phasability',
            action = 'store_true', dest = 'locus_mode'
            )
    
    phasability_parser_optional.add_argument(
            '--error_stats_hets', required = False,
            default = 'simulated_reads_log_likelihood_ratio_iteration_hets_phasing_stats.tsv',
            help = 'Path to file with estimated error statistics from simulated analyses.',
            dest = 'simulated_log_likelihood_ratio_iteration_hets_file', metavar = 'error statistics hets file'
            )
    
    phasability_parser_optional.add_argument(
            '-q', '--quiet', help = 'stdout will be muted', action = 'store_true', dest = 'quiet_mode'
            )
    
    phasability_parser.set_defaults(func = phasability)
    
    ############## error_analysis Mode Arguments ##############
    
    error_analysis_parser = lrphase_subparsers.add_parser(
            'error_analysis',
            description = 'Tool for performing error analysis of phasing reults using simulated reads and haplotype '
                          'information. '
            )
    
    ############## error_analysis Mode Required Arguments ##############
    
    error_analysis_parser_required: _ArgumentGroup = error_analysis_parser.add_argument_group(
            'Required', 'Required for error_analysis'
            )
    
    error_analysis_parser_required.add_argument(
            '-o', '--output_directory_name', required = True,
            help = 'Name given to directory where results will be output (ex: -o minion_GM12878_run3_phasing_output)',
            dest = 'output_directory_name', metavar = 'output directory name'
            )
    
    # error_analysis_parser_required.add_argument('-v', '--vcf', required = True, help = 'Path to vcf file with haplotype information that will be used for error_analysis. (Must be in .vcf.gz format with tabix index in same folder. If .vcf file is provided, bgzip and tabix must be installed and available on PATH because LRphase will attempt to convert it.  EX: -v GM12878_haplotype.vcf.gz)', dest = 'vcf_file_name', metavar = 'vcf file')
    
    #error_analysis_parser_required.add_argument('-i', required = True, help = 'Path to alignment file (.bam or .sam) of long reads that will be used for error_analysis. If either a .sam file is provided or an index is not found, .sam and .bam file will be sorted and indexed using pysam. Sorted.bam files should be in same directory as their index (.sorted.bam.bai). EX: -a data/minion_GM12878_run3.sorted.bam, -i minion_GM12878_run3.sam) Path to long read file in .fastq format that will be used for alignment and phasing (ex: -i minion_GM12878_run3.fastq)', dest = 'long_read_inputs', metavar = 'long-read input file', action = 'append', nargs = '*')
    
    # error_analysis_parser_required.add_argument('-r', '--reference', required = False, help = 'Path to reference genome sequence file. REQUIRED if -i is used to specify reads in fastq format to be aligned prior to phasing. (file types allowed: .fa, .fna, fasta. EX: -r data/reference_hg38.fna)', dest = 'reference_genome', metavar = 'reference genome')
    
    ############## Additional methods for evaluating phasing accuracy using simulated reads  ##############
    
    error_analysis_parser_simulation: _ArgumentGroup = error_analysis_parser.add_argument_group(
            'Evaluation of phasing using simulated reads',
            'Simulated reads are used to estimate the accuracy of phasing decisions and assign quality scores.'
            )
    
    # error_analysis_parser_simulation.add_argument('--simulated', help='Use the --simulated option to enable extra
    # analysis to be performed for determining correct phasing rates and selecting thresholds through iteration of
    # phasing decisions over log likelihood thresholds 0-10. When --simulated is used, LRphase will skip phasing and
    # process a per_read_phasing_stats.tsv results file located in the output folder specified by -o. ',
    # action='store_true')
    error_analysis_parser_simulation.add_argument(
            '--evaluate_phasing_stats',
            help = 'Compare the quality scores in a phased bam to error rates determined from simulated reads. All input '
                   'must be phased bam files that  -i for ath to phased with phased reads to output results from '
                   'simulated analyses.',
            action = 'store_true'
            )
    error_analysis_parser_simulation.add_argument(
            '--ignore_phase_set',
            help = 'Compare the quality scores in a phased bam to error rates determined from simulated reads. All input '
                   'must be phased bam files that  -i for ath to phased with phased reads to output results from '
                   'simulated analyses.',
            action = 'store_true'
            )
    
    # error_analysis_parser_simulation.add_argument('--evaluate_phased_bam', help = 'Compare the quality scores in a
    # phased bam to error rates determined from simulated reads. All input must be phased bam files that  -i for ath
    # to phased with phased reads to output results from simulated analyses.', action='store_true')
    # error_analysis_parser_simulation.add_argument('--simulated_bam', required = False, help = 'Path to file with
    # phased reads to output results from simulated analyses.', dest = 'simulated_bam', metavar = 'phased output bam
    # file')
    
    # error_analysis_parser_simulation.add_argument('--simulated_analysis_only', help='Use the --simulated option to
    # enable extra analysis to be performed for determining correct phasing rates and selecting thresholds through
    # iteration of phasing decisions over log likelihood thresholds 0-10.', action='store_true')
    # error_analysis_parser_simulation.add_argument('--simulated_phasing_stats', required = False, help = 'Path to
    # file with phased reads to output results from simulated analyses.', dest = 'simulated_phasing_stats',
    # metavar = 'phasing stats file')
    
    error_analysis_parser_simulation.add_argument(
            '-i', '--input_simulated', required = True,
            help = "Path to file with phased reads to output results from simulated analyses.",
            dest = 'input_simulated',
            metavar = 'phasing stats file', action = 'append', nargs = '*'
            )
    error_analysis_parser_simulation.add_argument(
            '-s', '--sample_output', required = False,
            help = "Path to file with phased reads to output results from simulated analyses.", dest = 'sample_output',
            metavar = 'sample to analyze'
            )
    error_analysis_parser_simulation.add_argument(
            '-p', '--phase_set_output', required = False, default = 'NA',
            help = 'Path to file with phased reads to output results from simulated analyses.',
            dest = 'phase_set_output',
            metavar = "phase set to analyze"
            )
    error_analysis_parser_simulation.add_argument(
            '-l', '--log_likelihood_ratio_interval', required = False, default = .5,
            help = 'Path to file with phased reads to output results from simulated analyses.',
            dest = 'log_likelihood_ratio_interval', metavar = 'phase set to analyze'
            )
    error_analysis_parser_simulation.add_argument(
            '-L', '--log_likelihood_ratio_threshold', required = False, default = 2.0,
            help = 'Path to file with phased reads to output results from simulated analyses.',
            dest = 'log_likelihood_ratio_threshold', metavar = 'phase set to analyze'
            )
    error_analysis_parser_simulation.add_argument(
            '-E', '--error_rate_threshold', required = False, default = 0.05,
            help = 'error rate used for phasing decision',
            dest = 'error_rate_threshold', type = float, metavar = 'error rate threshold'
            )
    
    error_analysis_parser_simulation.add_argument(
            '--phasing_error_file_path', required = False,
            help = 'Path to file with estimated error statistics from simulated analyses.',
            dest = 'phasing_error_file_path', metavar = 'phasing_error_file_path'
            )
    
    error_analysis_parser.set_defaults(func = error_analysis)
    
    ############## Parse arguments ##############
    
    args = lrphase_parser.parse_args()
    
    args.func(args)
    
    return args


def main():
    
    args: Namespace = getArgs()


if __name__ == '__main__':
    main()
