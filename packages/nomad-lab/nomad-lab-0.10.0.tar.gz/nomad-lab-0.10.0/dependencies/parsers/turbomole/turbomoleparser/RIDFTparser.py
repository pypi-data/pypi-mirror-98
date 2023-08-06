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

"""This module constructs the parser for the RIDFT module from TurboMole"""

import logging
import re
from nomadcore.simple_parser import SimpleMatcher as SM
from turbomoleparser.TurbomoleCommon import RE_FLOAT
import turbomoleparser.TurbomoleCommon as Common

logger = logging.getLogger("nomad.turbomoleParser")


class RIDFTparser(object):

    def __init__(self, context, key="ridft"):
        context[key] = self
        self.__context = context
        self.__backend = None

    def purge_data(self):
        pass

    def set_backend(self, backend):
        self.__backend = backend

    def build_parser(self):
        references = SM(r"\s{5,}[^+ ].+$",
                        name="references",
                        coverageIgnore=True,
                        repeats=True,
                        )
        header = SM(r"\s*r i d f t\s*$",
                    name="Credits",
                    coverageIgnore=True,
                    subMatchers=[references],
                    endReStr=r"\s*\+-+\+"
                    )

        auxbasis_title = r"\s*RI-J\s+AUXILIARY\s+BASIS\s+SET\s+information\s*:\s*$"

        sub_matchers = [
            header,
            self.__context["method"].build_uhf_matcher(),
            self.__context["geo"].build_qm_geometry_matcher(),
            self.__context["geo"].build_orbital_basis_matcher(),
            self.__context["geo"].build_auxiliary_basis_matcher(),
            # TODO: verify if this auxbasis title is used in official releases
            self.__context["geo"].build_auxiliary_basis_matcher(auxbasis_title),
            self.__context["orbitals"].build_ir_rep_matcher(),
            self.__context["method"].build_dft_functional_matcher(),
            self.__context["embedding"].build_embedding_matcher(),
            self.__build_scf_cycle_matcher(),
            self.__context["method"].build_total_energy_matcher(),
            self.__context["orbitals"].build_eigenstate_matcher(),
        ]

        return self.__context.build_module_matcher("ridft", sub_matchers, "RIDFT",
                                                   self.__context["method"].add_default_functional)

    def __build_scf_cycle_matcher(self):

        class PreviousCycle(object):
            energy = None

        def compute_energy_difference(backend, groups):
            backend.addRealValue("energy_total_scf_iteration", float(groups[0]), unit="hartree")
            backend.addRealValue("x_turbomole_energy_1electron_scf_iteration",
                                 float(groups[1]), unit="hartree")
            backend.addRealValue("x_turbomole_energy_2electron_scf_iteration",
                                 float(groups[2]), unit="hartree")
            # TODO: clarify the meaning of the "NORM[dD(SAO)]" and "TOL" columns in the output
            if PreviousCycle.energy:
                backend.addRealValue("energy_change_scf_iteration",
                                 float(groups[0]) - PreviousCycle.energy, unit="hartree")
            PreviousCycle.energy = float(groups[0])

        def store_damping(backend, groups):
            backend.addRealValue("x_turbomole_damping_scf_iteration",
                                 1.0 / (1.0 + float(groups[0])))

        total_energy = SM(r"\s*[0-9]+\s+("+RE_FLOAT+")\s+("+RE_FLOAT+")\s+("+RE_FLOAT+")"
                          "\s+("+RE_FLOAT+")\s+("+RE_FLOAT+")",
                          name="SCF E total",
                          startReAction=compute_energy_difference,
                          required=True
                          )

        xc_energy = SM(r"\s*Exc =\s*(?P<energy_XC_scf_iteration__hartree>"+RE_FLOAT+")"
                       r"\s+Coul =\s*(?P<energy_electrostatic_scf_iteration__hartree>"+RE_FLOAT+")",
                       name="SCF E xc+coul",
                       )
        damping = SM(r"\s*current damping\s*=\s*("+RE_FLOAT+")\s*$",
                     name="SCF damping",
                     startReAction=store_damping
                     )

        # TODO: identify the units of these norms
        norm_diis = SM(r"\s*Norm of current diis error:\s*(?P<x_turbomole_norm_diis_scf_iteration>"
                       + RE_FLOAT+r")\s*$",
                       name="SCF norm DIIS"
                       )
        norm_fia_block = SM(r"\s*max. resid. norm for Fia\-block\s*=\s*(?P"
                            r"<x_turbomole_norm_fia_scf_iteration>"+RE_FLOAT+")\s*for orbital\s+"
                            r"(?P<x_turbomole_norm_fia_orbital_scf_iteration>[0-9]+[a-z][0-9'\"]?"
                            r"\s*(?:alpha|beta)?)\s*$",
                            name="SCF norm Fia"
                            )
        norm_fock = SM(r"\s*max. resid. fock norm\s*=\s*(?P"
                       r"<x_turbomole_norm_fock_scf_iteration>"+RE_FLOAT+")\s*for orbital\s+"
                       r"(?P<x_turbomole_norm_fock_orbital_scf_iteration>[0-9]+[a-z][0-9'\"]?"
                       r"\s*(?:alpha|beta)?)\s*$",
                       name="SCF norm Fock"
                       )

        scf_iteration = SM("\s*ITERATION\s+ENERGY\s+1e-ENERGY\s+2e-ENERGY\s+"
                           "RMS\[dD\(SAO\)\]\s+TOL",
                           name="SCF iteration",
                           repeats=True,
                           sections=["section_scf_iteration"],
                           subMatchers=[
                               total_energy,
                               xc_energy,
                               damping,
                               norm_diis,
                               norm_fia_block,
                               norm_fock
                           ]
                           )

        return SM(r"\s*Starting SCF iterations\s*$",
                  name="HF/DFT SCF",
                  required=True,
                  subMatchers=[
                      scf_iteration
                  ]
                  )
