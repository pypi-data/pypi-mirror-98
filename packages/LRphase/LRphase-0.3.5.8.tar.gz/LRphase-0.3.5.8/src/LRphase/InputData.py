# coding=utf-8
import os
import random
import subprocess
import time
from collections import defaultdict
from datetime import date
from shutil import copyfileobj
from typing import Any, Dict, Tuple

import pysam
import requests
from LRphase import PhasableSample
from pysam import VariantFile


def _prepare_output_directory(output_directory_path: str) -> object:#Optional[str]:
    """

    Args:
        output_directory_path (object): 
    """
    print('############## Preparing output_directory ##############')
    if os.path.isfile(output_directory_path):
        print(
                f'Output directory exists as a file. Use -o to specify the name to be given to the output folder. May '
                f'also provide a relative path with a name to create output directory in a different location (EX: -o '
                f'path/to/name). Do not specify a file. '
                )
        return
    elif os.path.exists(output_directory_path):
        print(
                '%s already exists, WARNING: New results will overwrite old files' % os.path.abspath(
                        output_directory_path
                        ), '\n'
                )
    elif not os.path.exists(output_directory_path):
        os.mkdir(output_directory_path)
        print(f"%s created" % os.path.abspath(output_directory_path), '\n')
    output_directory = os.path.abspath(output_directory_path)
    return output_directory


def _prepare_summary_file(output_directory):
    print('############## Preparing summary_file ##############')
    
    summary_file_path = os.path.abspath('%s/%s' % (output_directory, 'summary.txt'))
    if os.path.exists(summary_file_path):
        print(
                '%s already exists, WARNING: New results will overwrite old files' % os.path.abspath(summary_file_path),
                '\n'
                )
    elif not os.path.exists(summary_file_path):
        print('%s created' % os.path.abspath(summary_file_path), '\n')
    summary_file = open(summary_file_path, 'w')
    summary_file.write('Start date: %s\n' % str(date.today()))
    start_time = time.time()
    print('%s created' % summary_file_path, '\n')
    
    return summary_file_path


def _pair_sample_with_vcf(sample, sample_to_vcf_file_dict, ignore_phase_sets):
    if str(sample) in sample_to_vcf_file_dict.keys():
        for vcf_file_path in sample_to_vcf_file_dict[str(sample)].items():
            if ignore_phase_sets:
                return vcf_file_path[0], True
            else:
                return vcf_file_path[0], vcf_file_path[1]
    else:
        return


def _sample_to_alignment_files(sample_to_vcf_file_dict: dict, RG_ID_dict: dict) -> object:
    sample_to_alignment_files = {}
    for sample in sample_to_vcf_file_dict:
        sample_to_alignment_files[sample] = {}
        for file in RG_ID_dict.keys():
            if len([file for key in RG_ID_dict[file].keys() if RG_ID_dict[file][key]['SM'] == sample]) > 0:
                for pair in [{
                        alignment_file_path:any(
                                [RG_ID_dict[alignment_file_path][ID]['RG_tags'] for ID in
                                 RG_ID_dict[alignment_file_path].keys()]
                                )
                        } for alignment_file_path in RG_ID_dict.keys() if any(
                        [RG_ID_dict[alignment_file_path][ID]['SM'] == sample for ID in
                         RG_ID_dict[alignment_file_path].keys()]
                        )]:
                    sample_to_alignment_files[sample][list(pair.keys())[0]] = list(pair.values())[0]
    return sample_to_alignment_files


def _align_long_reads_fastq(long_reads_fastq_path, reference_sequence_input, output_directory):
    """
    Align specified reads file to reference genome via minimap2.
    """
    if not reference_sequence_input:
        print('no reference genome was provided for', long_reads_fastq_path, '. This file will be skipped.')
        return
    
    print('################ Beginning Sequence Alignment ################')
    
    start_process_time = time.time()
    reference_sequence_input_path = os.path.abspath(reference_sequence_input)
    if str(long_reads_fastq_path).lower().endswith('.fastq'):
        sam_alignment_path = os.path.abspath(
                '%s/%s%s' % (
                        output_directory, os.path.splitext(os.path.basename(long_reads_fastq_path))[0],
                        '_alignment.sam')
                )
    elif str(long_reads_fastq_path).lower().endswith('fastq.gz'):
        sam_alignment_path = os.path.abspath(
                '%s/%s%s' % (
                        output_directory,
                        os.path.splitext(os.path.splitext(os.path.basename(long_reads_fastq_path))[0])[0],
                        '_alignment.sam')
                )
    
    # if subprocess.getstatusoutput(['minimap2 -ax map-ont'+'
    # /home/ubuntu/testing_LRphase/simtest6/reference_sequences/hg38/hg38output_regions_only_autosomal.fa '+
    # '/home/ubuntu/testing_LRphase/simtest6/simulated_reads/hg38output_regions_only_autosomal_hap1_HG001.fastq '+'-o
    # '+'a.sam'])[0] != 0: print('minimap2 failed to run. Installing minimap2 from source...') import getpass
    # password = getpass.getpass() os.system('echo %s | %s' % (password, "sudo -S rm -r minimap2")) subprocess.run([
    # 'git','clone','https://github.com/lh3/minimap2']) os.chdir('minimap2/') subprocess.run('make') os.system('echo
    # %s | %s' % (password, "sudo -S install -p minimap2/minimap2 /usr/local/bin"))
    subprocess.run(
            ['minimap2', '-ax', 'map-ont', '-Y', '-L', '--secondary=no', '--MD', reference_sequence_input_path,
             long_reads_fastq_path, '-o', sam_alignment_path], check = True
            )
    
    # try:
    
    # # '-R', '@RG\\tID:'+str(ID)+'\\tSM:'+str(sample)+'\\tDS:'+str(sample_description), '-a' = creates aligned
    # # SAM file '-x' to choose a preset (map-ont in this case): 'map-ont' Slightly more sensitive for Oxford
    # # Nanopore to reference mapping (-k15). For PacBio reads, HPC minimizers consistently leads to faster
    # # performance and more sensitive results in comparison to normal minimizers. For Oxford Nanopore data,
    # # normal minimizers are better, though not much. The effectiveness of HPC is determined by the sequencing
    # # error mode. '-L' option is used when working with ultra-long nanopore reads to account for CIGAR
    # # strings > 65,535 characters '--secondary=no' Do not output secondary alignments '--MD' Output the MD
    # # tag (see the SAM spec). '-R', '@RG\\tID:'str(ID)'\\tSM:'str(sample)'\\tDS:'str(sample_description) Read
    # # group information '-o' FILE Output alignments to FILE [stdout].
    # except Exception as e:
    # print('Error occurred when minimap2 was run. minimap2 must be installed on PATH for LRphase to continue. '
    # 'Please check minimap2 installation or provide an alignment file using the -a option. Error: %s' % e)
    # return
    
    end_process_time = time.time()
    total_process_time = end_process_time - start_process_time
    
    print(f'Alignment finished in {total_process_time:.2f} seconds', '\n')
    
    # summary_file(output_directory, time.time()-start_process_time, inspect.stack()[0][3], sam_alignment_path)
    
    return sam_alignment_path


def _sort_and_index_alignment_file(long_reads_alignment_path, output_directory: object):
    start_process_time = time.time()
    
    sorted_bam_file_path = os.path.abspath(
            '%s/%s%s' % (
                    output_directory, os.path.splitext(os.path.basename(long_reads_alignment_path))[0],
                    '_sorted.bam')
            )
    print('############## Sorting and indexing bam file ##############')
    pysam.sort('-O', 'BAM', long_reads_alignment_path, '-o', sorted_bam_file_path)
    # try: subprocess.run(['samtools sort -O BAM -o %s %s' % ( sorted_bam_file_path, long_reads_alignment_path)],
    # shell=True) # pysam.sort('-l','9','-m','1500M','-@','4','-O', 'BAM', long_reads_alignment_path, '-o',
    # sorted_bam_file_path, catch_stdout=False) except Exception as e: print(e,'Error occurred when using pysam.sort
    # with 8 threads on %s. Trying 0 extra threads now.' % long_reads_alignment_path) subprocess.run(['samtools sort
    # -O BAM -o %s %s' % (sorted_bam_file_path, long_reads_alignment_path)], shell=True) # pysam.sort('-O', 'bam',
    # long_reads_alignment_path, '-o', sorted_bam_file_path, catch_stdout=False)
    
    print('Created %s' % sorted_bam_file_path)
    pysam.index(sorted_bam_file_path)
    print('Created %s.bai' % sorted_bam_file_path)
    os.remove(long_reads_alignment_path)
    end_process_time = time.time()
    total_process_time = end_process_time - start_process_time
    
    print(f'Sorting and indexing finished in {total_process_time:.2f} seconds', '\n')
    # summary_file(output_directory, time.time()-start_process_time, inspect.stack()[0][3],
    # [sorted_bam_file_path, 'Created %s.bai' % sorted_bam_file_path])
    return sorted_bam_file_path


def _prepare_alignment(output_directory: str, long_reads_alignment_path: str) -> str:
    start_process_time = time.time()
    long_read_file_pysam = pysam.AlignmentFile(long_reads_alignment_path)
    if long_read_file_pysam.format == 'BAM':
        if long_read_file_pysam.has_index():
            sorted_bam_file_path = os.path.abspath(long_reads_alignment_path)
            print('%s is a valid alignment file with an index.' % long_reads_alignment_path)
        elif not long_read_file_pysam.has_index():
            print(
                    '%s is a .bam file but the index cannot be found. Sorting and indexing bam file.' % long_reads_alignment_path
                    )
            sorted_bam_file_path = _sort_and_index_alignment_file(long_reads_alignment_path, output_directory)
            # subprocess.run(['rm %s' % long_reads_alignment_path],shell=True)
    elif long_read_file_pysam.format == 'SAM':
        print(
                '%s is a .sam file. Converting to binary (.bam), sorting, and indexing bam file.' % long_reads_alignment_path
                )
        sorted_bam_file_path = _sort_and_index_alignment_file(long_reads_alignment_path, output_directory)
        # subprocess.run(['rm %s' % long_reads_alignment_path],shell=True)
    else:
        print(
                "Error: Pysam does not recognize %s as being in SAM or BAM format. If aligned reads are provided as "
                "input they must be in proper .sam or .bam format." % long_reads_alignment_path
                )
        return
        # summary_file(self.output_directory, time.time()-start_process_time, inspect.stack()[0][3],
    # sorted_bam_file_path)
    return sorted_bam_file_path


def _unique_RG_IDs_from_RG_tags(RG_ID_dict: dict, unique_RG_IDs: dict, alignment_file_path: str) -> object:
    """

    Args:
        RG_ID_dict (dict):
        unique_RG_IDs (dict):
        alignment_file_path (str):
    """
    with pysam.AlignmentFile(alignment_file_path, 'rb') as bam_file:
        RG_tags = bam_file.header.get('RG')
    if RG_tags is None:
        RG_ID_dict[str(alignment_file_path)] = 'No RG tags'
    else:
        RG_ID_dict[str(alignment_file_path)] = {}
        for RG_tag in RG_tags:
            RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])] = {}
            RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])]['DS'] = str(RG_tag['DS'])
            RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])]['SM'] = str(RG_tag['SM'])
            RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])]['RG_tags'] = True
            if str(RG_tag['ID']) in list(unique_RG_IDs):
                if unique_RG_IDs[str(RG_tag['ID'])]['DS'] == str(RG_tag['DS']) and unique_RG_IDs[str(RG_tag['ID'])][
                    'SM'] == str(RG_tag['SM']):
                    RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])]['outputID'] = str(RG_tag['ID'])
                else:
                    not_unique = True
                    i = 0
                    while not_unique:
                        newID: str = str(RG_tag['ID']) + '_' + str(i)
                        if str(newID) not in list(unique_RG_IDs):
                            RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])]['outputID'] = str(newID)
                            unique_RG_IDs[str(newID)] = {}
                            unique_RG_IDs[str(newID)]['DS'] = str(RG_tag['DS'])
                            unique_RG_IDs[str(newID)]['SM'] = str(RG_tag['SM'])
                            not_unique = False
                        i += 1
            else:
                RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])]['outputID'] = str(RG_tag['ID'])
                unique_RG_IDs[str(RG_tag['ID'])] = {}
                unique_RG_IDs[str(RG_tag['ID'])]['DS'] = str(RG_tag['DS'])
                unique_RG_IDs[str(RG_tag['ID'])]['SM'] = str(RG_tag['SM'])
    return RG_ID_dict, unique_RG_IDs


def _extract_RG_info_from_long_read_input(long_read_input: List[str]) -> tuple[
    Union[Union[str, bytes], Any], object, Optional[Any], Optional[Any], Optional[Any]]:
    """

    Returns:
        object:
    """
    long_read_input_path = os.path.abspath(long_read_input[0])
    if len(long_read_input) == 1:
        input_ID = None
        input_sample = None
        input_sample_description = None
        input_reference_sequence_input = None
    elif len(long_read_input) == 2:
        input_ID = long_read_input[1]
        input_sample = None
        input_sample_description = None
        input_reference_sequence_input = None
    elif len(long_read_input) == 3:
        input_ID = long_read_input[1]
        input_sample = long_read_input[2]
        input_sample_description = None
        input_reference_sequence_input = None
    elif len(long_read_input) == 4:
        input_ID = long_read_input[1]
        input_sample = long_read_input[2]
        input_sample_description = long_read_input[3]
        input_reference_sequence_input = None
    elif len(long_read_input) >= 5:
        input_ID: object = long_read_input[1]
        input_sample = long_read_input[2]
        input_sample_description = long_read_input[3]
        input_reference_sequence_input = long_read_input[4]
    return long_read_input_path, input_ID, input_sample, input_sample_description, input_reference_sequence_input


def _sample_to_vcf_file_dict(vcf_file_paths):
    sample_to_vcf_file_dict = {}
    for vcf_file_path in vcf_file_paths:
        vcf_file = pysam.VariantFile(list(vcf_file_path.keys())[0])
        for sample in vcf_file.header.samples:
            sample_to_vcf_file_dict[str(sample)] = vcf_file_path
    return sample_to_vcf_file_dict


def _compile_read_groups(
        alignment_file_path, sample, ID, sample_description, RG_ID_dict, unique_RG_IDs, ignore_samples
        ):
    if ignore_samples:
        RG_ID_dict[str(alignment_file_path)] = 'ignore_samples'
    else:
        with pysam.AlignmentFile(alignment_file_path, 'rb') as bam_file:
            RG_tags = bam_file.header.get('RG')
        if sample is not None:
            RG_ID_dict[str(alignment_file_path)] = {}
            if ID is not None:
                RG_ID_dict[str(alignment_file_path)][str(ID)] = {}
                RG_ID_dict[str(alignment_file_path)][str(ID)]['SM'] = str(sample)
                RG_ID_dict[str(alignment_file_path)][str(ID)]['outputID'] = str(ID)
                RG_ID_dict[str(alignment_file_path)][str(ID)]['RG_tags'] = False
                if sample_description is not None:
                    RG_ID_dict[str(alignment_file_path)][str(ID)]['DS'] = str(sample_description)
                else:
                    RG_ID_dict[str(alignment_file_path)][str(ID)]['DS'] = str(
                            'LRphase_input_file_' + str(alignment_file_path)
                            )
            else:
                ID = '0' + str(random.randint(1, 10000))
                RG_ID_dict[str(alignment_file_path)][str(ID)] = {}
                RG_ID_dict[str(alignment_file_path)][str(ID)]['SM'] = str(sample)
                RG_ID_dict[str(alignment_file_path)][str(ID)]['outputID'] = str(ID)
                RG_ID_dict[str(alignment_file_path)][str(ID)]['RG_tags'] = False
                if sample_description is not None:
                    RG_ID_dict[str(alignment_file_path)][str(ID)]['DS'] = str(sample_description)
                else:
                    RG_ID_dict[str(alignment_file_path)][str(ID)]['DS'] = str(
                            'LRphase_input_file_' + str(alignment_file_path)
                            )
            if str(ID) not in unique_RG_IDs:
                unique_RG_IDs[str(ID)] = {}
                unique_RG_IDs[str(ID)]['DS'] = str(sample_description)
                unique_RG_IDs[str(ID)]['SM'] = str(sample)
        elif RG_tags is not None:
            RG_ID_dict, unique_RG_IDs = _unique_RG_IDs_from_RG_tags(
                    RG_ID_dict, unique_RG_IDs, alignment_file_path
                    )
        else:
            print(
                    str(
                            alignment_file_path
                            ) + "Has No RG tags and was not input with sample information. Reads in this file will not be "
                                "processed. Either re-input this read file with sample information or resubmit with "
                                "ignore_samples option. "
                    )
    return RG_ID_dict, unique_RG_IDs


class InputData:
    """
    sample_to_RG_header: defaultdict[Any, list]
    sample_to_PG_header: defaultdict[Any, list]
    unique_RG_IDs: Dict[Any, Any]
    """
    output_directory: object
    try:
        import urls
        urls_found = True
    except:
        print('Could not find import urls from data. Data will not be able to downloaded from example web sources.')
        urls_found = False
    
    def __init__(
            self, output_directory_path: str = None, vcf_file_input: str = None, long_read_input: object = None,
            reference_sequence_input: str = None, sample: str = None, ID: str = None,
            sample_description: str = None,
            ignore_phase_sets: bool = None, ignore_samples: bool = None, download_from_urls: bool = False,
            reference_sequence_input_assembly: str = None
            ) -> object:
        """

        Returns:
            object: 
        """
        if output_directory_path is not None:
            self.output_directory = _prepare_output_directory(output_directory_path)
        else:
            self.output_directory = _prepare_output_directory(
                    'LRphase_output_' + str(time.localtime()[0]) + '-' + str(time.localtime()[1]) + '-' + str(
                            time.localtime()[2]
                            ) + '_' + str(time.localtime()[3]) + 'hr_' + str(time.localtime()[4]) + 'min_' + str(
                            time.localtime()[5]
                            ) + 'sec'
                    )
        
        _prepare_output_directory(self.output_directory + '/reference_sequences')
        _prepare_output_directory(self.output_directory + '/haplotype_information')
        _prepare_output_directory(self.output_directory + '/output_reads')
        _prepare_output_directory(self.output_directory + '/input_reads')
        
        self.summary_file_path = _prepare_summary_file(self.output_directory)
        
        self.RG_ID_dict = {}
        self.unique_RG_IDs = {}
        self.vcf_files = []
        self.sample_to_vcf_file_dict = {}
        self.sample_to_reference_sequences_dict = defaultdict(list)
        self.sample_to_reference_sequence_path = defaultdict(list)
        self.sample_to_sam_header = defaultdict(list)
        self.sample_to_PG_header = defaultdict(list)
        self.sample_to_RG_header = defaultdict(list)
        self.alignment_file_to_reference_sequences_dict = defaultdict(list)
        self.alignment_files = []
        self.phasable_samples = {}
        self.reference_sequence_files = {}
        # self.sample_hap_to_true_alignment_dict = {}
        
        self.reference_sequence_input = reference_sequence_input
        self.vcf_file_input = vcf_file_input
        self.long_read_input = long_read_input
        self.sample = sample
        self.ID = ID
        self.sample_description = sample_description
        self.ignore_phase_sets = ignore_phase_sets
        self.ignore_samples = ignore_samples
        self.download_from_urls = download_from_urls
        self.reference_sequence_input_assembly = reference_sequence_input_assembly
        
        if not self.reference_sequence_input_assembly is None:
            _prepare_output_directory(
                    self.output_directory + '/reference_sequences/' + str(reference_sequence_input_assembly)
                    )
        # if not vcf_file_input is None:
        # self.vcf_file_input = vcf_file_input
        # else:
        # self.vcf_file_input = vcf_file_input
        
        if not self.long_read_input is None:
            # self.long_read_input = long_read_input
            long_read_input_path, input_ID, input_sample, input_sample_description, input_reference_sequence_input = _extract_RG_info_from_long_read_input(
                    long_read_input
                    )
            if input_reference_sequence_input is None:
                input_reference_sequence_input = self.reference_sequence_input
            self.add_reads_from_file(
                    self.long_read_input, input_sample, input_ID, input_sample_description,
                    input_reference_sequence_input
                    )
        
        # if not long_reads_alignment_path is None:
        # self.long_reads_alignment_path = long_reads_alignment_path
        # self.add_reads_from_file(self.long_reads_alignment_path, sample, ID, sample_description,
        # self.reference_sequence_input)
        
        # if not self.vcf_file_input is None:
        # self.add_haplotype_information_from_file(self.vcf_file_input, self.ignore_phase_sets)
    
    def _download_file(self, url, output_directory = None):
        if output_directory is None:
            local_filename = self.output_directory + '/' + url.split('/')[-1]
        else:
            local_filename = output_directory + '/' + url.split('/')[-1]
        with requests.get(url, stream = True) as r:
            with open(local_filename, 'wb') as f:
                copyfileobj(r.raw, f)
        return local_filename
    
    # def _prepare_downloaded_vcf(self, assembly_version=None, sample=None, output_directory=None):
    
    # if output_directory is None: output_directory = self.output_directory if assembly_version is None: print('No
    # assembly version provided. Unable to download vcf file.') return if sample is None: print('No sample provided.
    # Unable to download vcf file.') return try: downloaded_vcf_file = str(assembly_version[str(sample)])
    # downloaded_vcf_file_path = output_directory+'/haplotype_information/'+str(sample)+'.vcf.gz' subprocess.run([
    # 'curl', '-L', downloaded_vcf_file_path, '| gunzip - >', str(output_directory)+'/haplotype_information/'+str(
    # assembly_version[sample]).replace('.vcf.gz','.vcf')], check = True) #subprocess.run(['curl', '-L',
    # downloaded_vcf_file, '-o', output_directory+'/haplotype_information/'+str(sample)+'.vcf.gz'], check = True)
    # print('VCF file downloaded successfully: %s.' % downloaded_vcf_file_path) return downloaded_vcf_file_path
    # except Exception as e: print(e) print('Error occurred while downloading VCF file.') return
    
    # def _prepare_downloaded_reference_sequence(self, assembly_version=None, output_directory=None):
    
    # if output_directory is None: output_directory = self.output_directory if assembly_version is None: print('No
    # assembly version provided. Unable to download reference sequence.') return try: reference_sequence_file = str(
    # assembly_version['reference_sequence']) subprocess.run(['curl', '-L', reference_sequence_file, '| gunzip - >',
    # str(output_directory)+'/reference_sequences/'+str(assembly_version['reference_sequence']).replace('.fa.gz',
    # '.fa')], check = True) #subprocess.run(['curl', '-L', reference_sequence_file, '-o',
    # output_directory+'/reference_sequences/'+str(assembly_version['reference_sequence_file_name'])], check = True)
    # reference_sequence_file_path = output_directory+'/reference_sequences/'+str(assembly_version[
    # 'reference_sequence_file_name']) print('Reference sequence file downloaded successfully: %s.' %
    # reference_sequence_file_path) return reference_sequence_file_path except Exception as e: print(e) print('Error
    # occurred while downloading reference sequence file.') return
    
    def _prepare_reference_sequence_file(
            self, reference_sequence_input, output_directory = None, reference_sequence_input_assembly = None
            ) -> object:
        
        if output_directory is None:
            output_directory_path = self.output_directory
        else:
            output_directory_path = output_directory
        
        if reference_sequence_input_assembly is None:
            output_directory_path = self.output_directory + '/reference_sequences'
        else:
            _prepare_output_directory(
                    self.output_directory + '/reference_sequences/' + str(reference_sequence_input_assembly)
                    )
            output_directory_path = self.output_directory + '/reference_sequences/' + str(
                    reference_sequence_input_assembly
                    )
        
        if reference_sequence_input.startswith('http'):
            print('The reference sequence input is a url. Downloading now.')
            reference_sequence_input = self._download_file(reference_sequence_input, output_directory_path)
        
        try:
            if reference_sequence_input.endswith('.fa'):
                reference_sequence_input_path = reference_sequence_input
            elif reference_sequence_input.endswith('.fasta'):
                reference_sequence_input_path = reference_sequence_input.replace(".fasta", '.fa')
            else:
                reference_sequence_input_path = os.path.dirname(reference_sequence_input) + '/' +\
                                                os.path.basename(reference_sequence_input).split('.')[0] + '.fa'
            
            with pysam.BGZFile(reference_sequence_input, 'r') as infile:
                with open(reference_sequence_input_path, 'w') as outfile:
                    outfile.write(infile.read().decode())
        except:
            try:
                if reference_sequence_input.endswith('.fa'):
                    reference_sequence_input_path = reference_sequence_input.replace('.fa', '.fa.gz')
                elif reference_sequence_input.endswith('.fasta'):
                    reference_sequence_input_path = reference_sequence_input.replace('.fasta', '.fa.gz')
                else:
                    reference_sequence_input_path = os.path.dirname(reference_sequence_input) + '/' +\
                                                    os.path.basename(reference_sequence_input).split('.')[0] + '.fa.gz'
                
                with pysam.BGZFile(reference_sequence_input, 'r') as infile:
                    with pysam.BGZFile(reference_sequence_input_path, 'wb') as outfile:
                        outfile.write(infile.read())
            except:
                print('fail reference sequence prep')
                return
        
        # with pysam.BGZFile(reference_sequence_input, 'r') as infile:
        # with pysam.BGZFile(reference_sequence_input_path,'w') as outfile:
        # outfile.write(infile.read())
        
        try:
            ref_seq = pysam.FastaFile(reference_sequence_input_path)
            #reference_sequence_names = ref_seq.references
            reference_sequence_file_path: object = ref_seq.filename.decode()
            self.reference_sequence_files[reference_sequence_file_path] = ref_seq
            if reference_sequence_input_assembly:
                self.reference_sequence_files[reference_sequence_input_assembly] = ref_seq
        except Exception as e:
            print(e)
            # try: output_reference_sequence_file_path = output_directory_path+'/'+os.path.basename(
            # reference_sequence_file_path) subprocess.Popen(['gunzip', '-c', reference_sequence_file_path, '>',
            # output_reference_sequence_file_path.replace('.fa.gz','.fa')], check = True) subprocess.run(['bgzip',
            # output_reference_sequence_file_path.replace('.fa.gz','.fa')], check = True) ref_seq = pysam.FastaFile(
            # reference_sequence_file) #reference_sequence_names = ref_seq.references
            # output_reference_sequence_file_path = ref_seq.filename.decode() except Exception as e: print(e) print(
            # 'Reference sequence file is not valid.')
        
        print(f'Reference sequence prepared successfully: {reference_sequence_file_path}')
        return reference_sequence_file_path  #reference_sequence_names
    
    def add_haplotype_information_from_file(
            self, vcf_file_input: str, ignore_phase_sets: bool = False, reference_sequence: object = 'hg38'
            ) -> object:
        """
        """
        vcf_file_path = self._prepare_vcf_file(self.output_directory, vcf_file_input)
        if pysam.VariantFile(vcf_file_path).header.formats.keys().count('PS') == 0:
            ignore_phase_sets = True
            print(
                    str(
                            vcf_file_path
                            ) + "This VCF file does not have the PS subfield. Phase sets will be ignored and all "
                                "phased variants on the same chromosome (vcf contig) will be considered to be one "
                                "contiguous haploblock "
                    )
        self.vcf_files.append({vcf_file_path:ignore_phase_sets})
        self.sample_to_vcf_file_dict = self._sample_to_vcf_file_dict(self.vcf_files)
        self.sample_to_alignment_files = _sample_to_alignment_files(self.sample_to_vcf_file_dict, self.RG_ID_dict)
        self._sample_to_reference_sequences_dict()
        self._sample_to_PG_dict()
    
    def __iter__(self):
        self.sample_counter = 0
        self.phasable_samples = {}
        return self
    
    def new_PhasableSample(self, sample: str, reference_sequence_paths: list = None) -> object:
        """

        Args:
            sample:
            reference_sequence_paths:

        Returns:

        """
        vcf_file_path, ignore_phase_sets = _pair_sample_with_vcf(
                sample, self.sample_to_vcf_file_dict, self.ignore_phase_sets
                )
        reference_sequence_names: list = self.sample_to_reference_sequences_dict[sample]
        phasable_sample = PhasableSample.PhasableSample(sample, vcf_file_path, ignore_phase_sets, self.sample_to_alignment_files[sample], self.RG_ID_dict,
                reference_sequence_names, reference_sequence_paths = reference_sequence_paths)
        return phasable_sample
    
    def __next__(self):
        if self.sample_counter < len(list(self.sample_to_vcf_file_dict.keys())):
            sample = str(list(self.sample_to_vcf_file_dict.keys())[self.sample_counter])
            if sample in self.sample_to_reference_sequence_path:
                if len(self.sample_to_reference_sequence_path[sample]) > 0:
                    reference_sequence_paths = self.sample_to_reference_sequence_path[sample]
            phasable_sample = self.new_PhasableSample(sample, reference_sequence_paths)
            #vcf_file_path, ignore_phase_sets = self._pair_sample_with_vcf(sample, self.sample_to_vcf_file_dict,
            #                                                             self.ignore_phase_sets)
            #phasable_sample = PhasableSample(sample, vcf_file_path, ignore_phase_sets,
            #                               self.sample_to_alignment_files[sample], self.RG_ID_dict)
            self.sample_counter += 1
            self.phasable_samples[phasable_sample.sample] = phasable_sample
            return phasable_sample
        else:
            raise StopIteration()
    
    def add_reads_from_file(
            self, long_reads_alignment_path, sample = None, ID = None, haplotype = None, sample_description = None,
            reference_sequence_input = None, database = None, master_database = False, simulated = False,
            reference_sequence_input_assembly = None
            ):
        """
        """
        # if reference_sequence_input == None:
        # reference_sequence_input = self.reference_sequence_input
        
        sorted_bam_file_paths, combined_long_read_fastq_path = self._parse_long_reads_input(
                long_reads_alignment_path, self.output_directory
                )
        if combined_long_read_fastq_path:
            reference_sequence_input = self._prepare_reference_sequence_file(
                    reference_sequence_input = reference_sequence_input, output_directory = self.output_directory,
                    reference_sequence_input_assembly = reference_sequence_input_assembly
                    )
            if reference_sequence_input is None:
                if self.reference_sequence_input is None:
                    print('Need reference sequence')
                    return
                else:
                    reference_sequence_input = self.reference_sequence_input
            sorted_bam_file_paths.append(
                    _align_long_reads_fastq(
                            combined_long_read_fastq_path, reference_sequence_input, self.output_directory
                            )
                    )
        for _sorted_bam_file_path in sorted_bam_file_paths:
            if _sorted_bam_file_path:
                sorted_bam_file_path, combined_long_read_fastq_path = self._parse_long_reads_input(
                        _sorted_bam_file_path, self.output_directory
                        )
                self.RG_ID_dict, self.unique_RG_IDs = self._compile_read_groups(
                        sorted_bam_file_path[0], sample, ID, sample_description, self.RG_ID_dict, self.unique_RG_IDs,
                        self.ignore_samples
                        )
                self.alignment_files.append(sorted_bam_file_path[0])
                self.sample_to_alignment_files = _sample_to_alignment_files(
                        self.sample_to_vcf_file_dict, self.RG_ID_dict
                        )
                self._sample_to_reference_sequences_dict(sorted_bam_file_path[0])
                self._sample_to_PG_dict(sam_file_path = sorted_bam_file_path[0])
                if reference_sequence_input is not None:
                    if not reference_sequence_input in self.sample_to_reference_sequence_path[sample]:
                        self.sample_to_reference_sequence_path[sample].append(reference_sequence_input)
    
    def _prepare_sam_header(self, _sample = None):
        if not str(_sample) in self.sample_to_sam_header:
            self.sample_to_sam_header[_sample] = defaultdict(list)
        self.sample_to_sam_header[_sample]['HD'] = {'VN':'1.6', 'SO':'coordinate'}
        self.sample_to_sam_header[_sample]['SQ'] = self.sample_to_reference_sequences_dict[_sample]
        self.sample_to_sam_header[_sample]['RG'] = self.sample_to_RG_header[_sample]
        self.sample_to_sam_header[_sample]['PG'] = self.sample_to_PG_header[_sample]
        return  # self.sample_to_sam_header[_sample]
    
    def _sample_to_reference_sequences_dict(self, sam_file_path = None, sam_file = None):
        if sam_file_path:
            for reference_sequence in pysam.AlignmentFile(sam_file_path).header['SQ']:
                self.alignment_file_to_reference_sequences_dict[sam_file_path].append(reference_sequence)
        for sample in self.sample_to_vcf_file_dict:
            for sam_file_path in self.alignment_file_to_reference_sequences_dict:
                if sam_file_path in self.sample_to_alignment_files[str(sample)]:
                    for reference_sequence in pysam.AlignmentFile(sam_file_path).header['SQ']:
                        if str(reference_sequence['SN']) not in [str(reference_seq['SN']) for reference_seq in
                                                                 self.sample_to_reference_sequences_dict[sample]]:
                            self.sample_to_reference_sequences_dict[sample].append(reference_sequence)
    
    def _sample_to_PG_dict(self, sam_file_path: object = None, sam_file: object = None) -> object:
        """

        Args:
            sam_file_path:
            sam_file:
        """
        if sam_file_path:
            for reference_sequence in pysam.AlignmentFile(sam_file_path).header['SQ']:
                self.alignment_file_to_reference_sequences_dict[sam_file_path].append(reference_sequence)
        for sample in self.sample_to_vcf_file_dict:
            for sam_file_path in self.alignment_file_to_reference_sequences_dict:
                if sam_file_path in self.sample_to_alignment_files[str(sample)]:
                    for PG_tag in pysam.AlignmentFile(sam_file_path).header['PG']:
                        PG_tag['ID'] = str(list(self.RG_ID_dict[sam_file_path].keys())[0])
                        # if PG_tag['ID'] in [PG_tag['ID'] for PG_tag in self.sample_to_PG_header[sample]]
                        RG_tag = {
                                'ID':str(list(self.RG_ID_dict[sam_file_path].keys())[0]), 'SM':str(
                                        self.RG_ID_dict[sam_file_path][
                                            str(list(self.RG_ID_dict[sam_file_path].keys())[0])]['SM']
                                        ),
                                'DS':str(
                                        self.RG_ID_dict[sam_file_path][
                                            str(list(self.RG_ID_dict[sam_file_path].keys())[0])]['DS']
                                        )
                                }
                        # {str(list(self.RG_ID_dict[sam_file_path].keys())[0]): {'DS': 'small7.fastq', 'SM': 'HG001',
                        # 'RG_tags': True, 'outputID': '1'}} self.RG_ID_dict[sam_file_path] self.RG_ID_dict[
                        # sam_file_path][str(list(self.RG_ID_dict[sam_file_path].keys())[0])]['SM'] if not PG_tag[
                        # 'ID'] in [PG_tag['ID'] for PG_tag in self.sample_to_PG_header[sample]]:
                        # self.sample_to_PG_header[sample].append(PG_tag)
                        new_PG_tag: bool = True
                        for PG_header in self.sample_to_PG_header[sample]:
                            if PG_tag['PN'] == PG_header['PN'] and PG_tag['ID'] == PG_header['ID']:
                                new_PG_tag = False
                        if new_PG_tag:
                            self.sample_to_PG_header[sample].append(PG_tag)
                        # self.sample_to_PG_header[sample].append(PG_tag)
                        if not RG_tag['ID'] in [RG_tag['ID'] for RG_tag in self.sample_to_RG_header[sample]]:
                            self.sample_to_RG_header[sample].append(RG_tag)
    
    def _parse_long_reads_input(self, long_read_input: object, output_directory: str) -> object:
        """

        Args:
            long_read_input (object):
            output_directory:

        Returns:
            object:

        """
        if long_read_input.startswith('http'):
            print('The long read input is a url. Downloading now.')
            long_reads_alignment_path = self._download_file(long_read_input, self.output_directory + '/input_reads')
        else:
            long_reads_alignment_path = long_read_input
        
        combined_long_read_fastq_path = []
        sorted_bam_file_paths = []
        
        if not os.path.exists(long_reads_alignment_path):
            print(
                    'Could not find %s. Use -i to specify the path of a file containing reads for phasing OR use -i '
                    'to specify the path of a directory containing the long read files and all files will be '
                    'processed individually. (EX: -i path/minion_run3_GM12878/minion_run3_GM12878_0.fastq OR -i '
                    'path/minion_run3_GM12878/minion_run3_GM12878_0.sam OR -i '
                    'path/minion_run3_GM12878/minion_run3_GM12878_0_sorted.bam OR -i path/minion_run3_GM12878/).' %
                    long_reads_alignment_path
                    )
            return
        
        elif os.path.isdir(long_reads_alignment_path):
            print(
                    'Directory was given as input for read files. Processing all files in %s.' % long_reads_alignment_path
                    )
            for file in os.listdir(long_reads_alignment_path):
                file = '%s/%s' % (os.path.abspath(long_reads_alignment_path), file)
                if os.path.isfile(file):
                    if str(file).lower().endswith('.fastq') or str(file).lower().endswith('.fastq.gz'):
                        print('%s is a valid fastq file.' % (file))
                        if not combined_long_read_fastq_path:
                            combined_long_read_fastq_path = os.path.abspath(
                                    '%s/%s%s' % (
                                            output_directory,
                                            os.path.splitext(os.path.basename(long_reads_alignment_path))[0],
                                            '_combined_fastq.gz')
                                    )
                        with open(combined_long_read_fastq_path, 'w') as combined_fastqs:
                            with open(file, 'r') as fastqfile:
                                combined_fastqs.write(fastqfile.read())
                    
                    elif str(file).lower().endswith('.sam') or str(file).lower().endswith('.bam'):
                        sorted_bam_file_paths.append(_prepare_alignment(output_directory, file))
        
        elif os.path.isfile(long_reads_alignment_path):
            if str(long_reads_alignment_path).lower().endswith('.fastq') or str(
                    long_reads_alignment_path
                    ).lower().endswith('.fastq.gz'):
                print('%s is a valid fastq file.' % long_reads_alignment_path)
                combined_long_read_fastq_path = os.path.abspath(
                        long_reads_alignment_path
                        )  # os.path.abspath('%s/%s%s' % (output_directory, os.path.splitext(
                # os.path.basename(long_reads_alignment_path))[0],'_combined_fastq.gz')) subprocess.run(['cat %s |
                # gzip >> %s' % (long_reads_alignment_path, combined_long_read_fastq_path)], check = True,
                # shell = True)
            
            elif str(long_reads_alignment_path).lower().endswith('.sam') or str(
                    long_reads_alignment_path
                    ).lower().endswith('.bam'):
                sorted_bam_file_paths.append(_prepare_alignment(output_directory, long_reads_alignment_path))
        else:
            print(
                    'Error: Reads should be in .fastq, .fastq.gz, .sam, or .bam format. %s does not have a correct '
                    'suffix to be a valid format and is not a directory. Use -i to specify the path of a file '
                    'containing reads for phasing OR use -i to specify the path of a directory containing the long '
                    'read files and all files will be processed individually. (EX: -i '
                    'path/minion_run3_GM12878/minion_run3_GM12878_0.fastq OR -i '
                    'path/minion_run3_GM12878/minion_run3_GM12878_0.sam OR -i '
                    'path/minion_run3_GM12878/minion_run3_GM12878_0_sorted.bam OR -i path/minion_run3_GM12878/).' %
                    long_reads_alignment_path
                    )
            return
        
        return sorted_bam_file_paths, combined_long_read_fastq_path
    
    def _prepare_vcf_file(self, output_directory: object, vcf_file_input: str) -> object:
        """

        Returns:
            object:
        """
        if vcf_file_input.startswith('http'):
            print('The vcf file input is a url. Downloading now.')
            vcf_file_input = self._download_file(vcf_file_input, self.output_directory + '/haplotype_information')
        
        print('############## Preparing vcf file ##############')
        
        start_process_time = time.time()
        
        if not os.path.isfile(vcf_file_input):
            print(
                    'Could not find %s. Use -v to specify the path of the vcf file to be used as haplotype information '
                    'for phasing. (EX: -v path/to/GM12878.vcf.gz or --vcf GM12878.vcf).' % vcf_file_input
                    )
            return
        
        elif os.path.isfile(vcf_file_input):
            vcf_file_pysam: VariantFile = pysam.VariantFile(vcf_file_input)
            if vcf_file_pysam.format == 'VCF':
                if vcf_file_pysam.compression == 'BGZF':
                    vcf_file_path = os.path.abspath(vcf_file_input)
                    vcf_file_index_path = '%s%s' % (vcf_file_path, '.tbi')
                    print('%s is a valid vcf file' % vcf_file_path)
                    if os.path.isfile(vcf_file_index_path):
                        print('Found %s as an index for vcf file' % vcf_file_index_path)
                    else:
                        print(
                                '%s is a valid .vcf file in bgzip (.vcf.gz) format but an index was not found. '
                                'Indexing with tabix now.' % vcf_file_input
                                )
                        
                        pysam.tabix_index(vcf_file_path, preset = 'vcf', force = True)
                        
                        # try:
                        # subprocess.run(['tabix', '-p', 'vcf', vcf_file_path],
                        # check=True)  # '-p' = 'preset' option to provide file type ('vcf')
                        # except Exception as e:
                        # print('Error occurred when tabix was run. Tabix must be installed on PATH for LRphase to '
                        # 'continue. Please check tabix installation or provide a tabix index for the vcf file '
                        # 'in the same folder as the bgzip compressed vcf file. If the vcf file has path: '
                        # 'path/to/name.vcf.gz file, then the index should be path/to/name.vcf.gz.tbi. Error: '
                        # '%s' % e)
                        #return
                        # else:
                        # print('Created %s' % vcf_file_index_path)
                else:
                    print(
                            '%s is a valid .vcf file but it is not in bgzip (.vcf.gz) format. VCF files must be '
                            'compressed with bgzip and indexed with tabix. LRphase will now attempt to run bgzip and '
                            'tabix on %s' % (vcf_file_input, vcf_file_input)
                            )
                    vcf_file_path = '%s/%s%s' % (
                            output_directory, os.path.splitext(os.path.basename(vcf_file_input))[0], 'sorted.vcf.gz')
                    #vcf_file_index_path = '%s%s' % (vcf_file_path, '.tbi')
                    
                    pysam.tabix_index(vcf_file_path, preset = 'vcf', force = True)
                    
                    # try: subprocess.run(["(grep ^'#' %s; grep -v ^'#' %s | sort -k1,1 -k2,2n) | bgzip > %s" % (
                    # vcf_file_input, vcf_file_input, vcf_file_path)], check=True, shell=True) except Exception as e:
                    # print('Error occurred when bgzip was run. Bgzip must be installed on PATH for LRphase to '
                    # 'continue. Please check bgzip installation or provide a bgzip compressed vcf file using ' 'the
                    # -v option (EX: -v path/to/GM12878.vcf.gz). Error: %s' % e) else: print('Created %s' %
                    # vcf_file_path)
                    
                    # try:
                    
                    # #subprocess.run(['tabix', '-p', 'vcf', vcf_file_path],check=True)  # '-p' = 'preset' option to
                    # provide file type ('vcf') except Exception as e: print('Error occurred when tabix was run.
                    # Tabix must be installed on PATH for LRphase to ' 'continue. Please check tabix installation or
                    # provide a tabix index for the vcf file in ' 'the same folder as the bgzip compressed vcf file.
                    # If the vcf file has path: ' 'path/to/name.vcf.gz file, then the index should be
                    # path/to/name.vcf.gz.tbi. Error: %s' % e) return else: print('Created %s' % vcf_file_index_path)
        
        vcf_file: VariantFile = pysam.VariantFile(vcf_file_path)
        if vcf_file_pysam.header.formats.keys().count('GT') == 0:
            print(
                    'The VCF file provided does not have the GT subfield. VCF files must have the GT subfield for all '
                    'samples in order to extract genotype information. Phased variants should have | in the GT '
                    'subfield instead of / '
                    )
            return
            # chromosomes_with_variants = list(vcf_file.index)
        
        end_process_time = time.time()
        total_process_time = end_process_time - start_process_time
        
        print(f'Prepared vcf file in {total_process_time:.2f} seconds', '\n')
        # summary_file(output_directory, time.time()-start_process_time, inspect.stack()[0][3], self.vcf_file_path)
        return vcf_file_path


def _sort_vcf_file(vcf_file_input: object, vcf_file_output: object) -> object:
    """

    Args:
        vcf_file_input: 
        vcf_file_output: 

    Returns:

    """
    try:
        subprocess.run(
                ["(grep ^'#' %s; grep -v ^'#' %s | sort -k1,1 -k2,2n) | bgzip > %s" % (
                        vcf_file_input, vcf_file_input, vcf_file_output)], check = True, shell = True
                )
        return vcf_file_output
    except Exception as e:
        print(
                "Error occurred when bgzip was run. Bgzip must be installed on PATH for LRphase to "
                "continue. Please check bgzip installation or provide a bgzip compressed vcf file using "
                "the -v option (EX: -v path/to/GM12878.vcf.gz). Error: %s" % e
                )
        return
