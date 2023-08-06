# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Analysis defaults options for DM pipelien analysis
"""
from __future__ import absolute_import, division, print_function

generic = {
    'outfile': (None, 'Path to output file.', str),
    'infile': (None, 'Path to input file.', str),
    'summaryfile': (None, 'Path to file with results summaries.', str),
}

common = {
    'ttype': (None, 'Type of target being analyzed.', str),
    'rosters': ([], 'Name of a stacking target roster.', list),
    'rosterlist': (None, 'Path to the roster list.', str),
    'target': (None, 'Name of analysis target.', str),
    'targetlist': (None, 'Path to the target list.', str),
    'config': (None, 'Path to fermipy config file.', str),
    'roi_baseline': ('fit_baseline', 'Key for roi baseline file.', str),
    'profile_file': (None, 'Path to yaml file with target profile', str),
    'spatial_models': ([], 'Types of spatial models to use', list),
    'alias_dict': (None, 'File to rename target version keys.', str),
    'sed_file': (None, 'Path to SED file.', str),
    'profiles': ([], 'List of profiles to analyze', list),
    'nsims': (-1, 'Number of simulations to run.', int),
    'dry_run': (False, 'Print commands but do not run them.', bool),
    'make_plots': (False, 'Make plots', bool),
    'non_null_src': (False, 'Zero out test source', bool),
    'do_find_src': (False, 'Add source finding step to simulated realizations', bool),

}

sims = {
    'sim': (None, 'Name of the simulation scenario.', str),
    'sims': ([], 'Names of the simulation scenario.', list),
    'sim_profile': ('default', 'Name of the profile to use for simulation.', str),
    'nsims': (20, 'Number of simulations to run.', int),
    'nsims_job': (0, 'Number of simulations to run per job.', int),
    'seed': (0, 'Seed number for first simulation.', int),
    'rand_config': (None, 'Path to config file for genaration random sky dirs', str),
    'skydirs': (None, 'Yaml file with blank sky directions.', str),
    'extracopy': ([], 'Extra files to copy', list),
    'band_sim': ('null', 'Name of the simulation scenario to use for plot bands.', str),
    'band_type': ('e2dnde_ul', 'Name of the quantity to plot in bands plots.', str),

}

collect = {
    'write_full': (False, 'Write file with full collected results', bool),
    'write_summary': (False, 'Write file with summary of collected results', bool),
}

jobs = {
    'action': ('run', 'Action to perform', str),
    'dry_run': (False, 'Print commands, but do not execute them', bool),
    'job_check_sleep': (300, 'Sleep time between checking on job status (s)', int),
    'print_update': (False, 'Print summary of job status', bool),
    'check_status_once': (False, 'Check status only once before proceeding', bool),
}
