"""
cluster.py
==========
Helper function to run LklCom on a cluster/coomputing farm
"""

import argparse
import yaml
import os

import likelihood_combiner as lklcom
from likelihood_combiner.combiner import combiner
from likelihood_combiner.utils import *

__all__ = [
    'run_cluster'
]

def run_cluster(settings,
        channel,
        input=None,
        output=None,
        simulation=0):
    """
    Run LklCom on a cluster/coomputing farm.

    Parameters
    ----------
    settings: dict
        settings of the combination, following the minimum skeleton (see example config file for more documentation):
        {'Data' : {'buildin_j_factors': `string`, 'j_nuisance': `boolean`, 'simulations': `int`},
        'Configuration' : {'channels': `numpy.ndarray of type string`, 'sources': `numpy.ndarray of type string`, 'collaborations': `dictionary`}}
    channel: `string`
        name of the channel.
    input: `string`
        path to the input file or directory.
    output: `string`
        path to the output directory.
    simulation: `int`
        number of the simulation.
    """
    
    if input is None:
        input = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../input/mock_data.hdf5"))
    if output is None:
        output = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output/"))
    
    if not os.path.exists(output):
        os.makedirs(output)
        
    # Initializing of the LklCom jfactor class
    if 'buildin_j_factors' not in settings['Data']:
        settings['Data']['buildin_j_factors'] = "Custom"

    if settings['Data']['buildin_j_factors'] == "GeringerSameth":
        LklCom_jfactor_class = lklcom.jfactor.GeringerSameth(sources=settings['Configuration']['sources'],
                                                    collaborations=settings['Configuration']['collaborations'],
                                                    combination_data=input,
                                                    jnuisance=settings['Data']['j_nuisance'])
    elif settings['Data']['buildin_j_factors'] == "Bonnivard":
        LklCom_jfactor_class = lklcom.jfactor.Bonnivard(sources=settings['Configuration']['sources'],
                                                    collaborations=settings['Configuration']['collaborations'],
                                                    combination_data=input,
                                                    jnuisance=settings['Data']['j_nuisance'])
    else:
        LklCom_jfactor_class = lklcom.jfactor.Custom(logJ=settings['Data']['custom_logJ'],
                                                    DlogJ=settings['Data']['custom_DlogJ'],
                                                    jnuisance=settings['Data']['j_nuisance'])

    # Initializing of the LklCom reader class
    if input.endswith(".h5") or input.endswith(".hdf5"):
        LklCom_reader_class = lklcom.reader.LklCom_hdf5(channel=channel,
                                                        LklCom_jfactor_class=LklCom_jfactor_class)
    if os.path.isdir(input):
        LklCom_reader_class = lklcom.reader.LklCom_txtdir(channel=channel,
                                                        LklCom_jfactor_class=LklCom_jfactor_class)

    # Constructing in the the sigmav range and spacing
    sigmav_range = get_sigmav_range()
    # Overwriting from the settings, if provided.
    if "sigmav_min" in settings['Data'] and "sigmav_max" in settings['Data'] and "sigmav_nPoints" in settings['Data']:
        sigmav_range = get_sigmav_range(settings['Data']['sigmav_min'], settings['Data']['sigmav_max'], settings['Data']['sigmav_nPoints'], 3)
        
    combiner(sigmav_range=sigmav_range,
            LklCom_reader_class=LklCom_reader_class,
            output=output,
            simulations=[simulation])
    return
