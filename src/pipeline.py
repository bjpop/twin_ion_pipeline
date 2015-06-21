'''
Build the pipeline workflow by plumbing the stages together.
'''

from ruffus import Pipeline, suffix, formatter, add_inputs, output_from
from stages import Stages


def make_pipeline(state):
    '''Build the pipeline by constructing stages and connecting them together'''
    # Build an empty pipeline
    pipeline = Pipeline(name='twin ion')
    # Get a list of paths to all the MZML files
    mzml_files = state.config.get_option('mzml')
    # Stages are dependent on the state
    stages = Stages(state)

    # The original MZML files
    # This is a dummy stage. It is useful because it makes a node in the
    # pipeline graph, and gives the pipeline an obvious starting point.
    pipeline.originate(
        task_func=stages.original_mzml,
        name='original_mzml',
        output=mzml_files)

    pipeline.transform(
        task_func=stages.resample,
        name='resample',
        input=output_from('original_mzml'),
        filter=suffix('.mzML'),
        output='.resample.mzML')

    pipeline.transform(
        task_func=stages.noise_filter_sgolay,
        name='noise_filter_sgolay',
        input=output_from('resample'),
        filter=suffix('.resample.mzML'),
        output='.denoise.mzML')

    pipeline.transform(
        task_func=stages.baseline_filter,
        name='baseline_filter',
        input=output_from('noise_filter_sgolay'),
        filter=suffix('.denoise.mzML'),
        output='.baseline.mzML')

    pipeline.transform(
        task_func=stages.peak_picker_hires,
        name='peak_picker_hires',
        input=output_from('baseline_filter'),
        filter=suffix('.baseline.mzML'),
        output='.peaks.mzML')

    pipeline.transform(
        task_func=stages.feature_finder_centroid,
        name='feature_finder_centroid',
        input=output_from('peak_picker_hires'),
        filter=suffix('.peaks.mzML'),
        output='.featureXML')

    return pipeline
