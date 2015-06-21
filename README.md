# A twin ion mass spec pipeline based on [Ruffus](http://www.ruffus.org.uk/)

Author: Bernie Pope (bjpope@unimelb.edu.au)

twin ion is based on the [Ruffus](http://www.ruffus.org.uk/) library for writing bioinformatics pipelines. Its features include:

 * Job submission on a cluster using DRMAA (currently only tested with SLURM).
 * Job dependency calculation and checkpointing.
 * Pipeline can be displayed as a flowchart.
 * Re-running a pipeline will start from the most up-to-date stage. It will not redo previously completed tasks.

## License

3 Clause BSD License. See LICENSE.txt in source repository.

## Installation

#### External dependencies

`twin ion` depends on the following programs and libraries:

 * [python](https://www.python.org/download/releases/2.7.5/) (version 2.7.5)
 * [DRMAA](http://www.drmaa.org/) for submitting jobs to the cluster (it uses the Python wrapper to do this). 
   You need to install your own `libdrama.so` for your local job submission system. There are versions
   available for common schedulers such as Torque/PBS, [SLURM](http://apps.man.poznan.pl/trac/slurm-drmaa) and so on.
 * [openms](http://open-ms.sourceforge.net/) (version 2.0.0)

You will need to install these dependencies yourself.

I recommend using a virtual environment:

```
cd /place/to/install
virtualenv twin_ion_dev 
source twin_ion_dev/bin/activate
pip install -U https://github.com/bjpop/twin_ion
```

If you don't want to use a virtual environment then you can just install with pip:

```
pip install -U https://github.com/bjpop/twin_ion
```

## Worked example

The `example` directory in the source distribution contains a small dataset to illustrate the use of the pipeline.

#### Get a copy of the source distribution

```
cd /path/to/test/directory
git clone https://github.com/bjpop/twin_ion
```

#### Install `twin ion` as described above


#### Tell Python where your DRMAA library is 

For example (this will depend on your local settings):

```
export DRMAA_LIBRARY_PATH=/usr/local/slurm_drmaa/1.0.7-gcc/lib/libdrmaa.so
```

#### Run `twin ion` and ask it what it will do next

```
twin_ion -n --verbose 3
```

#### Generate a flowchart diagram

```
twin_ion --flowchart pipeline_flow.png 
```

#### Run the pipeline

```
twin_ion --use_threads --log_file pipeline.log --jobs 2 --verbose 3
```

## Usage

You can get a summary of the command line arguments like so:

```
twin_ion -h
usage: twin_ion [-h] [--verbose [VERBOSE]] [-L FILE] [-T JOBNAME] [-j N]
              [--use_threads] [-n] [--touch_files_only] [--recreate_database]
              [--checksum_file_name FILE] [--flowchart FILE]
              [--key_legend_in_graph] [--draw_graph_horizontally]
              [--flowchart_format FORMAT] [--forced_tasks JOBNAME]
              [--config CONFIG] [--jobscripts JOBSCRIPTS] [--version]

Twin ion pipeline

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Pipeline configuration file in YAML format, defaults
                        to pipeline.config
  --jobscripts JOBSCRIPTS
                        Directory to store cluster job scripts created by the
                        pipeline, defaults to jobscripts
  --version             show program's version number and exit

Common options:
  --verbose [VERBOSE], -v [VERBOSE]
                        Print more verbose messages for each additional
                        verbose level.
  -L FILE, --log_file FILE
                        Name and path of log file

pipeline arguments:
  -T JOBNAME, --target_tasks JOBNAME
                        Target task(s) of pipeline.
  -j N, --jobs N        Allow N jobs (commands) to run simultaneously.
  --use_threads         Use multiple threads rather than processes. Needs
                        --jobs N with N > 1
  -n, --just_print      Don't actually run any commands; just print the
                        pipeline.
  --touch_files_only    Don't actually run the pipeline; just 'touch' the
                        output for each task to make them appear up to date.
  --recreate_database   Don't actually run the pipeline; just recreate the
                        checksum database.
  --checksum_file_name FILE
                        Path of the checksum file.
  --flowchart FILE      Don't run any commands; just print pipeline as a
                        flowchart.
  --key_legend_in_graph
                        Print out legend and key for dependency graph.
  --draw_graph_horizontally
                        Draw horizontal dependency graph.
  --flowchart_format FORMAT
                        format of dependency graph file. Can be 'pdf', 'svg',
                        'svgz' (Structured Vector Graphics), 'pdf', 'png'
                        'jpg' (bitmap graphics) etc
  --forced_tasks JOBNAME
                        Task(s) which will be included even if they are up to
                        date.
```

## Configuration file

You must supply a configuration file for the pipeline in YAML format.

Here is an example:

```
# Default settings for the pipeline stages.
# These can be overridden in the stage settings below.

defaults:
    # Number of CPU cores to use for the task
    cores: 1
    # Maximum memory in gigabytes for a cluster job
    mem: 4
    # VLSCI account for quota
    account: VR0002
    queue: main
    # Maximum allowed running time on the cluster in Hours:Minutes
    walltime: '1:00'
    # Load modules for running a command on the cluster.
    modules: 
    # Run on the local machine (where the pipeline is run)
    # instead of on the cluster. False means run on the cluster.
    local: False

# Stage-specific settings. These override the defaults above.
# Each stage must have a unique name. This name will be used in
# the pipeine to find the settings for the stage.

stages:
    # When writing an peak file, all spectra are resampled with a new sampling rate. The number of spectra does not change.
    resample:
        cores: 1
        rate: '0.01'
        walltime: '0:10'
        mem: 8
        modules:
            - 'openms-gcc/2.0.0'
        
    # Filter noise using Savitzky Golay
    noise_filter_sgolay:
        cores: 1
        walltime: '0:10'
        mem: 8
        modules:
            - 'openms-gcc/2.0.0'

    # Executes the top-hat filter to remove the baseline of an MS experiment.  
    baseline_filter:
        cores: 1
        walltime: '0:10'
        mem: 8
        modules:
            - 'openms-gcc/2.0.0'
    
    # Executes the peak picking with high_res algorithm.  
    peak_picker_hires:
        cores: 1
        walltime: '0:10'
        mem: 8
        modules:
            - 'openms-gcc/2.0.0'
    
    # Feature finder in centroided data
    feature_finder_centroid:
        cores: 1
        walltime: '0:10'
        mem: 8
        modules:
            - 'openms-gcc/2.0.0'

# The input MZML files.
mzml:
   - testing.mzML
```
