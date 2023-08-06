#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
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

import numpy as np

from nomad.normalizing.normalizer import Normalizer
from nomad.datamodel import EntryArchive
from nomad.datamodel.metainfo.public import Workflow, GeometryOptimization, Phonon, Elastic,\
    MolecularDynamics


class GeometryOptimizationNormalizer(Normalizer):
    def __init__(self, entry_archive):
        super().__init__(entry_archive)

    def _to_numpy_array(self, quantity):
        return np.array(quantity.m if quantity is not None else quantity)

    def _get_geometry_optimization_type(self):
        sec_system = self.section_run.section_system
        if not sec_system:
            return

        def compare_cell(cell1, cell2):
            if (cell1 == cell2).all():
                return None
            else:
                cell1_normed = cell1 / np.linalg.norm(cell1)
                cell2_normed = cell2 / np.linalg.norm(cell2)
                if (cell1_normed == cell2_normed).all():
                    return 'cell_volume'
                else:
                    return 'cell_shape'

        if len(sec_system) < 2:
            return 'static'

        else:
            cell_init = sec_system[0].lattice_vectors
            cell_final = sec_system[-1].lattice_vectors
            if cell_init is None:
                cell_init = sec_system[0].simulation_cell
            if cell_final is None:
                cell_final = sec_system[-1].simulation_cell

            cell_init = self._to_numpy_array(cell_init)
            cell_final = self._to_numpy_array(cell_final)

            cell_relaxation = compare_cell(cell_init, cell_final)

            if cell_relaxation is not None:
                return cell_relaxation

            atom_pos_init = self._to_numpy_array(sec_system[0].atom_positions)
            atom_pos_final = self._to_numpy_array(sec_system[-1].atom_positions)

            if (atom_pos_init == atom_pos_final).all():
                return 'static'

            return 'ionic'

    def normalize(self):
        self.section = self.entry_archive.section_workflow.section_geometry_optimization
        if not self.section:
            self.section = self.entry_archive.section_workflow.m_create(GeometryOptimization)

        if not self.section.geometry_optimization_type:
            try:
                geometry_optimization_type = self._get_geometry_optimization_type()
                self.section.geometry_optimization_type = geometry_optimization_type
            except Exception:
                pass

        scc = self.section_run.section_single_configuration_calculation
        if not self.entry_archive.section_workflow.calculation_result_ref:
            if scc:
                self.entry_archive.section_workflow.calculation_result_ref = scc[-1]

        if not self.entry_archive.section_workflow.calculations_ref:
            if scc:
                self.entry_archive.section_workflow.calculations_ref = scc

        if not self.section.optimization_steps:
            self.section.optimization_steps = len(scc)

        if not self.section.final_energy_difference:
            energies = []
            for scc in self.section_run.section_single_configuration_calculation:
                if scc.energy_total_T0:
                    energies.append(scc.energy_total_T0)

            delta_energy = None
            if len(energies) > 1:
                delta_energy = abs(energies[-1] - energies[-2])

            if delta_energy == 0.0:
                try:
                    delta_energy = abs(energies[-1] - energies[-3])
                except Exception:
                    pass

            if delta_energy:
                self.section.final_energy_difference = delta_energy

        if not self.section.final_force_maximum:
            scc = self.section_run.section_single_configuration_calculation
            max_force = None
            if scc:
                if scc[-1].atom_forces is not None:
                    forces = self._to_numpy_array(scc[-1].atom_forces)
                    max_force = np.max(np.linalg.norm(forces, axis=1))
            if max_force is not None:
                self.section.final_force_maximum = max_force


class PhononNormalizer(Normalizer):
    def __init__(self, entry_archive):
        super().__init__(entry_archive)

    def _get_n_imaginary_frequencies(self):
        scc = self.section_run.section_single_configuration_calculation
        if not scc:
            return
        sec_band = scc[0].section_k_band
        result = 0
        for band_segment in sec_band[0].section_k_band_segment:
            freq = band_segment.band_energies
            result += np.count_nonzero(np.array(freq) < 0)
        return result

    def normalize(self):
        self.section = self.entry_archive.section_workflow.section_phonon

        scc = self.section_run.section_single_configuration_calculation
        if not self.entry_archive.section_workflow.calculation_result_ref:
            if scc:
                self.entry_archive.section_workflow.calculation_result_ref = scc[-1]

        if not self.entry_archive.section_workflow.calculations_ref:
            if scc:
                self.entry_archive.section_workflow.calculations_ref = scc

        if not self.section:
            self.section = self.entry_archive.section_workflow.m_create(Phonon)

        if not self.section.n_imaginary_frequencies:
            # get number from bands (not complete as this is not the whole mesh)
            self.section.n_imaginary_frequencies = self._get_n_imaginary_frequencies()


class ElasticNormalizer(Normalizer):
    def __init__(self, entry_archive):
        super().__init__(entry_archive)

    def _resolve_mechanical_stability(self):
        spacegroup = self.entry_archive.section_run[-1].section_system[-1].x_elastic_space_group_number
        order = self.entry_archive.section_run[-1].section_method[-1].x_elastic_elastic_constant_order

        if spacegroup is None or order != 2:
            return

        scc = self.section_run.section_single_configuration_calculation[-1]
        c = scc.x_elastic_2nd_order_constants_matrix

        if c is None:
            return

        # see Phys. Rev B 90, 224104 (2014)
        res = False
        if spacegroup <= 2:  # Triclinic
            res = np.count_nonzero(c < 0)
        elif spacegroup <= 15:  # Monoclinic
            res = np.count_nonzero(c < 0)
        elif spacegroup <= 74:  # Orthorhombic
            res =\
                c[0][0] > 0 and c[0][0] * c[1][1] > c[0][1] ** 2 and\
                c[0][0] * c[1][1] * c[2][2] + 2 * c[0][1] * c[0][2] * c[1][2] -\
                c[0][0] * c[1][2] ** 2 - c[1][1] * c[0][2] ** 2 - c[2][2] * c[0][1] ** 2 > 0 and\
                c[3][3] > 0 and c[4][4] > 0 and c[5][5] > 0
        elif spacegroup <= 88:  # Tetragonal II
            res =\
                c[0][0] > abs(c[0][1]) and\
                2 * c[0][2] ** 2 < c[2][2] * (c[0][0] + c[0][1])
        elif spacegroup <= 142:  # Tetragonal I
            res =\
                c[0][0] > abs(c[0][1]) and\
                2 * c[0][2] ** 2 < c[2][2] * (c[0][0] + c[0][1]) and\
                c[3][3] > 0 and c[5][5] > 0
        elif spacegroup <= 148:  # rhombohedral II
            res =\
                c[0][0] > abs(c[0][1]) and c[3][3] > 0 and\
                c[0][2] ** 2 < (0.5 * c[2][2] * (c[0][0] + c[0][1])) and\
                c[0][3] ** 2 + c[0][4] ** 2 < 0.5 * c[3][3] * (c[0][0] - c[0][1])
        elif spacegroup <= 167:  # rhombohedral I
            res =\
                c[0][0] > abs(c[0][1]) and c[3][3] > 0 and\
                c[0][2] ** 2 < 0.5 * c[2][2] * (c[0][0] + c[0][1]) and\
                c[0][3] ** 2 < 0.5 * c[3][3] * (c[0][0] - c[0][1])
        elif spacegroup <= 194:  # hexagonal I
            res =\
                c[0][0] > abs(c[0][1]) and\
                2 * c[0][2] ** 2 < c[2][2] * (c[0][0] + c[0][1]) and\
                c[3][3] > 0 and c[5][5] > 0
        else:  # cubic
            res = c[0][0] - c[0][1] > 0 and c[0][0] + 2 * c[0][1] > 0 and c[3][3] > 0

        return res

    def _get_maximum_fit_error(self):
        scc = self.section_run.section_single_configuration_calculation[-1]

        max_error = 0.0
        for diagram in scc.x_elastic_section_strain_diagrams:
            if diagram.x_elastic_strain_diagram_type == 'cross-validation':
                error = np.amax(diagram.x_elastic_strain_diagram_values)
                max_error = error if error > max_error else max_error

        return max_error

    def normalize(self):
        self.section = self.entry_archive.section_workflow.section_elastic

        scc = self.section_run.section_single_configuration_calculation
        if not self.entry_archive.section_workflow.calculation_result_ref:
            if scc:
                self.entry_archive.section_workflow.calculation_result_ref = scc[-1]

        if not self.entry_archive.section_workflow.calculations_ref:
            if scc:
                self.entry_archive.section_workflow.calculations_ref = scc

        if not self.section:
            self.section = self.entry_archive.section_workflow.m_create(Elastic)

        if self.section.is_mechanically_stable is None:
            self.section.is_mechanically_stable = bool(self._resolve_mechanical_stability())

        if self.section.fitting_error_maximum is None:
            self.section.fitting_error_maximum = self._get_maximum_fit_error()


class MolecularDynamicsNormalizer(Normalizer):
    def __init__(self, entry_archive):
        super().__init__(entry_archive)

    def _is_with_thermodynamics(self):
        scc = self.section_run.section_single_configuration_calculation
        res = False
        if scc:
            res = scc[-1].temperature is not None
        return res

    def _is_with_trajectory(self):
        sec_system = self.section_run.section_system
        res = False
        if sec_system:
            res = sec_system[-1].atom_positions is not None
        return res

    def normalize(self):
        self.section = self.entry_archive.section_workflow.section_molecular_dynamics

        scc = self.section_run.section_single_configuration_calculation
        if not self.entry_archive.section_workflow.calculation_result_ref:
            if scc:
                self.entry_archive.section_workflow.calculation_result_ref = scc[-1]

        if not self.entry_archive.section_workflow.calculations_ref:
            if scc:
                self.entry_archive.section_workflow.calculations_ref = scc

        if not self.section:
            self.section = self.entry_archive.section_workflow.m_create(MolecularDynamics)

        if self.section.with_thermodynamics is None:
            self.section.with_thermodynamics = self._is_with_thermodynamics()

        if self.section.with_trajectory is None:
            self.section.with_trajectory = self._is_with_trajectory()


class WorkflowNormalizer(Normalizer):
    '''
    This normalizer performs all produces a section all data necessary for the Optimade API.
    It assumes that the :class:`SystemNormalizer` was run before.
    '''
    def __init__(self, entry_archive):
        super().__init__(entry_archive)
        self._elastic_programs = ['elastic']
        self._phonon_programs = ['phonopy']

    def _resolve_workflow_type_vasp(self):
        try:
            ibrion = self.section_run.section_method[0].x_vasp_incarOut_IBRION
        except Exception:
            ibrion = 1

        if ibrion == 0:
            workflow_type = "molecular_dynamics"
        else:
            workflow_type = "geometry_optimization"
        return workflow_type

    def _resolve_workflow_type(self):
        # first get it from section_sampling_method
        workflow_type = None
        sec_sampling_method = self.section_run.section_sampling_method
        if sec_sampling_method:
            workflow_type = sec_sampling_method[-1].sampling_method
            # some parsers e.g. turbomole outputs geometry optimization
            if workflow_type in ['geometry optimization', 'relaxation']:
                workflow_type = 'geometry_optimization'

        # resolve it from parser
        if not workflow_type:
            program_name = self.section_run.program_name
            if program_name:
                program_name = program_name.lower()

            if program_name == 'vasp':
                workflow_type = self._resolve_workflow_type_vasp()

            elif program_name == 'elastic':
                workflow_type = 'elastic'

            elif program_name == 'lammps':
                workflow_type = 'molecular_dynamics'

            elif program_name == 'phonopy':
                workflow_type = 'phonon'

        return workflow_type

    def normalize(self, logger=None) -> None:
        # Setup logger
        if logger is not None:
            self.logger = logger.bind(normalizer=self.__class__.__name__)

        # Do nothing if section_run is not present
        if self.section_run is None:
            return

        workflow_type = None
        if self.entry_archive.section_workflow:
            workflow_type = self.entry_archive.section_workflow.workflow_type

        if not workflow_type:
            workflow_type = self._resolve_workflow_type()

        if not workflow_type:
            return

        workflow = self.entry_archive.section_workflow
        if not workflow:
            workflow = self.entry_archive.m_create(Workflow)

        workflow.workflow_type = workflow_type

        if workflow.workflow_type == 'geometry_optimization':
            GeometryOptimizationNormalizer(self.entry_archive).normalize()

        elif workflow.workflow_type == 'phonon':
            PhononNormalizer(self.entry_archive).normalize()

        elif workflow.workflow_type == 'elastic':
            ElasticNormalizer(self.entry_archive).normalize()

        elif workflow.workflow_type == 'molecular_dynamics':
            MolecularDynamicsNormalizer(self.entry_archive).normalize()

        # remove the section workflow again, if the parser/normalizer could not produce a result
        if workflow.calculation_result_ref is None:
            self.entry_archive.m_remove_sub_section(EntryArchive.section_workflow, -1)
