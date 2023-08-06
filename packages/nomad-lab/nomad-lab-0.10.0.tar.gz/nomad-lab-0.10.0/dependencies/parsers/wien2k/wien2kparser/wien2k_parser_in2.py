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
import os, sys, json


################################################################
# This is the subparser for the WIEN2k input file (.in2)
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


class Wien2kIn2Context(object):
    """context for wien2k In2 parser"""

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

    def onClose_section_method(self, backend, gIndex, section):
        smearing_kind = section['x_wien2k_smearing_kind'][0]
        if smearing_kind is not None:
            if 'TETRA' in smearing_kind:
                backend.addValue('smearing_kind', 'tetrahedra')
            elif 'TEMP' in smearing_kind:
                backend.addValue('smearing_kind', 'fermi')
            elif 'GAUSS' in smearing_kind:
                backend.addValue('smearing_kind', 'gaussian')

# description of the input
def buildIn2Matchers():
    return SM(
    name = 'root',
    weak = True,
    startReStr = "",
        sections = ["section_run", "section_method"],
    subMatchers = [
#        SM(name = 'systemName',
#          startReStr = r"(?P<x_wien2k_system_nameIn>.*)"),
        SM(r"\s*(?P<x_wien2k_in2_switch>[A-Z]+)\s*.*"),
        SM(r"\s*(?P<x_wien2k_in2_emin>[-+0-9.]+)\s*(?P<x_wien2k_in2_ne>[-+0-9.]+)\s*(?P<x_wien2k_in2_espermin>[-+0-9.]+)\s*(?P<x_wien2k_in2_esper0>[-+0-9.]+)\s*.*"),
        SM(r"\s*(?P<x_wien2k_smearing_kind>[A-Z]+)\s*\s*(?P<smearing_width__rydberg>[-+0-9.]+)\s*.*"),
        SM(r"\s*(?P<x_wien2k_in2_gmax>[-+0-9.]+)\s*GMAX")

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
                               'section_method': CachingLvl
                              }
    return cachingLevelForMetaName

# loading metadata from nomad-meta-info/meta_info/nomad_meta_info/fhiaims.nomadmetainfo.json
