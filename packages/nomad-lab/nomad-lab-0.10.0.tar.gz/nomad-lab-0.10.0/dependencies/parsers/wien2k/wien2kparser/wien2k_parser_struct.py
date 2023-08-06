#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD.
# See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from builtins import object
from nomadcore.simple_parser import mainFunction, CachingLevel
from nomadcore.simple_parser import SimpleMatcher as SM
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
import os, sys, json, logging
import numpy as np
import ase.geometry


################################################################
# This is the subparser for the main WIEN2k input file (.struct)
################################################################

# Copyright 2016-2018 Daria M. Tomecka, Fawzi Mohamed
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = "Daria M. Tomecka"
__maintainer__ = "Daria M. Tomecka"
__email__ = "tomeckadm@gmail.com;"
__date__ = "15/05/2017"


class Wien2kStructContext():
    """context for wien2k struct parser"""

    def __init__(self):
        self.parser = None

    def initialize_values(self):
        """allows to reset values if the same superContext is used to parse different files"""
        pass

    def startedParsing(self, path, parser):
        """called when parsing starts"""
        self.parser = parser
        # allows to reset values if the same superContext is used to parse different files
        self.initialize_values()


# description of the input
def buildStructureMatchers():
    return SM(
    name = 'root',
    weak = True,
    startReStr = "",
    sections = ["section_run", "section_system"],
    subMatchers = [
        SM(name = 'systemName',
           startReStr = r"(?P<x_wien2k_system_nameIn>.*)"),
        SM(r"\w+\s*LATTICE,NONEQUIV\.ATOMS.\s*(?P<x_wien2k_nonequiv_atoms>[0-9]+)"),
        SM(r"(?P<x_wien2k_calc_mode>.*)"),
       # SM(r"\s*(?P<x_wien2k_unit_cell_param_a>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*(?P<x_wien2k_unit_cell_param_b>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*(?P<x_wien2k_unit_cell_param_c>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*(?P<x_wien2k_angle_between_unit_axis_alfa>[-+0-9.eEdD]{9})\s*(?P<x_wien2k_angle_between_unit_axis_beta>[-+0-9.eEdD]{9})\s*(?P<x_wien2k_angle_between_unit_axis_gamma>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)"),
        SM(r"\s*(?P<x_wien2k_unit_cell_param_a__angstrom>[-+0-9]*\.\d{0,6}){0,10}\s*(?P<x_wien2k_unit_cell_param_b__angstrom>[-+0-9]*\.\d{0,6}){0,10}\s*(?P<x_wien2k_unit_cell_param_c__angstrom>[-+0-9]*\.\d{0,6}){0,10}\s*(?P<x_wien2k_angle_between_unit_axis_alfa>[-+]?[0-9]*\.\d{0,6}){0,10}\s*(?P<x_wien2k_angle_between_unit_axis_beta>[-+]?[0-9]*\.\d{0,6}){0,10}\s*(?P<x_wien2k_angle_between_unit_axis_gamma>[-+]?[0-9]*\.\d*)"),
        SM(r"\s*ATOM\s*[-0-9]+:\s*X=(?P<x_wien2k_atom_pos_x__angstrom>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*Y=(?P<x_wien2k_atom_pos_y__angstrom>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*Z=(?P<x_wien2k_atom_pos_z__angstrom>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)",
           repeats=True,
           sections=["x_wien2k_section_equiv_atoms"],
           subMatchers=[
               SM(r"\s*[-0-9]+:\s*X=(?P<x_wien2k_atom_pos_x__angstrom>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*Y=(?P<x_wien2k_atom_pos_y__angstrom>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*Z=(?P<x_wien2k_atom_pos_z__angstrom>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)",
                  repeats=True
              ),
    #           SM(r"\s*(?P<atom>.{10})\s*NPT=\s*(?P<NPT>[0-9]+)\s*R0=(?P<r0>[0-9.]+)\s*RMT=\s*(?P<rmt>[0-9.]+)\s*Z:\s*(?P<z>[0-9.]+)",)
               SM(r"\s*(?P<x_wien2k_atom_name>^[^\s]+)\s*NPT=\s*(?P<x_wien2k_NPT>[0-9]+)\s*R0=(?P<x_wien2k_R0>[0-9.]+)\s*RMT=\s*(?P<x_wien2k_RMT>[0-9.]+)\s*Z:\s*(?P<x_wien2k_atomic_number_Z>[0-9.]+)",)
           ]
       )
    ])

def get_cachingLevelForMetaName(metaInfoEnv, CachingLvl):
    """Sets the caching level for the metadata.

    Args:
        metaInfoEnv: metadata which is an object of the class InfoKindEnv in nomadcore.local_meta_info.py.
        CachingLvl: Sets the CachingLevel for the sections k_band, run, and single_configuration_calculation.
            This allows to run the parser without opening new sections.

    Returns:
        Dictionary with metaname as key and caching level as value.
    """
    # manually adjust caching of metadata
    cachingLevelForMetaName = {
                               'section_run': CachingLvl,
                               'section_system': CachingLvl
                              }
    cachingLevelForMetaName["x_wien2k_system_nameIn"] = CachingLevel.ForwardAndCache
    cachingLevelForMetaName["x_wien2k_section_equiv_atoms"] = CachingLevel.ForwardAndCache
    cachingLevelForMetaName["atom_labels"] = CachingLevel.ForwardAndCache
    return cachingLevelForMetaName

# loading metadata from nomad-meta-info/meta_info/nomad_meta_info/fhi_aims.nomadmetainfo.json
