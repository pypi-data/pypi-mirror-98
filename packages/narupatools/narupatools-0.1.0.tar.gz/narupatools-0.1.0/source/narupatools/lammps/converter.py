import ase.io
from ase.atoms import Atoms
from lammps import PyLammps  # type: ignore

from .calculator import LAMMPSCalculator


def atoms_from_lammps(lammps_input_filename: str, lammps_data_filename: str) -> Atoms:
    """
    Start up a LAMMPS instance from the given lammps input file, and return an ASE atoms object which reads data from
    the lammps data file to initialize the atom states, and uses the LAMMPS instance as a calculator to compute
    forces and energies.

    :param lammps_input_filename: A LAMMPS input filename (usually of the the form in.*).
    :param lammps_data_filename: A LAMMPS data filename (usually of the the form data.*).
    :return: An ASE Atoms object with a calculator running LAMMPS.
    """
    atoms: Atoms = ase.io.read(lammps_data_filename, format="lammps-data")  # type: ignore
    lammps = PyLammps()
    lammps.file(lammps_input_filename)
    calc = LAMMPSCalculator(lammps, atoms)
    atoms.set_calculator(calc)
    return atoms
