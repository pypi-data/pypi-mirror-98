# coding=utf-8
import time
from typing import Any, Iterator

import pysam


class PhasableSample:
    """

    """
    RG_ID_dict: object
    
    def __init__(
            self, sample, vcf_file_path, ignore_phase_sets, alignment_file_paths, RG_ID_dict,
            reference_sequence_names = None, reference_sequence_paths = None
            ):
        self.sample = sample
        self.vcf_file = pysam.VariantFile(vcf_file_path)
        self.vcf_file_path = vcf_file_path
        self.ignore_phase_sets = ignore_phase_sets
        self.alignment_file_paths = []
        self.RG_ID_dict = RG_ID_dict
        self.use_RG_tag = {}
        for alignment_file_path in alignment_file_paths:
            self.alignment_file_paths.append(str(alignment_file_path))
            self.use_RG_tag[str(alignment_file_path)] = alignment_file_paths[str(alignment_file_path)]
        self.reference_sequence_names = reference_sequence_names
        self.reference_sequence_paths = reference_sequence_paths
        self.reference_sequences_in_VCF = list(self.vcf_file.index)

    def _pysam_bam_files_initialize(self):
        bam_files = []
        for alignment_file_path in self.alignment_file_paths:
            bam_files.append(iter(pysam.AlignmentFile(alignment_file_path, 'rb')))
        return bam_files

    def __iter__(self):
        print('Alignments for sample %s' % str(self.sample))
        self.bam_files = self._pysam_bam_files_initialize()
        # self._initialize_alignment_counter()
        self.alignment_files_processed_count = 0
        self.alignments_processed_count = 0
        self.alignment_files_read_counts = []
        bam_file: Iterator[Any]
        for bam_file in self.bam_files:
            self.alignment_files_read_counts.append(bam_file.mapped + bam_file.unmapped)
        self.total_alignments = sum(self.alignment_files_read_counts)
        self.alignment_file_pysam = self.bam_files[self.alignment_files_processed_count]
        self.start_process_time = time.time()
        self.unique_read_names = set()
        return self

    def __next__(self):
        read = next(self.alignment_file_pysam)
        if read.query_name not in self.unique_read_names:
            self.unique_read_names.add(read.query_name)
        #read = self._evaluate_alignment(read)
        RG_info: object = self._get_RG_info_for_read(read, self.alignment_file_pysam)
        #if str(RG_info[2])[0:3] == 'SIM':
        #read.set_tag(tag='oa', value=str(RG_info[2][3]), value_type='Z', replace=True)
        read.set_tag(tag = 'RG', value = str(RG_info[1]), value_type = 'Z', replace = True)
        self.alignment_files_read_counts[self.alignment_files_processed_count] -= 1
        if self.alignment_files_read_counts[self.alignment_files_processed_count] == 0:
            self.alignment_files_processed_count += 1
            if self.alignment_files_processed_count == len(self.alignment_file_paths):
                raise StopIteration()
            self.alignment_file_pysam = self.bam_files[self.alignment_files_processed_count]
        self.alignments_processed_count += 1
        if self.alignments_processed_count % 2000 == 0:
            print(
                    'Processing %s reads per second' % str(
                            round(self.alignments_processed_count / (time.time() - self.start_process_time), 2)
                            )
                    )
            print(
                    'Processed %s reads (%s percent complete)' % (str(self.alignments_processed_count), str(
                            round(100 * (self.alignments_processed_count / self.total_alignments), 2)
                            ))
                    )
            print(
                    'Processing sample %s will finish in %s seconds' % (str(self.sample), str(
                            round(
                                    (self.total_alignments - self.alignments_processed_count) / (
                                            self.alignments_processed_count / (time.time() - self.start_process_time)),
                                    1
                                    )
                            ))
                    )
        return read

    def __repr__(self):
        return f'Sample Name: {self.sample}\nVCF: {self.vcf_file_path}\nReference sequence path: {str(self.reference_sequence_paths)}\nTotal sequences in reference files: {len(self.reference_sequence_names)}\nTotal Reference sequences in VCF: {len(self.reference_sequences_in_VCF)}\nAlignment Files: {str(self.alignment_file_paths)}\nTotal alignment files processed: {self.alignment_files_processed_count}\nTotal alignments: {self.total_alignments}\nTotal alignments processed: {self.alignments_processed_count}\nTotal unique reads observed: {len(self.unique_read_names)}'

    def _get_RG_info_for_read(self, read: pysam.AlignedSegment, alignment_file: object) -> object:
        """

        Args:
            read: 
            alignment_file: 

        Returns:

        """
        alignment_file_path = ''
        if isinstance(alignment_file, pysam.AlignmentFile):
            if str(alignment_file.filename.decode()) in self.alignment_file_paths:
                alignment_file_path = str(alignment_file.filename.decode())
            else:
                return
        elif str(alignment_file) in self.alignment_file_paths:
            alignment_file_path = str(alignment_file)
        else:
            return
        if alignment_file_path in self.use_RG_tag.keys():
            use_RG_tag = self.use_RG_tag[alignment_file_path]
            if use_RG_tag:
                if str(read.get_tag('RG')) in self.RG_ID_dict[alignment_file_path]:
                    if self.RG_ID_dict[alignment_file_path][str(read.get_tag('RG'))]['SM'] == self.sample:
                        ID = str(read.get_tag('RG'))
                        outputID = self.RG_ID_dict[alignment_file_path][str(read.get_tag('RG'))]['outputID']
                        sample_description = self.RG_ID_dict[alignment_file_path][str(read.get_tag('RG'))]['DS']
                        return ID, outputID, sample_description, use_RG_tag
            else:
                ID = list(self.RG_ID_dict[alignment_file_path].keys())[0]
                outputID = self.RG_ID_dict[alignment_file_path][ID]['outputID']
                sample_description = self.RG_ID_dict[alignment_file_path][ID]['DS']
                return ID, outputID, sample_description, use_RG_tag

    # @classmethod
    # def PhasableSample(
    #         cls, sample, vcf_file_path, ignore_phase_sets, param, RG_ID_dict: object, reference_sequence_names,
    #         reference_sequence_paths
    #         ):
    #     """
    #
    #     Args:
    #         sample:
    #         vcf_file_path:
    #         ignore_phase_sets:
    #         reference_sequence_names:
    #         reference_sequence_paths:
    #         RG_ID_dict (object):
    #
    #     Returns:
    #         object:
    #     """
    #     pass
