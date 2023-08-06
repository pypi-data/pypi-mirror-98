# coding=utf-8
import math
from collections import defaultdict
from statistics import mean
from typing import Any, List

import LRphase.HeterozygousSites as HeterozygousSite


def powlaw_modified(x: object, a: object = 4, xmin: object = 2) -> object:
    """

    Args:
        x:
        a:
        xmin:

    Returns:

    """
    return ((a - 1) / xmin) * math.pow(x / xmin, -1 * a)


def _multcoeff(*args):
    '''# self.result = _multcoeff(*args)'''
    """Return the multinomial coefficient
    (n1 + n2 + ...)! / n1! / n2! / ..."""
    if not args:  # no parameters
        return 1
    # Find and store the index of the largest parameter so we can skip
    #   it (for efficiency)
    skipndx = args.index(max(args))
    newargs = args[:skipndx] + args[skipndx + 1:]
    
    result = 1
    num = args[skipndx] + 1  # a factor in the numerator
    for n in newargs:
        for den in range(1, n + 1):  # a factor in the denominator
            result = result * num // den
            num += 1
    return result


def _read_base_error_rates_from_quality_scores(gapped_alignment_positions, query_qualities):
    """# self.read_base_error_rates, self.error_rate_average_het_sites =
    self._read_base_error_rates_from_quality_scores(self.gapped_alignment_positions,
    self.aligned_segment.query_qualities) """
    
    ############ Extract base qualities for heterozygous sites in aligned_segment  ############
    
    read_base_error_rates = []
    error_rate_total_het_sites = 0
    total_het_sites_count = 0
    
    for position in gapped_alignment_positions:
        if isinstance(position, str):
            if position[0] == '-':
                read_base_error_rates.append(1)
        else:
            read_base_error_rates.append(10**(-0.1 * query_qualities[position]))
            error_rate_total_het_sites += 10**(-0.1 * query_qualities[position])
            total_het_sites_count += 1
    
    if total_het_sites_count > 0:
        error_rate_average_het_sites = error_rate_total_het_sites / total_het_sites_count
    else:
        error_rate_average_het_sites = 0
    return read_base_error_rates, error_rate_average_het_sites


def _read_bases_from_gapped_alignment(gapped_alignment_positions, query_sequence):
    """# self.read_bases = self._read_bases_from_gapped_alignment(self.gapped_alignment_positions,
    self.aligned_segment.query_sequence) """
    ############ Extract bases for heterozygous sites in aligned_segment  ############
    read_bases = []
    for position in gapped_alignment_positions:
        if isinstance(position, str):
            if position[0] == '-':
                read_bases.append('-')
        else:
            read_bases.append(query_sequence[position])
    return read_bases


def _read_base_error_rates_from_gapped_alignment(gapped_alignment_positions: object, per_base_error_rate):
    """# self.read_base_error_rates = self._read_base_error_rates_from_gapped_alignment(
    self.gapped_alignment_positions, self.per_base_error_rate) """
    read_base_error_rates = []
    # PhaseSet._estimate_per_base_error_rate()
    for position in gapped_alignment_positions:
        if isinstance(position, str):
            if position[0] == '-':
                read_base_error_rates.append(1)
        else:
            read_base_error_rates.append(per_base_error_rate)
    return read_base_error_rates


def _calculate_per_base_mismatch_rate(aligned_segment):
    """# self.per_base_mismatch_rate = self._calculate_per_base_mismatch_rate(self.aligned_segment)"""
    matches = 0
    i = 0
    for position in aligned_segment.get_aligned_pairs(with_seq = True):
        if position[1] is None:
            continue
        elif position[0] is None:
            continue
        else:
            if str(aligned_segment.query_sequence[position[0]]) == str(position[2]).upper():
                matches += 1
        i += 1
    per_base_mismatch_rate = float(1 - (matches / i))
    return per_base_mismatch_rate


def _calculate_local_per_base_mismatch_rate(aligned_segment, gapped_alignment_positions) -> object:
    """# self.read_base_error_rates, self.per_base_mismatch_rate, self.error_rate_average_het_sites =
    self._calculate_local_per_base_mismatch_rate(self.aligned_segment, self.gapped_alignment_positions)

    Args:
        aligned_segment:
        gapped_alignment_positions: """
    
    # read_base_error_rates = defaultdict(int)
    error_rate_total_het_sites = 0
    total_het_sites_count = 0
    matches = 0
    matches_alignment_query: List[int] = []
    read_base_error_rates = []
    # gapped_alignment_positions_error_rate = []
    i = 0
    for position in aligned_segment.get_aligned_pairs(with_seq = True):
        if position[1] is None:
            matches_alignment_query.append(0)
            continue
        elif position[0] is None:
            continue
        else:
            if str(aligned_segment.query_sequence[position[0]]) == str(position[2]).upper():
                matches += 1
                matches_alignment_query.append(1)
            else:
                matches_alignment_query.append(0)
        i += 1
    per_base_mismatch_rate = float(1 - (matches / i))
    
    for site in gapped_alignment_positions:
        if isinstance(site, str):
            if site[0] == '-':
                read_base_error_rates.append(1)
        else:
            try:
                read_base_error_rates.append(
                        round(
                                (2 * round(
                                        1 - (
                                                sum(matches_alignment_query[int(site) - 10:int(site) + 10]) / len(
                                                matches_alignment_query[int(site) - 10:int(site) + 10]
                                                )), 4
                                        ) + round(
                                        1 - (
                                                sum(matches_alignment_query[int(site) - 25:int(site) + 25]) / len(
                                                matches_alignment_query[int(site) - 25:int(site) + 25]
                                                )), 4
                                        ) + round(
                                        1 - (
                                                sum(matches_alignment_query[int(site) - 50:int(site) + 50]) / len(
                                                matches_alignment_query[int(site) - 50:int(site) + 50]
                                                )), 4
                                        )) / 4, 4
                                )
                        )
                error_rate_total_het_sites += round(
                        (2 * round(
                                1 - (
                                        sum(matches_alignment_query[int(site) - 10:int(site) + 10]) / len(
                                        matches_alignment_query[int(site) - 10:int(site) + 10]
                                        )), 4
                                ) + round(
                                1 - (
                                        sum(matches_alignment_query[int(site) - 25:int(site) + 25]) / len(
                                        matches_alignment_query[int(site) - 25:int(site) + 25]
                                        )), 4
                                ) + round(
                                1 - (
                                        sum(matches_alignment_query[int(site) - 50:int(site) + 50]) / len(
                                        matches_alignment_query[int(site) - 50:int(site) + 50]
                                        )), 4
                                )) / 4, 4
                        )
            except ZeroDivisionError:
                read_base_error_rates.append(per_base_mismatch_rate)
                error_rate_total_het_sites += per_base_mismatch_rate
            total_het_sites_count += 1
    
    if total_het_sites_count > 0:
        error_rate_average_het_sites = error_rate_total_het_sites / total_het_sites_count
    else:
        error_rate_average_het_sites = 0
    
    return read_base_error_rates, per_base_mismatch_rate, error_rate_average_het_sites


def _count_matches(
        read_bases: object, phased_alleles: object, read_base_error_rates: object,
        multinomial_correction: object
        ) -> object:
    """# self.log_probability_read_given_haplotype_i, self.non_matches, self.matches, self.total_hets,
    self.total_hets_analyzed, self.ploidy_phase_set = self._count_matches(self.read_bases, self.phased_alleles,
    self.read_base_error_rates, self.error_model)

    Args:
        read_bases:
        phased_alleles:
        read_base_error_rates:
        multinomial_correction:

    Returns:
        object: """
    log_probability_read_given_haplotype_i: defaultdict[Any, int] = defaultdict(int)  # log10(P(data|phase_i))
    non_matches = defaultdict(int)
    matches = defaultdict(int)
    total_hets = 0
    total_hets_analyzed = 0
    ploidy_list = []
    i = 0
    # print(read_bases, phased_alleles, read_base_error_rates, error_model)
    for read_base in read_bases:
        ploidy = len(phased_alleles[i])
        ploidy_list.append(ploidy)
        q = read_base_error_rates[i] + .001
        if not read_base == '-':
            for haplotype in range(0, ploidy):
                if len(phased_alleles[i][haplotype]) > 1:
                    continue
            total_hets_analyzed += 1
            for haplotype in range(0, ploidy):
                if read_base == phased_alleles[i][haplotype]:
                    log_probability_read_given_haplotype_i[haplotype] += math.log10(1 - q)
                    matches[haplotype] += 1
                else:
                    log_probability_read_given_haplotype_i[haplotype] += math.log10(q / 3)
                    non_matches[haplotype] += 1
        total_hets += 1
        i += 1
    if total_hets_analyzed > 0:
        ploidy_phase_set = max(ploidy_list)
    else:
        ploidy_phase_set = 0
    
    if multinomial_correction:
        haplotype: int
        for haplotype in range(0, ploidy_phase_set):
            multinomial = math.log10(_multcoeff(int(matches[haplotype]), int(non_matches[haplotype])))
            log_probability_read_given_haplotype_i[haplotype] = log_probability_read_given_haplotype_i[
                                                                    haplotype] + multinomial
    
    return log_probability_read_given_haplotype_i, non_matches, matches, total_hets, total_hets_analyzed, ploidy_phase_set


def _estimate_per_base_error_rate(aligned_segment: pysam.AlignedSegment) -> object:
    """# self.per_base_error_rate, self.error_rate_calculation = self._estimate_per_base_error_rate(
    self.aligned_segment) """
    error_rate_calculation = []
    try:
        per_base_error_rate = aligned_segment.get_tag(
                tag = 'de'
                )  # Gap-compressed per-base sequence divergence from minimap2 output
        error_rate_calculation.append('de tag')
    except LookupError:
        error_rate_calculation.append('no de tag')
        try:
            per_base_error_rate = aligned_segment.get_tag(tag = 'NM') / aligned_segment.query_alignment_length
            error_rate_calculation.append('NM tag')
        except LookupError:
            error_rate_calculation.append('no NM tag')
            try:
                per_base_error_rate = _calculate_per_base_mismatch_rate(aligned_segment)
                error_rate_calculation.append('_calculate_per_base_mismatch_rate success')
            except LookupError:
                error_rate_calculation.append('_calculate_per_base_mismatch_rate failed')
    if per_base_error_rate == 0:
        per_base_error_rate = 0.001
    return per_base_error_rate, error_rate_calculation


def _get_phased_alleles(vcf_records, sample):
    '''self.phased_alleles = self._get_phased_alleles(self.vcf_records, self.sample) '''
    return [vcf_record.samples[sample].alleles for vcf_record in vcf_records]


def _get_reference_positions(vcf_records):
    '''self.reference_positions = self._get_reference_positions(self.vcf_records) '''
    return [vcf_record.pos - 1 for vcf_record in vcf_records]


def _generate_gapped_alignment(reference_start, cigartuples, reference_positions) -> object:
    """# self.gapped_alignment_positions = self._generate_gapped_alignment(self.aligned_segment.reference_start,
    self.aligned_segment.cigartuples, self.reference_positions)

    Args:
        reference_start:
        cigartuples:
        reference_positions: """
    i: object = reference_start  # self.aligned_segment.reference_start
    j = 0
    h = 0
    gapped_alignment_positions = []
    
    if not cigartuples:
        return gapped_alignment_positions
    
    for cigartuple in cigartuples:  # self.aligned_segment.cigartuples:
        j1 = j
        if h >= len(reference_positions):
            break
        elif cigartuple[0] in [0, 7, 8]:
            i += cigartuple[1]
            j += cigartuple[1]
        elif cigartuple[0] in [1, 4]:
            j += cigartuple[1]
        elif cigartuple[0] in [2, 3]:
            i += cigartuple[1]
        while i > reference_positions[h]:
            if cigartuple[0] in [0, 7, 8]:
                gapped_alignment_positions.append(j1 + (cigartuple[1] - (i - reference_positions[h])))
                if h == len(reference_positions) - 1:
                    h += 1
                    break
            elif cigartuple[0] == 2:
                gapped_alignment_positions.append('-' + str(j1 + (cigartuple[1] - (i - reference_positions[h]))))
                if h == len(reference_positions) - 1:
                    h += 1
                    break
            if h >= len(reference_positions) - 1:
                break
            else:
                h += 1
    return gapped_alignment_positions


def _estimate_prior_probabilities(ploidy_phase_set = 2, prior_probabilities: object = None):
    if prior_probabilities is None:
        if ploidy_phase_set > 0:
            prior_probabilities = [1 / ploidy_phase_set] * ploidy_phase_set  # P(phase_i)
    return prior_probabilities


class PhaseSet:
    """

    """
    
    def __init__(
            self, phase_set, aligned_segment, vcf_records, sample, error_model = 0, error_rate_threshold = 0.01,
            multinomial_correction = True, prior_probabilities = None, liftover_converters = None
            ):
        self.aligned_segment = aligned_segment
        self.phase_set = phase_set
        self.vcf_records = vcf_records
        if liftover_converters:
            self.liftover_converters = liftover_converters
        else:
            self.liftover_converters = None
        # self.vcf_records
        self.sample = sample
        self.error_model = error_model
        self.error_rate_threshold = error_rate_threshold
        self.prior_probabilities = _estimate_prior_probabilities()
        self.multinomial_correction = multinomial_correction
        self.gapped_alignment_positions = []
        self.read_bases = []
        self.phased_alleles = []
        self.reference_positions = []
        self.max_log_likelihood_ratio = None
        self.max_phase = None
        self.phase = None
        if not self.aligned_segment.is_unmapped or self.aligned_segment.is_aligned_to_contig_not_in_vcf:
            if len(self.vcf_records) > 0:
                self.reference_positions = _get_reference_positions(self.vcf_records)
                self.phased_alleles = _get_phased_alleles(self.vcf_records, self.sample)
                self.gapped_alignment_positions = _generate_gapped_alignment(
                        self.aligned_segment.reference_start,
                        self.aligned_segment.cigartuples,
                        self.reference_positions
                        )
                self.read_bases = _read_bases_from_gapped_alignment(
                        self.gapped_alignment_positions,
                        self.aligned_segment.query_sequence
                        )
        # self.read_base_error_rates =[]
    
    def __iter__(self):
        self.HeterozygousSites = []
        self.HeterozygousSites_processed_count = 0
        # self.alignment_files_read_counts = [bam_file.mapped+bam_file.unmapped for bam_file in self.bam_files]
        return self
    
    def __next__(self):
        if self.HeterozygousSites_processed_count < len(self.vcf_records):
            Heterozygous_Site = HeterozygousSite(
                    self.vcf_records[self.HeterozygousSites_processed_count], self.sample,
                    self.aligned_segment, self.liftover_converters
                    )
            self.HeterozygousSites.append(Heterozygous_Site)
            self.HeterozygousSites_processed_count += 1
            return Heterozygous_Site
        else:
            raise StopIteration()
    
    def solve_phase(
            self, error_model: object = 0, error_rate_threshold: object = 0.01, prior_probabilities: object = None,
            multinomial_correction: object = True
            ) -> object:
        """

        Args:
            error_model:
            error_rate_threshold:
            prior_probabilities:
            multinomial_correction:

        Returns:

        """
        if prior_probabilities is None:
            prior_probabilities = self.prior_probabilities
        if not self.aligned_segment.is_unmapped or self.aligned_segment.is_aligned_to_contig_not_in_vcf:
            if len(self.gapped_alignment_positions) > 0:
                if not error_model == 5:
                    self.read_base_error_rates, self.error_rate_average_het_sites, self.per_base_mismatch_rate = self._retrieve_read_base_error_rates(
                            self.aligned_segment, self.gapped_alignment_positions, error_model
                            )
                    
                    self.log_probability_read_given_haplotype_i, self.non_matches, self.matches, self.total_hets, self.total_hets_analyzed, self.ploidy_phase_set = _count_matches(
                            self.read_bases, self.phased_alleles, self.read_base_error_rates, multinomial_correction
                            )
                    
                    self.log_likelihood_ratios, self.phase, self.max_phase, self.max_log_likelihood_ratio = _phasing_decision(
                            self.log_probability_read_given_haplotype_i, self.ploidy_phase_set, prior_probabilities,
                            error_rate_threshold, self.total_hets_analyzed
                            )
                
                elif error_model == 5:
                    haplotypes = {}
                    self.matches = 0
                    self.non_matches = 0
                    hets = [het for het in self]
                    self.total_hets = len(hets)
                    self.log_likelihood_ratios = []
                    log_likelihood_ratio = {}
                    self.ploidy_phase_set = int(mean([int(het.ploidy_het_site) for het in self]))
                    for haplotype in range(1, self.ploidy_phase_set + 1):
                        haplotypes[haplotype] = sum(
                                [het.calculate_probs(haplotype = haplotype) for het in hets if
                                 het.calculate_probs(haplotype = haplotype)]
                                )
                        # if len(haplotypes[haplotype])>0:
                        # print(haplotypes[haplotype])
                    # print('1', haplotypes)
                    # print('2', haplotypes.values())
                    # print('3',list(haplotypes.values()))
                    
                    for count, haplotype in enumerate(haplotypes):
                        self.log_likelihood_ratios.append(haplotypes[haplotype] - haplotypes[len(haplotypes) - count])
                    self.max_log_likelihood_ratio = max(self.log_likelihood_ratios)
                    self.max_phase = self.log_likelihood_ratios.index(self.max_log_likelihood_ratio) + 1
                    if self.max_log_likelihood_ratio > self.error_rate_threshold:
                        self.phase = self.max_phase
                    else:
                        self.phase = 'Unphased'
                    self.total_hets = len(hets)
                    self.total_hets_analyzed = len(hets)
                    
                    self.log_probability_read_given_haplotype_i = haplotypes
                    for het in hets:
                        het.calculate_probs()
                        if het.total_matches > 0:
                            self.matches += 1
                        elif het.total_non_matches > 0:
                            self.non_matches += 1
                    
                    # self.matches = sum([1 for het in self if het.calculate_probs()[str(self.max_phase)][
                    # het.gapped_alignment_position]['match']]) self.non_matches = sum([1 for het in self if not
                    # het.calculate_probs()[str(self.max_phase)][het.gapped_alignment_position]['match']])
                    # per_base_mismatch_rate = aligned_segment.get_tag(tag='NM')/aligned_segment.query_alignment_length
                    # read_base_error_rates = [het.read_base_quality_error_rate for het in
                    # self]self._read_base_error_rates_from_gapped_alignment(gapped_alignment_positions,
                    # per_base_mismatch_rate)
        
        self.error_model_used = error_model
        self.error_rate_threshold_used = error_rate_threshold
        self.prior_probabilities_used = prior_probabilities
        
        return  # self.max_log_likelihood_ratio, self.phase_set
    
    def _retrieve_read_base_error_rates(
            self, aligned_segment: object, gapped_alignment_positions: object,
            error_model: object
            ) -> object:
        """

        Args:
            aligned_segment:
            gapped_alignment_positions:
            error_model:

        Returns:

        """
        error_rate_average_het_sites = None
        read_base_error_rates = []
        per_base_mismatch_rate = None
        
        if not self.aligned_segment.is_unmapped or self.aligned_segment.is_aligned_to_contig_not_in_vcf:
            if len(self.gapped_alignment_positions) > 0:
                
                if error_model == 3:
                    read_base_error_rates, per_base_mismatch_rate, error_rate_average_het_sites = _calculate_local_per_base_mismatch_rate(
                            aligned_segment, gapped_alignment_positions
                            )
                
                if error_model == 2:
                    read_base_error_rates, error_rate_average_het_sites = _read_base_error_rates_from_quality_scores(
                            gapped_alignment_positions, aligned_segment.query_qualities
                            )
                    per_base_mismatch_rate = aligned_segment.get_tag(
                            tag = 'NM'
                            ) / aligned_segment.query_alignment_length
                
                if error_model == 0:
                    per_base_mismatch_rate = aligned_segment.get_tag(tag = 'de')
                    read_base_error_rates = _read_base_error_rates_from_gapped_alignment(
                            gapped_alignment_positions, per_base_mismatch_rate
                            )
                
                if error_model == 1:
                    per_base_mismatch_rate = aligned_segment.get_tag(
                            tag = 'NM'
                            ) / aligned_segment.query_alignment_length
                    read_base_error_rates = _read_base_error_rates_from_gapped_alignment(
                            gapped_alignment_positions, per_base_mismatch_rate
                            )
                
                if error_model == 4:
                    per_base_mismatch_rate = _calculate_per_base_mismatch_rate(aligned_segment)
                    read_base_error_rates = _read_base_error_rates_from_gapped_alignment(
                            gapped_alignment_positions, per_base_mismatch_rate
                            )
                
                if len(read_base_error_rates) > 0:
                    if len([error_rate for error_rate in read_base_error_rates if error_rate != 1]) > 0:
                        error_rate_average_het_sites = mean(
                                [error_rate for error_rate in read_base_error_rates if error_rate != 1]
                                )
        
        return read_base_error_rates, error_rate_average_het_sites, per_base_mismatch_rate
    
    # @staticmethod
    
    # @staticmethod
    
    # @staticmethod
    
    # @staticmethod
    
    # @staticmethod
    
    # @staticmethod
    
    # @staticmethod
    
    # @staticmethod
    
    # @staticmethod
    
    # @staticmethod
    
    # @staticmethod
    
    # @staticmethod


def _phasing_decision(
        log_probability_read_given_haplotype_i, ploidy_phase_set, prior_probabilities,
        error_rate_threshold, total_hets_analyzed
        ) -> object:
    """# self.log_likelihood_ratios, self.phase, self.max_phase, self.max_log_likelihood_ratio =
    self._phasing_decision(self.log_probability_read_given_haplotype_i, self.ploidy_phase_set,
    self.prior_probabilities, self.error_rate_threshold)

    Args:
        log_probability_read_given_haplotype_i:
        ploidy_phase_set:
        prior_probabilities:
        error_rate_threshold:
        total_hets_analyzed: """
    
    if total_hets_analyzed == 0:
        phase = 'Nonphasable'
        log_likelihood_ratios = None
        max_log_likelihood_ratio: float = None
        max_phase = 'Nonphasable'
        return log_likelihood_ratios, phase, max_phase, max_log_likelihood_ratio
    
    else:
        log_likelihood_ratios = []
        for haplotype in log_probability_read_given_haplotype_i:
            log_flag = False
            denominator = 0
            numerator = 0
            for j in range(0, ploidy_phase_set):
                if haplotype == j:
                    try:
                        numerator += math.log10(
                                (10**log_probability_read_given_haplotype_i[haplotype]) * prior_probabilities[
                                    haplotype]
                                )
                    except ValueError:
                        numerator += log_probability_read_given_haplotype_i[haplotype]
                else:
                    if log_flag:
                        if denominator == 0:
                            denominator = log_probability_read_given_haplotype_i[j]
                        elif denominator < 0 and denominator < log_probability_read_given_haplotype_i[j]:
                            denominator = log_probability_read_given_haplotype_i[j]
                    try:
                        test: float = math.log10(
                                (10**log_probability_read_given_haplotype_i[j]) * prior_probabilities[j]
                                )
                        denominator += (10**log_probability_read_given_haplotype_i[j]) * prior_probabilities[j]
                    except ValueError:
                        if denominator == 0:
                            denominator = log_probability_read_given_haplotype_i[j]
                            log_flag = True
                        elif denominator < 0 and denominator < log_probability_read_given_haplotype_i[j]:
                            denominator = log_probability_read_given_haplotype_i[j]
                            log_flag = True
                        elif denominator > 0:
                            if math.log10(denominator) < log_probability_read_given_haplotype_i[j]:
                                denominator = log_probability_read_given_haplotype_i[j]
                                log_flag = True
            if log_flag:
                log_likelihood_ratios.append(numerator - denominator)
            else:
                log_likelihood_ratios.append(numerator - math.log10(denominator))
        i = 0
        for log_likelihood_ratio in log_likelihood_ratios:
            if max(log_likelihood_ratios) == 0:
                phase = 'Unphased'
                max_phase = 0
                max_log_likelihood_ratio = 0
            elif log_likelihood_ratio == max(log_likelihood_ratios):
                max_log_likelihood_ratio = log_likelihood_ratios[i]
                max_phase = i + 1
                if error_rate_threshold >= powlaw_modified(max_log_likelihood_ratio):
                    # if max_log_likelihood_ratio >= 10 ** (math.log10((error_rate_threshold / .5491)) / -2.45):
                    phase = i + 1
                else:
                    phase = f'Unphased'
            i += 1
        
        return [log_likelihood_ratios, phase, max_phase, max_log_likelihood_ratio]
