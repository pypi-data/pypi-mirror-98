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
import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference
)
from nomad.metainfo.legacy import LegacyDefinition

from nomad.datamodel.metainfo import public

m_package = Package(
    name='qbox_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='qbox.nomadmetainfo.json'))


class x_qbox_section_dipole(MSection):
    '''
    -
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_qbox_section_dipole'))

    x_qbox_dipole_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='bohr * elementary_charge',
        description='''
        x component of dipole
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_dipole_x'))

    x_qbox_dipole_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='bohr * elementary_charge',
        description='''
        y component of dipole
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_dipole_y'))

    x_qbox_dipole_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='bohr * elementary_charge',
        description='''
        z component of dipole
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_dipole_z'))


class x_qbox_section_efield(MSection):
    '''
    -
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_qbox_section_efield'))


class x_qbox_section_MLWF(MSection):
    '''
    -
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_qbox_section_MLWF'))

    x_qbox_geometry_MLWF_atom_positions_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        x component of atomic position in maximally localized Wannier functions(MLWF)
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_geometry_MLWF_atom_positions_x'))

    x_qbox_geometry_MLWF_atom_positions_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        y component of atomic position in maximally localized Wannier functions(MLWF)
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_geometry_MLWF_atom_positions_y'))

    x_qbox_geometry_MLWF_atom_positions_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        z component of atomic position in maximally localized Wannier functions(MLWF)
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_geometry_MLWF_atom_positions_z'))

    x_qbox_geometry_MLWF_atom_spread = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        spread of atomic position in maximally localized Wannier functions(MLWF)
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_geometry_MLWF_atom_spread'))


class x_qbox_section_stress_tensor(MSection):
    '''
    -
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_qbox_section_stress_tensor'))

    x_qbox_stress_tensor_xx = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='pascal',
        description='''
        xx component of stress tensor
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_stress_tensor_xx'))

    x_qbox_stress_tensor_xy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='pascal',
        description='''
        xy component of stress tensor
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_stress_tensor_xy'))

    x_qbox_stress_tensor_xz = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='pascal',
        description='''
        xz component of stress tensor
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_stress_tensor_xz'))

    x_qbox_stress_tensor_yy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='pascal',
        description='''
        yy component of stress tensor
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_stress_tensor_yy'))

    x_qbox_stress_tensor_yz = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='pascal',
        description='''
        yz component of stress tensor
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_stress_tensor_yz'))

    x_qbox_stress_tensor_zz = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='pascal',
        description='''
        zz component of stress tensor
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_stress_tensor_zz'))


class x_qbox_section_functionals(MSection):
    '''
    -
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_qbox_section_functionals'))

    x_qbox_functional_name = Quantity(
        type=str,
        shape=[],
        description='''
        xc function
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_functional_name'))


class x_qbox_section_xml_file(MSection):
    '''
    -
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_qbox_section_xml_file'))

    x_qbox_loading_xml_file = Quantity(
        type=str,
        shape=[],
        description='''
        The xml file used in this calculation
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_loading_xml_file'))


class section_system(public.section_system):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_system'))

    x_qbox_atom_force_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='newton',
        description='''
        x component of atomic force
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_atom_force_x'))

    x_qbox_atom_force_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='newton',
        description='''
        y component of atomic force
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_atom_force_y'))

    x_qbox_atom_force_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='newton',
        description='''
        z component of atomic force
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_atom_force_z'))

    x_qbox_geometry_atom_labels = Quantity(
        type=str,
        shape=[],
        description='''
        labels of atom
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_geometry_atom_labels'))

    x_qbox_geometry_atom_positions_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        x component of atomic position
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_geometry_atom_positions_x'))

    x_qbox_geometry_atom_positions_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        y component of atomic position
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_geometry_atom_positions_y'))

    x_qbox_geometry_atom_positions_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        z component of atomic position
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_geometry_atom_positions_z'))

    x_qbox_geometry_lattice_vector_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        x component of vector of unit cell
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_geometry_lattice_vector_x'))

    x_qbox_geometry_lattice_vector_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        y component of vector of unit cell
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_geometry_lattice_vector_y'))

    x_qbox_geometry_lattice_vector_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        z component of vector of unit cell
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_geometry_lattice_vector_z'))


class section_method(public.section_method):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_method'))

    x_qbox_atoms_dyn = Quantity(
        type=str,
        shape=[],
        description='''
        atom dynamics control variable
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_atoms_dyn'))

    x_qbox_cell_dyn = Quantity(
        type=str,
        shape=[],
        description='''
        cell dynamics control variable
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_cell_dyn'))

    x_qbox_ecut = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        plane-wave basis energy cutoff, according to qbox,  it must given in Rydberg
        units.
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_ecut'))

    x_qbox_efield_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='hartree / bohr / elementary_charge',
        description='''
        x component of efield
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_efield_x'))

    x_qbox_efield_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='hartree / bohr / elementary_charge',
        description='''
        y component of efield
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_efield_y'))

    x_qbox_efield_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='hartree / bohr / elementary_charge',
        description='''
        z component of efield
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_efield_z'))

    x_qbox_k_point_weight = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        weight k point
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_k_point_weight'))

    x_qbox_k_point_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        x component of vector of k point
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_k_point_x'))

    x_qbox_k_point_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        y component of vector of k point
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_k_point_y'))

    x_qbox_k_point_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        z component of vector of k point
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_k_point_z'))

    x_qbox_wf_dyn = Quantity(
        type=str,
        shape=[],
        description='''
        wave function dynamics control variable
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_wf_dyn'))

    x_qbox_section_functionals = SubSection(
        sub_section=SectionProxy('x_qbox_section_functionals'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_qbox_section_functionals'))

    x_qbox_section_xml_file = SubSection(
        sub_section=SectionProxy('x_qbox_section_xml_file'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_qbox_section_xml_file'))


class section_run(public.section_run):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_run'))

    x_qbox_nodename = Quantity(
        type=str,
        shape=[],
        description='''
        compute node
        ''',
        a_legacy=LegacyDefinition(name='x_qbox_nodename'))

    x_qbox_section_dipole = SubSection(
        sub_section=SectionProxy('x_qbox_section_dipole'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_qbox_section_dipole'))

    x_qbox_section_efield = SubSection(
        sub_section=SectionProxy('x_qbox_section_efield'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_qbox_section_efield'))

    x_qbox_section_MLWF = SubSection(
        sub_section=SectionProxy('x_qbox_section_MLWF'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_qbox_section_MLWF'))


class section_single_configuration_calculation(public.section_single_configuration_calculation):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_single_configuration_calculation'))

    x_qbox_section_stress_tensor = SubSection(
        sub_section=SectionProxy('x_qbox_section_stress_tensor'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_qbox_section_stress_tensor'))


m_package.__init_metainfo__()
