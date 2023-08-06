# coding=utf-8
import os
import subprocess
import time

import pyliftover
import pysam
from pysam import bcftools
from pysam import faidx
from typing import Tuple, List


#import pysam.bcftools
#import pysam.samtools


def simulate_reads_pbsim2(
        reference_sequence: str, path_to_pbsim: str = 'pbsim', depth: int = 1,
        simulation_mode: str = 'pbsim2/data/R103.model',
        difference_ratio: str = '23:31:46', length_mean: int = 20000,
        length_max: int = 1000000, length_min: int = 100,
        length_sd: int = 15000, accuracy_min: float = 0.01,
        accuracy_max: float = 1.00, accuracy_mean: float = 0.80,
        prefix: str = None, id_prefix: str = 'S', output_directory: str = None, sample: str = None,
        haplotype: int = None
        ) -> str:
    """
    Args:
        reference_sequence (str):
            reference sequence template to simulate reads from
        path_to_pbsim (str):
            if pbsim2 is not installed to the PATH as pbsim then use this to set its absolute or relative path
        depth (int):
            the depth of coverage that will be simulated
        simulation_mode: 
        difference_ratio: 
        length_mean: 
        length_min: 
        length_max: 
        length_sd: 
        accuracy_min: 
        accuracy_max: 
        accuracy_mean: 
        prefix: 
        id_prefix: 
        output_directory: 
        sample: 
        haplotype: 

    Returns:
        object: 
    
    """
    
    if output_directory is None:
        output_directory: str = 'simulated'
    
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    
    if not sample is None and not haplotype is None:
        #id_prefix = str(sample)+'__'+str(haplotype)+'__'

        if prefix is None:
            prefix = str(output_directory) + '/' + str(sample) + '__' + str(haplotype) + '__' + 'pbsim2_simulated_' +\
                     os.path.basename(reference_sequence).split('.')[0] + '_' + str(time.localtime()[0]) + '_' + str(
                    time.localtime()[1]
                    ) + '_' + str(time.localtime()[2]) + '_' + str(time.localtime()[3]) + 'hr_' + str(
                    time.localtime()[4]
                    ) + 'min_' + str(time.localtime()[5]) + 'sec'
        else:
            prefix = '{0}/{1}__{2}__{3}'.format(str(output_directory), str(sample), str(haplotype), str(prefix))
    
    # if prefix is None:
    # if prefix is None:
    # prefix = str(output_directory) + '/pbsim2_simulated'
    # else:
    # prefix = str(output_directory) + '/' + str(prefix)
    
    if str(simulation_mode).lower().endswith(".fastq"):
        mode1 = '--sample-fastq'
        mode2 = simulation_mode
    
    elif str(simulation_mode).lower().endswith('.model'):
        mode1 = '--hmm_model'
        mode2 = simulation_mode
    
    if not reference_sequence:
        print(
                f'no reference genome was provided for pbsim2 simulation. Please specify reference_genome_path to be '
                f'simulated '
                )
        return
    print('################ Beginning Read Simulation ################')
    
    start_process_time = time.time()
    
    reference_genome_path = os.path.abspath(reference_sequence)
    reference_genome_index_path = str(reference_genome_path) + '.fai'
    if not os.path.isfile(reference_genome_index_path):
        faidx(reference_genome_path)
        #subprocess.run(['samtools', 'faidx', reference_genome_path], check=True)
    
    subprocess.run(
            [f'--depth',
             str(path_to_pbsim), str(depth),
             str(mode1), str(mode2),
             f'--difference-ratio', str(difference_ratio),
             f'--length-mean', str(length_mean),
             f'--length-min', str(length_min),
             f'--length-max', str(length_max),
             f'--length-sd', str(length_sd),
             f'--accuracy-mean', str(accuracy_mean),
             f'--accuracy-min', str(accuracy_min),
             f'--prefix', '--accuracy-max',
             str(accuracy_max), str(prefix),
             '--id-prefix', str(id_prefix),
             str(reference_genome_path)], check = True
            )
    
    end_process_time = time.time()
    total_process_time = end_process_time - start_process_time
    
    print(f'Simulation finished in {total_process_time:.2f} seconds', '\n')
    sample_hap_to_true_alignment_dict = {}
    pbsim2_pbsim2fq_output = str(prefix) + '_pbsim2fq.fastq'
    subprocess.run(
            ["paftools.js pbsim2fq %s %s*.maf >> %s" % (
                    str(reference_genome_index_path), str(prefix), str(pbsim2_pbsim2fq_output))], shell = True
            )
    
    #subprocess.run(['rm %s/*.maf' % os.path.dirname(pbsim2_pbsim2fq_output)], shell=True)
    #subprocess.run(['rm %s/*.ref' % os.path.dirname(pbsim2_pbsim2fq_output)], shell=True)
    
    combined_simulated_long_reads_fastq_path = str(
            os.path.dirname(pbsim2_pbsim2fq_output)
            ) + '/combined_simulated_long_reads.fastq'
    final_combined_simulated_long_reads_fastq_path: str = '{0}/{1}.fastq'.format(
            str(
                    os.path.dirname(combined_simulated_long_reads_fastq_path)
                    ), str(os.path.splitext(os.path.basename(reference_sequence))[0])
            )
    #output_fastq = str(final_combined_simulated_long_reads_fastq_path) + '.gz'
    
    for file in os.listdir(os.path.dirname(pbsim2_pbsim2fq_output)):
        file = str(os.path.dirname(pbsim2_pbsim2fq_output)) + '/' + str(file)
        if str(file).lower().endswith('pbsim2fq.fastq') or str(file).lower().endswith('pbsim2fq.fastq.gz'):
            continue
        elif str(file).lower().endswith('.fastq'):
            with open(combined_simulated_long_reads_fastq_path, 'w') as outfile:
                with open(file, 'r') as infile:
                    outfile.write(infile.read())
            os.remove(file)
    
    for read in pysam.FastxFile(pbsim2_pbsim2fq_output):
        sample_hap_to_true_alignment_dict[str(read.name.split('!')[0])] = read.name
    
    os.remove(pbsim2_pbsim2fq_output)
    
    with pysam.FastxFile(combined_simulated_long_reads_fastq_path) as in_pysam_fastx:
        with open(final_combined_simulated_long_reads_fastq_path, mode = 'w') as out_pysam_fastx:
            for read in in_pysam_fastx:
                try:
                    read.name = str(sample) + '__' + str(haplotype) + '__' + str(
                            sample_hap_to_true_alignment_dict[read.name]
                            )
                    out_pysam_fastx.write(str(read) + '\n')
                except Exception as e:
                    print(e)
    
    os.remove(combined_simulated_long_reads_fastq_path)
    #final_combined_simulated_long_reads_fastq_path
    return final_combined_simulated_long_reads_fastq_path


def convert_coordinates(
        haplotype: int, sample: str, contig: str, position: int, reference_sequence: str,
        reference_liftover_converters = None, chain_file = None
        ):
    """

    Args:
        haplotype (int):
        sample (str):
        contig (str):
        position (int):
        reference_sequence (str):
        reference_liftover_converters: 
        chain_file: 

    Returns:
        object: 

    """
    if reference_liftover_converters is None:
        reference_liftover_converters = {}
    
    if reference_sequence in reference_liftover_converters:
        if sample in reference_liftover_converters[reference_sequence]:
            if str(haplotype) in reference_liftover_converters[reference_sequence][sample]:
                return reference_liftover_converters[reference_sequence][sample][str(haplotype)].convert_coordinates(
                        contig, position
                        )
        
        elif chain_file is not None:
            if os.path.isfile(chain_file):
                reference_liftover_converters[reference_sequence][sample] = {}
                reference_liftover_converters[reference_sequence][sample][str(haplotype)] = pyliftover.LiftOver(
                        chain_file
                        )
                return reference_liftover_converters[reference_sequence][sample][str(haplotype)].convert_coordinates(
                        contig, position
                        )
    
    elif chain_file is not None:
        if os.path.isfile(chain_file):
            reference_liftover_converters[reference_sequence] = {}
            reference_liftover_converters[reference_sequence][sample] = {}
            reference_liftover_converters[reference_sequence][sample][str(haplotype)] = pyliftover.LiftOver(chain_file)
            return reference_liftover_converters[reference_sequence][sample][str(haplotype)].convert_coordinates(
                    contig, position
                    )


def generate_haplotype_specific_fasta(
        haplotype: int, sample: str, input_reference_sequence_path: str, haplotype_vcf: str,
        output_reference_sequence_path: str = None,
        chain_file_path: str = None
        ) -> Tuple(str, str):
    """

    Args:
        haplotype:
        sample:
        input_reference_sequence_path:
        haplotype_vcf:
        output_reference_sequence_path:
        chain_file_path:

    Returns:

    """
    print('################ Generating Haplotype Reference Sequence ################')
    input_reference_sequence_path = os.path.abspath(input_reference_sequence_path)
    input_reference_sequence_index_path: str = str(input_reference_sequence_path) + '.fai'
    
    if output_reference_sequence_path is None:
        output_reference_sequence_path: str = str(os.path.splitext(input_reference_sequence_path)[0]) + '_hap' + str(
                haplotype
                ) + '_' + str(sample) + '.fa'
        output_reference_sequence_path_index = str(os.path.splitext(input_reference_sequence_path)[0]) + '_hap' + str(
                haplotype
                ) + '_' + str(sample) + '.fa.fai'
    
    if chain_file_path is None:
        chain_file_path = str(os.path.splitext(input_reference_sequence_path)[0]) + '_hap' + str(haplotype) + '_' + str(
                sample
                ) + '.chain'
    
    fasta_output = bcftools.consensus(
            '-H', str(haplotype), '-s', str(sample), '-c', str(chain_file_path), '-f',
            str(input_reference_sequence_path),
            str(haplotype_vcf)
            )
    with open(output_reference_sequence_path, 'w') as output_fasta:
        output_fasta.write(fasta_output)
    
    return output_reference_sequence_path, chain_file_path


def index_fasta_file(fasta_file_path: str) -> str:
    """

    Args:
        fasta_file_path: 

    Returns:

    """
    fasta_file_path = os.path.abspath(fasta_file_path)
    
    if fasta_file_path.endswith('.fa') or fasta_file_path.endswith('fa.gz'):
        faidx(fasta_file_path)
        return os.path.abspath(fasta_file_path)
    
    elif fasta_file_path.endswith('fa.gz'):
        os.rename(fasta_file_path, '{0}.fa.gz'.format(str(os.splitext(fasta_file_path)[0])))
        faidx(str(os.splitext(fasta_file_path)[0]) + '.fa.gz')
        return str(os.splitext(fasta_file_path)[0]) + '.fa.gz'
    
    else:
        os.rename(fasta_file_path, str(os.splitext(fasta_file_path)[0]) + '.fa')
        faidx(str(os.splitext(fasta_file_path)[0]) + '.fa')
        return str(os.splitext(fasta_file_path)[0]) + '.fa'


def create_fasta_file(
        input_fasta_file_path: str, output_fasta_file_path: str = None, regions: List[str] = None, only_autosomal:
        bool = False
        ) -> str:
    f"""

    Args:
        input_fasta_file_path: 
        only_autosomal (object): 
        regions:
            List of regions and/or contigs ie: ['chr1:10000000:60000000','chr2']
        output_fasta_file_path (object): 
    """
    autosomal_reference_names = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10',
                                 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19',
                                 'chr20', 'chr21', 'chr22']
    input_fasta_file_path = os.path.abspath(input_fasta_file_path)
    if output_fasta_file_path is None:
        if only_autosomal:
            output_fasta_file_path = str(
                    os.path.splitext(input_fasta_file_path)[0]
                    ) + 'output_regions_only_autosomal.fa'
        else:
            output_fasta_file_path = str(os.path.splitext(input_fasta_file_path)[0]) + 'output_regions.fa'
    
    if regions is None:
        regions_file = str(os.path.splitext(output_fasta_file_path)[0]) + '_regions.txt'
        all_regions = pysam.FastaFile(input_fasta_file_path).references
        if only_autosomal:
            regions_list = [region for region in all_regions if region in autosomal_reference_names]
        else:
            regions_list = all_regions
    
    elif isinstance(regions, list):
        regions_file: str = str(os.splitext(output_fasta_file_path)[0]) + '_regions.txt'
        if only_autosomal:
            regions_list = [region for region in regions if region in autosomal_reference_names]
        else:
            regions_list = regions
    
    if regions is not None:
        if os.path.isfile(regions):
            regions_file = regions
    else:
        with open(regions_file, 'w') as file:
            for region in regions_list:
                file.write(str(region) + '\n')
    
    faidx(input_fasta_file_path, '-r', regions_file, '-o', output_fasta_file_path)
    
    return output_fasta_file_path


def true_alignment_match(
        aligned_segment: pysam.AlignedSegment, needs_liftover: bool = False, contig: str = None, ref_start: int = None,
        ref_end: int = None, strand: str = None, tag_read: bool = False, only_output_match_label: bool = False, only_output_overlap: bool = False,
        true_reference_sequence_path: str = None, aligned_reference_sequence_path: str = None, liftover_converter = None,
        chain_file_path: str = None, sample: str = None, haplotype: int = None, reference_liftover_converters = None
        ) -> object:
    """

    Args:
        chain_file_path (object): 
        aligned_segment: 
        sample: 
        tag_read (object): 
    """
    overlap = 0
    match_label = 'non_match'
    
    if contig is None or ref_start is None or ref_end is None or strand is None:
        contig, ref_start, ref_end, strand = true_alignment_coordinates(
                aligned_segment, tag_read = tag_read, contig = contig, ref_start = ref_start, ref_end = ref_end,
                strand = strand
                )
    
    if needs_liftover:
        if liftover_converter is not None:
            liftover_converter = liftover_converter
    
        elif reference_liftover_converters is not None:
            if aligned_reference_sequence_path is not None:
                if aligned_reference_sequence_path in reference_liftover_converters:
                    if sample in reference_liftover_converters[aligned_reference_sequence_path]:
                        if str(haplotype) in reference_liftover_converters[aligned_reference_sequence_path][sample]:
                            liftover_converter = reference_liftover_converters[aligned_reference_sequence_path][sample][
                                str(haplotype)]
    
        elif chain_file_path is not None:
            if os.path.isfile(chain_file_path):
                liftover_converter = pyliftover.Liftover(chain_file_path)
    
        else:
            print('could not liftover')
            return
    
        contig = liftover_converter.convert_coordinate(contig, ref_start)[0][0]
        ref_start = liftover_converter.convert_coordinate(contig, ref_start)[0][1]
        ref_end = liftover_converter.convert_coordinate(contig, ref_end)[0][1]
        strand = liftover_converter.convert_coordinate(contig, ref_start)[0][2]
    
    if aligned_segment.reference_name == contig:
        match_label = 'ref_match'
        if int(ref_start) <= int(aligned_segment.reference_start) <= int(ref_end):
            match_label = 'mapping_match'
            if int(aligned_segment.reference_end) >= int(ref_end):
                overlap = int(ref_end) - int(aligned_segment.reference_start)
            else:
                overlap = int(aligned_segment.reference_end) - int(aligned_segment.reference_start)
        elif int(ref_start) <= int(aligned_segment.reference_end) <= int(ref_end):
            match_label = 'mapping_match'
            if int(ref_start) >= int(aligned_segment.reference_start):
                overlap = int(aligned_segment.reference_end) - int(ref_start)
            else:
                overlap = int(aligned_segment.reference_end) - int(aligned_segment.reference_start)
        elif (
                int(ref_start) - (int(ref_start) * 0.1)) <= aligned_segment.reference_start <= (
                int(ref_end) + (int(ref_end) * 0.1)):
            match_label = 'within_10percent'
    
    if tag_read:
        aligned_segment.set_tag(
                tag = 'ov', value = str(overlap / (int(ref_end) - int(ref_start))), value_type = 'Z', replace = True
                )
        aligned_segment.set_tag(
                tag = 'OV', value = str(overlap / (aligned_segment.query_alignment_length)), value_type = 'Z',
                replace = True
                )
        aligned_segment.set_tag(tag = 'ml', value = str(match_label), value_type = 'Z', replace = True)
    
    if only_output_match_label:
        return match_label
    
    elif only_output_overlap:
        return overlap
    
    else:
        return match_label, overlap


def true_alignment_coordinates(
        aligned_segment: pysam.AlignedSegment, tag_read: bool = False, contig: str = None, ref_start: int = None,
        ref_end: int = None, strand: str = None
        ) -> Tuple(str,int,int,str):
    """

    Args:
        aligned_segment: 
        tag_read: 
        contig: 
        ref_start: 
        ref_end: 
        strand: 

    Returns:

    """
    if '!' in str(aligned_segment.query_name):
        _read_name, _contig, _ref_start, _ref_end, _strand = aligned_segment.query_name.split('!')
        if contig is None:
            contig = _contig
        if ref_start is None:
            ref_start = _ref_start
        if ref_end is None:
            ref_end = _ref_end
        if strand is None:
            strand = _strand
    
    if tag_read:
        aligned_segment.set_tag(tag = 'st', value = str(ref_start), value_type = 'Z', replace = True)
        aligned_segment.set_tag(tag = 'lo', value = str(contig), value_type = 'Z', replace = True)
        aligned_segment.set_tag(tag = 'en', value = str(ref_end), value_type = 'Z', replace = True)
        aligned_segment.set_tag(tag = 'sd', value = str(strand), value_type = 'Z', replace = True)
    
    return contig, ref_start, ref_end, strand


def alignment_type(aligned_segment: pysam.AlignedSegment, tag_read: bool = False) -> str:
    """

    Args:
        aligned_segment:
        tag_read:

    Returns:

    """
    alignment_label: str = 'None'
    if aligned_segment.is_unmapped:
        alignment_label = 'unmapped'
    elif aligned_segment.is_secondary:
        alignment_label = 'secondary'
    elif aligned_segment.is_supplementary:
        alignment_label = 'supplementary'
    else:
        alignment_label = 'mapped'
    if tag_read:
        aligned_segment.set_tag(tag = 'al', value = str(alignment_label), value_type = 'Z', replace = True)
    
    return alignment_label
