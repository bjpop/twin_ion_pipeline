'''
Individual stages of the pipeline implemented as functions from
input files to output files.

The run_stage function knows everything about submitting jobs and, given
the state parameter, has full access to the state of the pipeline, such 
as config, options, DRMAA and the logger.
'''

from utils import safe_make_dir
from runner import run_stage
import os

class Stages(object):
    def __init__(self, state):
        self.state = state

    def original_mzml(self, output):
        '''original mzml files'''

    def resample(self, mzml_in, mzml_out):
        '''Resample MZML file to new sampling rate'''
        cores = self.state.config.get_stage_option('resample', 'cores')
        rate = self.state.config.get_stage_option('resample', 'rate')
        command = "Resampler -sampling_rate {rate} -threads {cores} -in {mzml_in} -out {mzml_out}".format(rate=rate, cores=cores, mzml_in=mzml_in, mzml_out=mzml_out)
        run_stage(self.state, 'resample', command)

    def noise_filter_sgolay(self, mzml_in, mzml_out):
        '''Filter noise using Savitzky Golay'''
        cores = self.state.config.get_stage_option('noise_filter_sgolay', 'cores')
        command = "NoiseFilterSGolay -threads {cores} -in {mzml_in} -out {mzml_out}".format(cores=cores, mzml_in=mzml_in, mzml_out=mzml_out)
        run_stage(self.state, 'noise_filter_sgolay', command)

    def baseline_filter(self, mzml_in, mzml_out):
        '''Executes the top-hat filter to remove the baseline of an MS experiment.'''
        cores = self.state.config.get_stage_option('baseline_filter', 'cores')
        command = "BaselineFilter -threads {cores} -in {mzml_in} -out {mzml_out}".format(cores=cores, mzml_in=mzml_in, mzml_out=mzml_out)
        run_stage(self.state, 'baseline_filter', command)

    def peak_picker_hires(self, mzml_in, mzml_out):
        '''Executes the peak picking with high_res algorithm'''
        cores = self.state.config.get_stage_option('baseline_filter', 'cores')
        command = "PeakPickerHiRes -threads {cores} -in {mzml_in} -out {mzml_out}".format(cores=cores, mzml_in=mzml_in, mzml_out=mzml_out)
        run_stage(self.state, 'peak_picker_hires', command)

    def feature_finder_centroid(self, mzml_in, feature_xml_out):
        '''The feature detection application for quantitation (centroided).'''
        cores = self.state.config.get_stage_option('feature_finder_centroid', 'cores')
        command = "FeatureFinderCentroided -threads {cores} -in {mzml_in} -out {feature_out}".format(cores=cores, mzml_in=mzml_in, feature_out=feature_xml_out)
        run_stage(self.state, 'feature_finder_centroid', command)
