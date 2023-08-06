import math
import os
from collections import defaultdict

#import numpy as np
import pyliftover

import PhaseSet


def true_alignment_match(
        aligned_segment: object, needs_liftover: object = False, contig: object = None,
        ref_start: object = None,
        ref_end: object = None,
        strand: object = None,
        tag_read: object = False,
        only_output_match_label: object = False,
        only_output_overlap: object = False,
        true_reference_sequence_path: object = None,
        aligned_reference_sequence_path: object = None,
        liftover_converter: object = None,
        chain_file_path: object = None,
        sample: object = None,
        haplotype: object = None,
        reference_liftover_converters: object = None) -> object:
    """
Args:
    aligned_segment:
    needs_liftover:
    contig:
    ref_start (object):
    ref_end:
    strand:
    tag_read:
    only_output_match_label:
    only_output_overlap:
    true_reference_sequence_path:
    aligned_reference_sequence_path (object):
    liftover_converter:
    chain_file_path:
    sample:
    haplotype:
    reference_liftover_converters:

Returns:

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
    if int(aligned_segment.reference_start) >= int(ref_start) and int(aligned_segment.reference_start) <= int(
            ref_end
            ):
        match_label = 'mapping_match'
        if int(aligned_segment.reference_end) >= int(ref_end):
            overlap = int(ref_end) - int(aligned_segment.reference_start)
        else:
            overlap = int(aligned_segment.reference_end) - int(aligned_segment.reference_start)
    elif int(aligned_segment.reference_end) >= int(ref_start) and int(aligned_segment.reference_end) <= int(
            ref_end
            ):
        match_label = 'mapping_match'
        if int(ref_start) >= int(aligned_segment.reference_start):
            overlap = int(aligned_segment.reference_end) - int(ref_start)
        else:
            overlap = int(aligned_segment.reference_end) - int(aligned_segment.reference_start)
    elif aligned_segment.reference_start >= (
            int(ref_start) - (int(ref_start) * 0.1)) and aligned_segment.reference_start <= (
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
        aligned_segment, tag_read = False, contig = None, ref_start = None, ref_end = None, strand = None
        ):
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


def true_read_origin(
        aligned_segment, tag_read = False, sample = None, haplotype = None, contig = None, ref_start = None,
        ref_end = None, strand = None
        ):
    if '!' in str(aligned_segment.query_name):
        _ref_start: object
        _read_name, _contig, _ref_start, _ref_end, _strand = aligned_segment.query_name.split('!')
        if contig is None:
            contig = _contig
        if ref_start is None:
            ref_start = _ref_start
        if ref_end is None:
            ref_end = _ref_end
        if strand is None:
            strand = _strand
        
        if '__' in _read_name:
            sample, haplotype, name_contig_numeric = _read_name.split('__')
    
    if tag_read:
        
        aligned_segment.set_tag(tag = 'sm', value = str(sample), value_type = 'Z', replace = True)
        aligned_segment.set_tag(tag = 'ha', value = str(haplotype), value_type = 'Z', replace = True)
    
    return sample, haplotype


def alignment_type(aligned_segment, tag_read = False):
    alignment_type = 'None'
    if aligned_segment.is_unmapped:
        alignment_type = 'unmapped'
    elif aligned_segment.is_secondary:
        alignment_type = 'secondary'
    elif aligned_segment.is_supplementary:
        alignment_type = 'supplementary'
    else:
        alignment_type = 'mapped'
    if tag_read:
        aligned_segment.set_tag(tag = 'al', value = str(alignment_type), value_type = 'Z', replace = True)
    
    return alignment_type


class PhasedRead:
    """

    """
    
    def __init__(
            self, aligned_segment, vcf_file = None, sample = None, ignore_phase_sets = False, error_model = 0,
            error_rate_threshold = 0.01,
            prior_probabilities = None, bam_file_header = None, output_file_path = None, liftover_converters = None,
            multinomial_correction = True, auto_phase = True, evaluate_alignment = True,
            evaluate_true_alignment = False, phasable_sample = None, input_data = None
            ):
        
        self.aligned_segment = aligned_segment
        self.vcf_file = vcf_file
        self.sample = sample
        self.ignore_phase_sets = ignore_phase_sets
        self.error_model = error_model
        self.multinomial_correction = multinomial_correction
        self.error_rate_threshold = error_rate_threshold
        self.prior_probabilities = prior_probabilities
        # self._get_alignment_label()
        if liftover_converters:
            self.liftover_converters = liftover_converters
        else:
            self.liftover_converters = None
        self.auto_phase = auto_phase
        # self.log_likelihood_ratio = None
        # self.phase_set_name = None
        # self.max_phase = None
        self._Phase_Set_max = None
        self.PhaseSets = []
        self.evaluate_alignment = evaluate_alignment
        self.evaluate_true_alignment = evaluate_true_alignment
        if output_file_path:
            self.output_file_path = output_file_path
        else:
            self.output_file_path = '%s_phase_tagged.bam' % self.sample
        if bam_file_header:
            self.bam_file_header = bam_file_header
        if self.evaluate_alignment:
            self._evaluate_alignment()
        
        if self.auto_phase:
            self.phase_read(
                    error_model = self.error_model, error_rate_threshold = self.error_rate_threshold,
                    multinomial_correction = self.multinomial_correction,
                    evaluate_alignment = self.evaluate_alignment,
                    evaluate_true_alignment = self.evaluate_true_alignment
                    )
    
    def __repr__(self):
        return f'Read Name: {self.query_name}\nRead Length: {self.aligned_segment.query_length}\nAlignment Type: {self.alignment_type}\nPrimary Alignment Length: {self.aligned_segment.query_alignment_length}'
    
    def __iter__(self):
        self.PhaseSets = self._find_PhaseSets(
                self.error_model, self.error_rate_threshold, self.prior_probabilities,
                liftover_converters = self.liftover_converters
                )
        self.PhaseSets_processed_count = 0
        # self.alignment_files_read_counts = [bam_file.mapped+bam_file.unmapped for bam_file in self.bam_files]
        return self
    
    def __next__(self):
        if self.PhaseSets_processed_count < len(self.PhaseSets):
            PhaseSet = self.PhaseSets[self.PhaseSets_processed_count]
            self.PhaseSets_processed_count += 1
            return PhaseSet
        else:
            raise StopIteration()
    
    @property
    def _evaluate_true_alignment(self) -> object:
        """

        Returns:

        """
        overlap = 0
        match_label = 'non_match'
        if '!' in str(self.aligned_segment.query_name):
            contig: object
            read_name, contig, ref_start, ref_end, strand = self.aligned_segment.query_name.split('!')
            if self.liftover_converters:
                try:
                    contig =\
                        self.liftover_converters[str(self.aligned_segment.get_tag('oa'))][
                            'converter'].convert_coordinate(
                                contig,
                                int(
                                        ref_start
                                        )
                                )[
                            0][0]
                    ref_start =\
                        self.liftover_converters[str(self.aligned_segment.get_tag('oa'))][
                            'converter'].convert_coordinate(
                                contig,
                                int(
                                        ref_start
                                        )
                                )[
                            0][1]
                    self.aligned_segment.set_tag(tag = 'st', value = str(ref_start), value_type = 'Z', replace = True)
                    self.aligned_segment.set_tag(tag = 'lo', value = str(contig), value_type = 'Z', replace = True)
                except:
                    self.aligned_segment.set_tag(tag = 'st', value = 'NA', value_type = 'Z', replace = True)
                    self.aligned_segment.set_tag(tag = 'en', value = 'NA', value_type = 'Z', replace = True)
                try:
                    ref_end =\
                        self.liftover_converters[str(self.aligned_segment.get_tag('oa'))][
                            'converter'].convert_coordinate(
                                contig,
                                int(
                                        ref_end
                                        )
                                )[
                            0][1]
                    self.aligned_segment.set_tag(tag = 'en', value = str(ref_end), value_type = 'Z', replace = True)
                except:
                    self.aligned_segment.set_tag(tag = 'en', value = 'NA', value_type = 'Z', replace = True)
            if self.aligned_segment.reference_name == contig:
                match_label = 'ref_match'
                if int(self.aligned_segment.reference_start) >= int(ref_start) and int(
                        self.aligned_segment.reference_start
                        ) <= int(ref_end):
                    match_label = 'mapping_match'
                    if int(self.aligned_segment.reference_end) >= int(ref_end):
                        overlap = int(ref_end) - int(self.aligned_segment.reference_start)
                    else:
                        overlap = int(self.aligned_segment.reference_end) - int(self.aligned_segment.reference_start)
                elif int(self.aligned_segment.reference_end) >= int(ref_start) and int(
                        self.aligned_segment.reference_end
                        ) <= int(ref_end):
                    match_label = 'mapping_match'
                    if int(ref_start) >= int(self.aligned_segment.reference_start):
                        overlap = int(self.aligned_segment.reference_end) - int(ref_start)
                    else:
                        overlap = int(self.aligned_segment.reference_end) - int(self.aligned_segment.reference_start)
                elif (
                        int(ref_start) - (int(ref_start) * 0.1)) <= self.aligned_segment.reference_start <= (
                        int(ref_end) + (int(ref_end) * 0.1)):
                    match_label = 'within_10percent'
            
            self.aligned_segment.set_tag(
                    tag = 'ov', value = str(overlap / (int(ref_end) - int(ref_start))), value_type = 'Z', replace = True
                    )
            self.aligned_segment.set_tag(
                    tag = 'OV', value = str(overlap / (self.aligned_segment.query_alignment_length)), value_type = 'Z',
                    replace = True
                    )
            self.aligned_segment.set_tag(tag = 'ml', value = str(match_label), value_type = 'Z', replace = True)
            return match_label

    def _evaluate_alignment(self):
        alignment_label = 'None'
        if self.aligned_segment.is_unmapped:
            alignment_label = 'unmapped_reads'
        elif self.aligned_segment.reference_name not in list(self.vcf_file.index):
            alignment_label = 'aligned_to_contig_not_in_vcf'
        elif self.aligned_segment.is_secondary:
            alignment_label = 'secondary_alignments'
        elif self.aligned_segment.is_supplementary:
            alignment_label = 'supplementary_alignments'

        # elif self.aligned_segment.query_alignment_length/self.aligned_segment.query_length < 0.95:
        # alignment_label = 'reads_truncated_95percent'
        else:
            alignment_label = 'mapped_reads'
        # self.aligned_segment.set_tag(tag = 'xx', value = str(self.aligned_segment.query_alignment_length/self.aligned_segment.query_length),
        # value_type='Z', replace=True)
        self.aligned_segment.set_tag(tag = 'al', value = str(alignment_label), value_type = 'Z', replace = True)
    
    def write_per_read_phasing_stats(self, per_read_phasing_stats_file_path = None):
        """

        Args:
            per_read_phasing_stats_file_path:

        Returns:

        """
        # with open(per_read_phasing_stats_file_path, 'a') as per_read_phasing_stats: per_read_phasing_stats.write(
        # aligned_segment.query_name + '\t' + str(aligned_segment.reference_name) + '\t' + str(aligned_segment.reference_start) + '\t' + str(
        # aligned_segment.reference_end) + '\t' + str(sample) + '\t' + str(phase_set) + '\t' + str(phase) + '\t' + str(
        # phasing_quality)  + '\t' + str(total_hets_phase_set[phase_set])  + '\t' + str(
        # total_hets_analyzed_phase_set[phase_set]) + '\t' + str(matches_phase_set[phase_set][max_phase-1]) + '\t' +
        # str(non_matches_phase_set[phase_set][max_phase-1]) + '\t' + str(round(log_likelihood_ratio, 2)) + '\t' +
        # str(per_base_sequence_divergence) + '\t' + str(per_base_mismatch_rate) + '\t' + str(error_rate_qual) + '\t'
        # + str(ID) + '\t' + str(sample_description) + '\t' + str(max_phase) + '\t' + str(multi_PS) + '\t' + str(
        # phase_sets) + '\t' + str(phases) + '\t' + str(log_likelihood_ratios_phase_set[phase_set]) + '\t' + str(
        # max_log_likelihood_ratios) + '\t' + str(aligned_segment.query_length) + '\n')
        return
    
    def write_phase_tagged_bam(self, output_file_path_bam = None, output_bam_pysam = None, header = None):
        """

        Args:
            output_file_path_bam:
            output_bam_pysam:
            header:

        Returns:

        """
        # self.aligned_segment.set_tag(tag = 'PS', value = str(self.phase_set_name), value_type='Z', replace=True)
        # self.aligned_segment.set_tag(tag = 'HP', value = str(self.phase), value_type='Z', replace=True)
        # self.aligned_segment.set_tag(tag = 'PC', value = str(self.log_likelihood_ratio), value_type='Z', replace=True)
        self.aligned_segment.set_tag(tag = 'PS', value = str(self.phase_set_name), value_type = 'Z', replace = True)
        self.aligned_segment.set_tag(tag = 'HP', value = str(self.phase), value_type = 'Z', replace = True)
        self.aligned_segment.set_tag(
                tag = 'PC', value = str(self.log_likelihood_ratio), value_type = 'Z', replace = True
                )
        self.aligned_segment.set_tag(tag = 'py', value = str(self.ploidy_phase_set), value_type = 'Z', replace = True)
        # #################################################################################################
        # aligned_segment.set_tag(tag = 'lr', value = str(phased_read.log_likelihood_ratio), value_type='Z', replace=True)
        # aligned_segment.set_tag(tag = 'ma', value = str(phased_read.total_matches_to_favored_haplotype), value_type='Z',
        # replace=True) aligned_segment.set_tag(tag = 'mm', value = str(phased_read.total_non_matches_to_favored_haplotype),
        # value_type='Z', replace=True) aligned_segment.set_tag(tag = 'pl', value = str(phased_read.ploidy_phase_set),
        # value_type='Z', replace=True)
        # #################################################################################################
        
        # if header:
        # _bam_file_header = header
        # else:
        # _bam_file_header = self.bam_file_header
        
        if output_bam_pysam:
            _output_file_path = output_bam_pysam
        elif output_file_path_bam is None:
            _output_file_path = output_file_path_bam
        else:
            return
        
        # self.aligned_segment.set_tag(tag = 'RG', value = str(RG_info[1]), value_type='Z', replace=True)
        # output_bam = pysam.AlignmentFile(_output_file_path, 'wb', header = _bam_file_header)
        output_bam_pysam.write(self.aligned_segment)
        
        return
    
    def _find_PhaseSets(self, error_model, error_rate_threshold, prior_probabilities, liftover_converters = None):
        
        if liftover_converters is None:
            liftover_converters = self.liftover_converters
        
        self._evaluate_alignment()
        
        if self.aligned_segment.is_unmapped:
            self._Phase_Set_max = 'unmapped'
            return 'Nonphasable'
        
        if self.aligned_segment.get_tag('al') == 'aligned_to_contig_not_in_vcf' or self.aligned_segment.is_unmapped:
            return 'aligned_to_contig_not_in_vcf'
        
        variants_phase_sets = self._fetch_phased_variants(
                self.aligned_segment, self.vcf_file, self.sample, self.ignore_phase_sets
                )
        
        PhaseSets = []
        if len(variants_phase_sets) > 0:
            if max([len(variants_phase_sets[str(phase_set)]) for phase_set in variants_phase_sets]) > 0:
                for phase_set in variants_phase_sets:
                    PhaseSets.append(
                            PhaseSet.PhaseSet(
                                    phase_set, self.aligned_segment, variants_phase_sets[str(phase_set)],
                                    str(self.sample),
                                    error_model = error_model, error_rate_threshold = error_rate_threshold,
                                    prior_probabilities = prior_probabilities, liftover_converters = liftover_converters
                                    )
                            )
        
        return PhaseSets
    
    def phase_read(
            self, error_model = None, error_rate_threshold = None, prior_probabilities = None,
            multinomial_correction = None, evaluate_alignment = True, evaluate_true_alignment = True
            ):
        '''#self.Phase_Set_max, self.phase, self.phase_set_name, self.log_likelihood_ratio, self.max_phase,
        self.ploidy_phase_set = self._select_best_phasing(self._find_PhaseSets()) '''
        if error_model is None:
            error_model = self.error_model
        if error_rate_threshold is None:
            error_rate_threshold = self.error_rate_threshold
        if multinomial_correction is None:
            multinomial_correction = True
        
        if evaluate_alignment:
            self._evaluate_alignment()
        if evaluate_true_alignment:
            if self.aligned_segment.has_tag('oa'):
                match_label = self._evaluate_true_alignment
        
        if not self.aligned_segment.has_tag('al'):
            self._evaluate_alignment()
        
        if not self.aligned_segment.has_tag('ml'):
            if self.aligned_segment.has_tag('oa'):
                match_label = self._evaluate_true_alignment
        
        _Phase_Set_max = self._select_best_phasing(
                self._find_PhaseSets(
                        error_model, error_rate_threshold, prior_probabilities,
                        liftover_converters = self.liftover_converters
                        ), error_model, error_rate_threshold,
                prior_probabilities, multinomial_correction
                )
        
        self._Phase_Set_max = _Phase_Set_max
        # self.aligned_segment.set_tag(tag = 'PS', value = str(self.phase_set_name), value_type='Z', replace=True)
        # self.aligned_segment.set_tag(tag = 'HP', value = str(self.phase), value_type='Z', replace=True)
        # self.aligned_segment.set_tag(tag = 'PC', value = str(self.log_likelihood_ratio), value_type='Z', replace=True)
        # self.aligned_segment.set_tag(tag = 'py', value = str(self.ploidy_phase_set), value_type='Z', replace=True)
        
        return self
    
    def _select_best_phasing(
            self, PhaseSets, error_model, error_rate_threshold, prior_probabilities = None,
            multinomial_correction = True
            ):
        '''self.Phase_Set_max, self.phase, self.phase_set_name, self.log_likelihood_ratio, self.max_phase =
        self._select_best_phasing(self.PhaseSets) '''
        self.PhaseSets = PhaseSets
        phasable = {}
        if isinstance(PhaseSets, str):
            return 'Nonphasable'
        
        if len(PhaseSets) > 0:
            for Phase_Set in PhaseSets:
                Phase_Set.solve_phase(error_model, error_rate_threshold, prior_probabilities, multinomial_correction)
                if isinstance(Phase_Set.max_log_likelihood_ratio, float):
                    phasable[Phase_Set.max_log_likelihood_ratio] = Phase_Set
        
        if len(phasable) > 0:
            Phase_Set_max = phasable[max(phasable.keys())]
            # phase = Phase_Set_max.phase
            # phase_set_name = Phase_Set_max.phase_set
            # log_likelihood_ratio = Phase_Set_max.max_log_likelihood_ratio
            # max_phase = Phase_Set_max.max_phase
            Phase_Set_max = Phase_Set_max
        
        else:
            # phase = 'Nonphasable'
            # phase_set_name = None
            # log_likelihood_ratio = None
            # max_phase = 'Nonphasable'
            Phase_Set_max = 'Nonphasable'
        
        return Phase_Set_max  # phase, phase_set_name, log_likelihood_ratio, max_phase
    
    # @staticmethod
    def _fetch_phased_variants(self, aligned_segment, vcf_file, sample, ignore_phase_sets):
        '''self.variants_phase_sets = self._fetch_phased_variants(self.aligned_segment, self.vcf_file, self.sample,
        self.ignore_phase_sets) '''
        variants_phase_sets = defaultdict(list)
    
        for vcf_record in vcf_file.fetch(
                aligned_segment.reference_name, aligned_segment.reference_start, aligned_segment.reference_end
                ):
            if vcf_record.samples[str(sample)].phased and max(vcf_record.samples[str(sample)].allele_indices) > min(
                    vcf_record.samples[str(sample)].allele_indices
                    ):
                if ignore_phase_sets:
                    variants_phase_sets['ignore_phase_sets'].append(vcf_record)
                else:
                    variants_phase_sets[str(vcf_record.samples[str(sample)]['PS'])].append(vcf_record)
        return variants_phase_sets
    
    @property
    def is_phased_correctly(self):
        '''
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            if self.is_Phased:
                if self.aligned_segment.has_tag('oa'):
                    return str(self.phase) == str(self.aligned_segment.get_tag('oa'))
    
    @property
    def read_name(self):
        '''
        '''
        return str(self.aligned_segment.query_name)
    
    @property
    def query_name(self):
        '''
        '''
        return str(self.aligned_segment.query_name)
    
    @property
    def alignment_type(self):
        '''
        '''
        if self.aligned_segment.has_tag('al'):
            return str(self.aligned_segment.get_tag('al'))
    
    @property
    def fraction_of_read_overlapping_true_alignment(self):
        '''
        '''
        if self.aligned_segment.has_tag('ov'):
            return str(self.aligned_segment.get_tag('ov'))
    
    @property
    def alignment_is_unmapped(self):
        '''
        '''
        return self.aligned_segment.is_unmapped
    
    @property
    def alignment_is_supplementary(self):
        '''
        '''
        return self.aligned_segment.is_supplementary
    
    @property
    def alignment_is_secondary(self):
        '''
        '''
        return self.aligned_segment.is_secondary
    
    @property
    def is_aligned_to_contig_not_in_vcf(self):
        '''
        '''
        return self.aligned_segment.reference_name not in list(self.vcf_file.index)
    
    @property
    def alignment_is_reverse(self):
        '''
        true if aligned_segment is mapped to reverse strand
        '''
        return self.aligned_segment.is_reverse
    
    @property
    def alignment_is_mapped(self):
        '''
        '''
        return self.aligned_segment.is_unmapped == False
    
    @property
    def alignment_is_primary(self):
        '''
        '''
        if self.aligned_segment.has_tag('tp'):
            return str(self.aligned_segment.get_tag('tp')) == 'P'
        # return self.aligned_segment.is_unmapped == False
    
    @property
    def validation_using_true_alignment_label(self):
        '''
        '''
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml'))
    
    @property
    def matches_true_alignment(self):
        '''
        '''
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml')) == 'mapping_match'
    
    @property
    def mapped_within_10percent_of_true_alignment(self):
        '''
        '''
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml')) == 'within_10percent'
    
    @property
    def does_not_overlap_true_alignment_but_does_align_to_true_contig(self):
        '''
        '''
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml')) == 'ref_match'
    
    @property
    def does_not_match_true_alignment(self):
        '''
        '''
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml')) == 'non_match'
    
    @property
    def alignment_length_fraction_of_total_read_length(self):
        '''
        aligned_segment.query_alignment_length/aligned_segment.query_length
        returns 0 if unmapped
        '''
        # self.aligned_segment.set_tag(tag = 'xx', value = str(self.aligned_segment.query_alignment_length/self.aligned_segment.query_length),
        # value_type='Z', replace=True)
        if self.aligned_segment.has_tag('al'):
            if str(self.aligned_segment.get_tag('al')) == 'unmapped_reads':
                return 0
            return self.aligned_segment.query_alignment_length / self.aligned_segment.query_length
    
    @property
    def fraction_of_alignment_length_overlapping_true_alignment(self):
        '''
        '''
        if self.aligned_segment.has_tag('OV'):
            return str(self.aligned_segment.get_tag('OV'))
    
    @property
    def favored_phase_is_correct(self):
        '''
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            if self.one_phase_is_favored:
                if self.aligned_segment.has_tag('oa'):
                    return str(self.max_phase) == str(self.aligned_segment.get_tag('oa'))
    
    @property
    def is_phased_incorrectly(self):
        '''
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            if self.is_Phased:
                if self.aligned_segment.has_tag('oa'):
                    return str(self.phase) != str(self.aligned_segment.get_tag('oa'))
    
    @property
    def favored_phase_is_incorrect(self):
        '''
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            if self.one_phase_is_favored:
                if self.aligned_segment.has_tag('oa'):
                    return str(self.max_phase) != str(self.aligned_segment.get_tag('oa'))
    
    @property
    def is_Nonphasable(self):
        '''
        Returns True if this aligned_segment was assigned Nonphasable for not having any heterozygous positions
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return True
        else:
            return self.phase == 'Nonphasable'
    
    @property
    def is_Unphased(self):
        '''
        Returns True if this aligned_segment was left unassigned (Unphased) because it did not have a log likelihood ratio (LR)
        above the threshold chosen for this experiment.
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            return self.phase == 'Unphased'
    
    @property
    def is_Phased(self):
        '''
        Returns True if this aligned_segment was assigned to a haplotype based on its log likelihood ratio (LR) being above the
        threshold chosen for this experiment.
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            if self.phase == 'Unphased' or self.phase == 'Nonphasable':
                is_Phased = False
            else:
                is_Phased = True
            return is_Phased
    
    @property
    def one_phase_is_favored(self):
        '''
        Returns True if this aligned_segment was assigned to a haplotype based on its log likelihood ratio (LR) being above the
        threshold chosen for this experiment.
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            if int(self.max_phase) > 0:
                one_phase_is_favored = True
            elif int(self.max_phase) == 0:
                one_phase_is_favored = False
            else:
                return
            return one_phase_is_favored
    
    def is_assigned_to_haplotype_i(self, haplotype):
        
        '''Returns True if this aligned_segment was was assigned to haplotype i. (ie: the index of the haplotype in the allele_indices A|T )
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            return str(self.phase) == str(haplotype)
    
    @property
    def overlaps_multiple_phase_sets(self):
        '''
        This aligned_segment overlapped heterozygous positions that belonged to at least two different phase sets (independently
        phased blocks of sequence are only phased within themselves and one must be chosen)
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        if len(self.PhaseSets) > 1:
            overlaps_multiple_phase_sets = True
        else:
            overlaps_multiple_phase_sets = False
        return overlaps_multiple_phase_sets
    
    @property
    def Phase_Set_max(self):
        '''
        '''
        if self._Phase_Set_max is None:
            return
        elif self._Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self._Phase_Set_max
    
    @property
    def phase(self):
        '''
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.phase
    
    @property
    def max_phase(self):
        '''
        The number of distinct haplotypes at this position. Our model assumes that ploidy represents the ground truth
        molecular copy number of the population from which these reads were samples.
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.max_phase
    
    @property
    def phase_set_name(self):
        '''
        The number of distinct haplotypes at this position. Our model assumes that ploidy represents the ground truth
        molecular copy number of the population from which these reads were samples.
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.phase_set
    
    @property
    def phasing_error_rate(self):
        if self.phase == 'Nonphasable':
            return 0.50
        if self.log_likelihood_ratio > 0:
            if self.powlaw_modified(self.log_likelihood_ratio) <= 1 - (1 / float(self.ploidy_phase_set)):
                return self.powlaw_modified(self.log_likelihood_ratio)
            else:
                return 1 - (1 / float(self.ploidy_phase_set))
    
    def powlaw_modified(self, x, a = 4.5, xmin = 2):
        return ((a - 1) / xmin) * math.pow(x / xmin, -1 * a)
    
    @property
    def log_likelihood_ratio(self):
        '''
        The number of distinct haplotypes at this position. Our model assumes that ploidy represents the ground truth
        molecular copy number of the population from which these reads were samples.
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.max_log_likelihood_ratio
    
    @property
    def ploidy_phase_set(self):
        '''
        The number of distinct haplotypes at this position. Our model assumes that ploidy represents the ground truth
        molecular copy number of the population from which these reads were samples.
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.ploidy_phase_set
    
    @property
    def error_model_used(self):
        '''
        self.aligned_segment.set_tag(tag = 'em', value = str(self.error_model), value_type='Z', replace=True)

        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.error_model_used
    
    @property
    def multinomial_correction_used(self):
        '''
        self.aligned_segment.set_tag(tag = 'em', value = str(self.error_model), value_type='Z', replace=True)

        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            return self.Phase_Set_max.multinomial_correction
    
    @property
    def error_rate_threshold_used(self):
        '''

        self.aligned_segment.set_tag(tag = 'et', value = str(self.error_rate_threshold), value_type='Z', replace=True)
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.error_rate_threshold_used
    
    @property
    def prior_probabilities_used(self):
        '''

        self.aligned_segment.set_tag(tag = 'et', value = str(self.error_rate_threshold), value_type='Z', replace=True)
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.prior_probabilities_used
    
    @property
    def error_rate_average_het_sites_used(self):
        '''

        self.aligned_segment.set_tag(tag = 'er', value = str(Phase_Set_max.error_rate_average_het_sites_used), value_type='Z', replace=True)
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.error_rate_average_het_sites
    
    @property
    def per_base_mismatch_rate_used(self):
        '''

        self.aligned_segment.set_tag(tag = 'er', value = str(Phase_Set_max.error_rate_average_het_sites_used), value_type='Z', replace=True)
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.per_base_mismatch_rate
    
    @property
    def total_hets_analyzed_favored_haplotype(self):
        '''
        Returns the total number of heterozygous positions that were included in the phasing evaluation for this aligned_segment
        that resulted in the most favorable likelihood (ie: positions containing heterozygous SNVs that align to the
        aligned_segment of interest.)
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.total_hets_analyzed
    
    @property
    def total_hets_favored_haplotype(self):
        '''
        Returns the total number of heterozygous positions that overlapped this aligned_segment before filtering the sites with
        '-'. This set of het sites was the most favorable phase set that resulted in the most favorable likelihood (
        ie: positions containing heterozygous SNVs that align to the aligned_segment of interest.)
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.total_hets
    
    @property
    def total_matches_to_favored_haplotype(self):
        '''
        Returns the total number of matches to the favored haplotype sequence at heterozygous positions that
        overlapped this aligned_segment. This phased set of het sites resulted in the most favorable likelihood for this aligned_segment.
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.matches[self.Phase_Set_max.max_phase - 1]
    
    @property
    def total_non_matches_to_favored_haplotype(self):
        '''
        Returns the total number of non-matches to the favored haplotype sequence at heterozygous positions that
        overlapped this aligned_segment. This phased set of het sites resulted in the most favorable likelihood for this aligned_segment.
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.non_matches[self.Phase_Set_max.max_phase - 1]
    
    def prior_probability_for_haplotype_i(self, i):
        '''
        self.aligned_segment.set_tag(tag = 'pr', value = str(self.prior_probabilities), value_type='Z', replace=True)


        prior_probability_haplotype_i = P(haplotype_i)
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.prior_probabilities[i - 1]
    
    @property
    def prior_probability_for_favored_haplotype(self):
        '''
        self.aligned_segment.set_tag(tag = 'pr', value = str(self.prior_probabilities), value_type='Z', replace=True)


        prior_probability_haplotype_i = P(haplotype_i)
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.prior_probabilities[self.max_phase - 1]
    
    def calculate_log_likelihood_read_given_haplotype_i(self, i):
        """

        Args:
            i:

        Returns:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.log_probability_read_given_haplotype_i[i - 1]
    
    def calculate_likelihood_of_read_given_haplotype_i(self, i):
        """

        Args:
            i:

        Returns:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return 10**self.Phase_Set_max.log_probability_read_given_haplotype_i[i - 1]
    
    @property
    def calculate_log_likelihood_read_given_favored_haplotype(self):
        """

        Returns:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.log_probability_read_given_haplotype_i[self.max_phase - 1]
    
    @property
    def calculate_likelihood_of_read_given_favored_haplotype(self):
        """

        Returns:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return 10**self.Phase_Set_max.log_probability_read_given_haplotype_i[self.max_phase - 1]
    
    @property
    def bayes_numerator_for_favored_haplotype(self):
        '''
        P(aligned_segment|haplotype_i)P(haplotype_i)
        Bayes numerator. likelihood * prior
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.calculate_likelihood_of_read_given_haplotype_i(
                    self.max_phase - 1
                    ) * self.prior_probability_for_haplotype_i(self.max_phase - 1)
        # if self.likelihood_for_haplotype_i(i) and self.prior_probability_for_haplotype_i(i):
    
    @property
    def log_likelihood_ratio_for_favored_haplotype_vs_not_favored_haplotype(self):
        '''

        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            if self.total_probability_of_read_given_haplotypes and self.bayes_numerator_for_haplotype_i(
                    self.max_phase - 1
                    ):
                return math.log10(self.bayes_numerator_for_favored_haplotype) - math.log10(
                        sum(
                                [self.bayes_numerator_for_haplotype_i(_i - 1) for _i in
                                 range(1, self.ploidy_phase_set + 1) if
                                 _i - 1 != self.max_phase - 1]
                                )
                        )
    
    @property
    def posterior_probability_for_favored_haplotype(self):
        '''
        # posterior_probability_haplotype_i = P(haplotype_i|aligned_segment)

        # aligned_segment.set_tag(tag = 'fp', value = str(phased_read.posterior_probability_for_haplotype_i(c)), value_type='Z',
        replace=True) # aligned_segment.set_tag(tag = 'pp', value = str(phased_read.posterior_probability_for_haplotype_i(int(
        aligned_segment.get_tag('oa')))), value_type='Z', replace=True)


        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            if self.total_probability_of_read_given_haplotypes and self.bayes_numerator_for_haplotype_i(
                    self.max_phase - 1
                    ):
                return self.bayes_numerator_for_haplotype_i(
                        self.max_phase - 1
                        ) / self.total_probability_of_read_given_haplotypes
    
    @property
    def log_posterior_probability_for_favored_haplotype(self):
        '''
        posterior_probability_haplotype_i = P(haplotype_i|aligned_segment)
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            if self.total_probability_of_read_given_haplotypes and self.bayes_numerator_for_haplotype_i(
                    self.max_phase - 1
                    ):
                return math.log10(self.bayes_numerator_for_haplotype_i(self.max_phase - 1)) - math.log10(
                        self.total_probability_of_read_given_haplotypes
                        )
    
    def bayes_numerator_for_haplotype_i(self, i):
        '''
        P(aligned_segment|haplotype_i)P(haplotype_i)
        Bayes numerator. likelihood * prior
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.calculate_likelihood_of_read_given_haplotype_i(i - 1) * self.prior_probability_for_haplotype_i(
                    i - 1
                    )
        # if self.likelihood_for_haplotype_i(i) and self.prior_probability_for_haplotype_i(i):
    
    def log_likelihood_ratio_for_haplotype_i_vs_not_haplotype_i(self, i):
        '''

        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            if self.total_probability_of_read_given_haplotypes and self.bayes_numerator_for_haplotype_i(i - 1):
                return math.log10(self.bayes_numerator_for_haplotype_i(i - 1)) - math.log10(
                        sum(
                                [self.bayes_numerator_for_haplotype_i(_i - 1) for _i in
                                 range(1, self.ploidy_phase_set + 1) if
                                 _i - 1 != i - 1]
                                )
                        )
    
    def posterior_probability_for_haplotype_i(self, i):
        '''
        # posterior_probability_haplotype_i = P(haplotype_i|aligned_segment)

        # aligned_segment.set_tag(tag = 'fp', value = str(phased_read.posterior_probability_for_haplotype_i(c)), value_type='Z',
        replace=True) # aligned_segment.set_tag(tag = 'pp', value = str(phased_read.posterior_probability_for_haplotype_i(int(
        aligned_segment.get_tag('oa')))), value_type='Z', replace=True)


        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            if self.total_probability_of_read_given_haplotypes and self.bayes_numerator_for_haplotype_i(i - 1):
                return self.bayes_numerator_for_haplotype_i(i - 1) / self.total_probability_of_read_given_haplotypes
    
    def log_posterior_probability_for_haplotype_i(self, i):
        '''
        posterior_probability_haplotype_i = P(haplotype_i|aligned_segment)
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            if self.total_probability_of_read_given_haplotypes and self.bayes_numerator_for_haplotype_i(i - 1):
                return math.log10(self.bayes_numerator_for_haplotype_i(i - 1)) - math.log10(
                        self.total_probability_of_read_given_haplotypes
                        )
    
    @property
    def total_probability_of_read_given_haplotypes(self):
        '''
        total_probability_of_read_given_haplotypes = sum(P(aligned_segment|haplotype_i)P(haplotype_i)) for i = 1,...,ploidy Our
        model assumes that the haplotypes listed in the VCF file are the ground truth molecular composition of the
        populations from which these reads were sampled from physically.
        '''
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return sum([self.bayes_numerator_for_haplotype_i(i) for i in range(1, self.ploidy_phase_set + 1)])
