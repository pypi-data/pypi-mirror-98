from ctypes import c_double, Array
from threading import Lock
from typing import Optional, Collection, List, Any

import numpy as np
from ase import Atoms
from ase.calculators.calculator import Calculator, all_changes
from lammps import PyLammps  # type:ignore
from narupatools.ase.constraints.observer import ASEObserver
from narupatools.ase.converter import KCALMOL_TO_EV


class LAMMPSCalculator(Calculator):
    """
    ASE Calculator that interfaces with a given LAMMPS simulation, by updating positions and reading energy/forces.
    """
    implemented_properties = ['energy', 'forces']

    def __init__(self, lammps: PyLammps, atoms: Optional[Atoms] = None, **kwargs: Any):
        super().__init__(**kwargs)
        self._lammps = lammps
        self._lammps_lock = Lock()
        self._atoms = atoms
        self._identify_units()

        if atoms is not None:
            _position_observer = ASEObserver()
            _position_observer.on_set_positions.add_callback(self._mark_positions_as_dirty)
            atoms.constraints.append(_position_observer)
        self._positions_dirty = True

        self._energy = 0.0
        if self._atoms is None:
            self._forces = np.zeros((3, 0))
        else:
            self._forces = np.zeros((3, len(self._atoms)))

    def calculate(self, atoms: Optional[Atoms] = None,
                  properties: Collection[str] = ('energy', 'forces'),
                  system_changes: List[str] = all_changes) -> None:
        if self._atoms is not None and (atoms is self._atoms or atoms is None):
            if self._positions_dirty:
                with self._lammps_lock:
                    self._set_positions(self._atoms.get_positions())
                    self._run_system()
                    self._energy = self._extract_potential_energy()
                    self._forces = self._extract_forces()
                self._positions_dirty = False
        elif atoms is not None:
            with self._lammps_lock:
                self._set_positions(atoms.get_positions())
                self._run_system()
                self._energy = self._extract_potential_energy()
                self._forces = self._extract_forces()
            self._positions_dirty = True
        else:
            raise ValueError("No atoms provided")

        self.results['energy'] = self._energy
        self.results['forces'] = self._forces

    def _mark_positions_as_dirty(self, **kwargs: Any) -> None:
        self._positions_dirty = True

    def _identify_units(self) -> None:
        unit_system = self._lammps.system.units
        if unit_system == "real":
            self._lammps_to_ase_energy = KCALMOL_TO_EV  # Kcal/mole to eV
            self._lammps_to_ase_forces = KCALMOL_TO_EV  # Kcal/mole/A to eV/A
            self._ase_to_lammps_positions = 1  # angstroms to angstroms
        else:
            raise ValueError(f"Unsupported unit system {unit_system}")

    def _extract_potential_energy(self) -> float:
        energy_lammps: float = self._lammps.lmp.extract_compute("thermo_pe", 0, 0)
        return energy_lammps * self._lammps_to_ase_energy

    def _run_system(self) -> None:
        self._lammps.run(1)

    def _extract_forces(self) -> np.ndarray:
        forces_raw = self._lammps.lmp.gather_atoms("f", 1, 3)
        return np.array(forces_raw).reshape((-1, 3)) * self._lammps_to_ase_forces  # type: ignore

    def _set_positions(self, positions: np.ndarray) -> None:
        n_atoms = self._lammps.lmp.get_natoms()
        self._lammps.lmp.scatter_atoms("x", 1, 3, to_ctypes(positions * self._ase_to_lammps_positions, n_atoms))


def to_ctypes(array: np.ndarray, natoms: int) -> Array:
    n3 = 3 * natoms
    x = (n3 * c_double)()
    for i, f in enumerate(array.flat):
        x[i] = f  # type: ignore
    return x
