import os
import numpy as np
import pint
import logging
import phonopy
from phonopy.units import THzToEv

from phonopyparser.fhiaims_io import Control, read_forces_aims
from phonopyparser.phonopy_properties import PhononProperties
from phonopyparser.FHIaims import read_aims

import nomad.config
from nomad.datamodel.metainfo.common_dft import Run, System, SystemToSystemRefs, Method,\
    SingleConfigurationCalculation, KBand, KBandSegment, Dos, FrameSequence,\
    ThermodynamicalProperties, SamplingMethod, Workflow, Phonon, CalculationToCalculationRefs

from nomad.parsing.parser import FairdiParser
from .metainfo import m_env


class PhonopyParser(FairdiParser):
    def __init__(self, **kwargs):
        super().__init__(
            name='parsers/phonopy', code_name='Phonopy', code_homepage='https://phonopy.github.io/phonopy/',
            mainfile_name_re=(r'(.*/phonopy-FHI-aims-displacement-0*1/control.in$)|(.*/phonon.yaml)')
        )
        self._kwargs = kwargs

    @property
    def mainfile(self):
        return self._filepath

    @mainfile.setter
    def mainfile(self, val):
        self._phonopy_obj = None
        self.references = []
        self._filepath = os.path.abspath(val)

    @property
    def calculator(self):
        if 'control.in' in self.mainfile:
            return 'fhi-aims'
        elif 'phonon.yaml' in self.mainfile:
            return 'vasp'

    @property
    def phonopy_obj(self):
        if self._phonopy_obj is None:
            if self.calculator == 'fhi-aims':
                self._build_phonopy_object_fhi_aims()
            elif self.calculator == 'vasp':
                self._build_phonopy_object_vasp()
        return self._phonopy_obj

    def _build_phonopy_object_vasp(self):
        cwd = os.getcwd()
        os.chdir(os.path.dirname(self.mainfile))

        phonopy_obj = phonopy.load('phonon.yaml')
        os.chdir(cwd)

        self._phonopy_obj = phonopy_obj

    def _build_phonopy_object_fhi_aims(self):
        cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.dirname(self.mainfile)))
        cell_obj = read_aims("geometry.in")
        control = Control()
        if (len(control.phonon["supercell"]) == 3):
            supercell_matrix = np.diag(control.phonon["supercell"])
        elif (len(control.phonon["supercell"]) == 9):
            supercell_matrix = np.array(control.phonon["supercell"]).reshape(3, 3)
        displacement = control.phonon["displacement"]
        sym = control.phonon["symmetry_thresh"]

        try:
            set_of_forces, phonopy_obj, relative_paths = read_forces_aims(
                cell_obj, supercell_matrix, displacement, sym)
        except Exception:
            self.logger.error("Error generating phonopy object.")
            set_of_forces = []
            phonopy_obj = None
            relative_paths = []

        prep_path = self.mainfile.split("phonopy-FHI-aims-displacement-")
        # Try to resolve references as paths relative to the upload root.
        try:
            for path in relative_paths:
                abs_path = "%s%s" % (prep_path[0], path)
                rel_path = abs_path.split(nomad.config.fs.staging + "/")[1].split("/", 3)[3]
                self.references.append(rel_path)
        except Exception:
            self.logger.warn("Could not resolve path to a referenced calculation within the upload.")

        os.chdir(cwd)

        if set_of_forces:
            phonopy_obj.set_forces(set_of_forces)
            phonopy_obj.produce_force_constants()

        self._phonopy_obj = phonopy_obj

    def parse_bandstructure(self):
        freqs, bands, bands_labels = self.properties.get_bandstructure()

        # convert THz to eV
        freqs = freqs * THzToEv

        # convert eV to J
        freqs = pint.Quantity(freqs, 'eV').to('joules').magnitude

        sec_scc = self.archive.section_run[0].section_single_configuration_calculation[0]

        sec_k_band = sec_scc.m_create(KBand)
        sec_k_band.band_structure_kind = 'vibrational'

        for i in range(len(freqs)):
            freq = np.expand_dims(freqs[i], axis=0)
            sec_k_band_segment = sec_k_band.m_create(KBandSegment)
            sec_k_band_segment.band_energies = freq
            sec_k_band_segment.band_k_points = bands[i]
            sec_k_band_segment.band_segm_labels = bands_labels[i]

    def parse_dos(self):
        f, dos = self.properties.get_dos()

        # To match the shape given in meta data another dimension is added to the
        # array (spin degress of fredom is 1)
        dos = np.expand_dims(dos, axis=0)

        # convert THz to eV to Joules
        f = f * THzToEv
        f = pint.Quantity(f, 'eV').to('joules').magnitude

        sec_scc = self.archive.section_run[0].section_single_configuration_calculation[0]
        sec_dos = sec_scc.m_create(Dos)
        sec_dos.dos_kind = 'vibrational'
        sec_dos.dos_values = dos
        sec_dos.dos_energies = f

    def parse_thermodynamical_properties(self):
        T, fe, _, cv = self.properties.get_thermodynamical_properties()

        n_atoms = len(self.phonopy_obj.unitcell)
        n_atoms_supercell = len(self.phonopy_obj.supercell)

        fe = fe / n_atoms

        # The thermodynamic properties are reported by phonopy for the base
        # system. Since the values in the metainfo are stored per the referenced
        # system, we need to multiple by the size factor between the base system
        # and the supersystem used in the calculations.
        cv = cv * (n_atoms_supercell / n_atoms)

        # convert to SI units
        fe = pint.Quantity(fe, 'eV').to('joules').magnitude

        cv = pint.Quantity(cv, 'eV/K').to('joules/K').magnitude

        sec_run = self.archive.section_run[0]
        sec_scc = sec_run.section_single_configuration_calculation

        sec_frame_sequence = sec_run.m_create(FrameSequence)
        sec_frame_sequence.frame_sequence_local_frames_ref = sec_scc

        sec_thermo_prop = sec_frame_sequence.m_create(ThermodynamicalProperties)
        sec_thermo_prop.thermodynamical_property_temperature = T
        sec_thermo_prop.vibrational_free_energy_at_constant_volume = fe
        sec_thermo_prop.thermodynamical_property_heat_capacity_C_v = cv

        sec_sampling_method = sec_run.m_create(SamplingMethod)
        sec_sampling_method.sampling_method = 'taylor_expansion'
        sec_sampling_method.sampling_method_expansion_order = 2

        sec_frame_sequence.frame_sequence_to_sampling_ref = sec_sampling_method

    def parse_ref(self):
        sec_scc = self.archive.section_run[0].section_single_configuration_calculation[0]
        for ref in self.references:
            sec_calc_refs = sec_scc.m_create(CalculationToCalculationRefs)
            sec_calc_refs.calculation_to_calculation_kind = 'source_calculation'
            sec_calc_refs.calculation_to_calculation_external_url = ref

    def parse(self, filepath, archive, logger, **kwargs):
        self.mainfile = filepath
        self.archive = archive
        self.logger = logger if logger is not None else logging
        self._kwargs.update(kwargs)

        self._metainfo_env = m_env

        sec_run = self.archive.m_create(Run)
        sec_run.program_name = 'Phonopy'
        sec_run.program_version = phonopy.__version__

        phonopy_obj = self.phonopy_obj

        pbc = np.array((1, 1, 1), bool)

        unit_cell = self.phonopy_obj.unitcell.get_cell()
        unit_pos = self.phonopy_obj.unitcell.get_positions()
        unit_sym = np.array(self.phonopy_obj.unitcell.get_chemical_symbols())

        super_cell = self.phonopy_obj.supercell.get_cell()
        super_pos = self.phonopy_obj.supercell.get_positions()
        super_sym = np.array(self.phonopy_obj.supercell.get_chemical_symbols())

        unit_cell = pint.Quantity(unit_cell, 'angstrom').to('meter').magnitude
        unit_pos = pint.Quantity(unit_pos, 'angstrom').to('meter').magnitude

        super_cell = pint.Quantity(super_cell, 'angstrom').to('meter').magnitude
        super_pos = pint.Quantity(super_pos, 'angstrom').to('meter').magnitude

        displacement = np.linalg.norm(phonopy_obj.displacements[0][1:])
        displacement = pint.Quantity(displacement, 'angstrom').to('meter').magnitude

        supercell_matrix = phonopy_obj.supercell_matrix
        sym_tol = phonopy_obj.symmetry.tolerance

        sec_system_unit = sec_run.m_create(System)
        sec_system_unit.configuration_periodic_dimensions = pbc
        sec_system_unit.atom_labels = unit_sym
        sec_system_unit.atom_positions = unit_pos
        sec_system_unit.simulation_cell = unit_cell

        sec_system = sec_run.m_create(System)
        sec_system_to_system_refs = sec_system.m_create(SystemToSystemRefs)
        sec_system_to_system_refs.system_to_system_kind = 'subsystem'
        sec_system_to_system_refs.system_to_system_ref = sec_system_unit
        sec_system.configuration_periodic_dimensions = pbc
        sec_system.atom_labels = super_sym
        sec_system.atom_positions = super_pos
        sec_system.simulation_cell = super_cell
        sec_system.SC_matrix = supercell_matrix
        sec_system.x_phonopy_original_system_ref = sec_system_unit

        sec_method = sec_run.m_create(Method)
        # TODO I put this so as to have a recognizable section method, but metainfo
        # should be expanded to include phonon related method parameters
        sec_method.electronic_structure_method = 'DFT'
        sec_method.x_phonopy_symprec = sym_tol
        sec_method.x_phonopy_displacement = displacement

        try:
            force_constants = phonopy_obj.get_force_constants()
            force_constants = pint.Quantity(force_constants, 'eV/(angstrom**2)').to('eV/(m**2)').magnitude
        except Exception:
            self.logger.error('Error producing force constants.')
            return

        sec_scc = sec_run.m_create(SingleConfigurationCalculation)
        sec_scc.single_configuration_calculation_to_system_ref = sec_system
        sec_scc.single_configuration_to_calculation_method_ref = sec_method
        sec_scc.hessian_matrix = force_constants

        self.properties = PhononProperties(self.phonopy_obj, self.logger, **self._kwargs)

        self.parse_bandstructure()
        self.parse_dos()
        self.parse_thermodynamical_properties()
        self.parse_ref()

        sec_workflow = self.archive.m_create(Workflow)
        sec_workflow.workflow_type = 'phonon'
        sec_phonon = sec_workflow.m_create(Phonon)
        sec_phonon.force_calculator = self.calculator
        vol = np.dot(unit_cell[0], np.cross(unit_cell[1], unit_cell[2]))
        sec_phonon.mesh_density = np.prod(self.properties.mesh) / vol
        n_imaginary = np.count_nonzero(self.properties.frequencies < 0)
        sec_phonon.n_imaginary_frequencies = n_imaginary
        if phonopy_obj.nac_params:
            sec_phonon.with_non_analytic_correction = True
