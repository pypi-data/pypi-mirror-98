import os
import pytest
import numpy as np
from phonopy.structure.atoms import PhonopyAtoms
from phonopy.structure.cells import (
    get_supercell, get_primitive, TrimmedCell,
    compute_permutation_for_rotation, compute_all_sg_permutations)
from phonopy.interface.phonopy_yaml import read_cell_yaml

data_dir = os.path.dirname(os.path.abspath(__file__))


def test_compute_permutation_sno2(ph_sno2):
    _test_compute_permutation(ph_sno2)


def test_compute_permutation_tio2(ph_tio2):
    _test_compute_permutation(ph_tio2)


def test_compute_permutation_nacl(ph_nacl):
    _test_compute_permutation(ph_nacl)


def _test_compute_permutation(ph):
    symmetry = ph.primitive_symmetry
    ppos = ph.primitive.scaled_positions
    plat = ph.primitive.cell.T
    symprec = symmetry.tolerance
    rots = symmetry.get_symmetry_operations()['rotations']
    trans = symmetry.get_symmetry_operations()['translations']
    perms = compute_all_sg_permutations(ppos, rots, trans, plat, symprec)
    for i, (r, t) in enumerate(zip(rots, trans)):
        ppos_rot = np.dot(ppos, r.T) + t
        perm = compute_permutation_for_rotation(ppos, ppos_rot, plat, symprec)
        np.testing.assert_array_equal(perms[i], perm)
        diff = ppos[perm] - ppos_rot
        diff -= np.rint(diff)
        assert ((np.dot(diff, plat) ** 2).sum(axis=1) < symprec).all()


@pytest.mark.parametrize("nosnf", [True, False])
def test_get_supercell_convcell_sio2(convcell_sio2, nosnf, helper_methods):
    _test_get_supercell_convcell_sio2(convcell_sio2,
                                      helper_methods,
                                      is_old_style=nosnf)


@pytest.mark.parametrize("nosnf", [True, False])
def test_get_supercell_primcell_si(primcell_si, nosnf, helper_methods):
    _test_get_supercell_primcell_si(primcell_si,
                                    helper_methods,
                                    is_old_style=nosnf)


def test_get_supercell_nacl_snf(convcell_nacl, helper_methods):
    cell = convcell_nacl
    smat = [[-1, 1, 1], [1, -1, 1], [1, 1, -1]]
    scell = get_supercell(cell, smat, is_old_style=True)
    scell_snf = get_supercell(cell, smat, is_old_style=False)
    helper_methods.compare_cells(scell, scell_snf)


def _test_get_supercell_convcell_sio2(convcell_sio2,
                                      helper_methods,
                                      is_old_style=True):
    smat = np.diag([1, 2, 3])
    fname = "SiO2-123.yaml"
    scell = get_supercell(convcell_sio2, smat, is_old_style=is_old_style)
    cell_ref = read_cell_yaml(os.path.join(data_dir, fname))
    if is_old_style is True:
        helper_methods.compare_cells_with_order(scell, cell_ref)
    else:
        helper_methods.compare_cells(scell, cell_ref)


def _test_get_supercell_primcell_si(primcell_si,
                                    helper_methods,
                                    is_old_style=True):
    smat = [[-1, 1, 1], [1, -1, 1], [1, 1, -1]]
    fname = "Si-conv.yaml"
    scell = get_supercell(primcell_si, smat, is_old_style=is_old_style)
    cell_ref = read_cell_yaml(os.path.join(data_dir, fname))
    if is_old_style is True:
        helper_methods.compare_cells_with_order(scell, cell_ref)
    else:
        helper_methods.compare_cells(scell, cell_ref)


def test_get_primitive_convcell_nacl(convcell_nacl,
                                     primcell_nacl,
                                     helper_methods):
    pcell = get_primitive(convcell_nacl, [[0, 0.5, 0.5],
                                          [0.5, 0, 0.5],
                                          [0.5, 0.5, 0]])
    helper_methods.compare_cells_with_order(pcell, primcell_nacl)


def test_TrimmedCell(convcell_nacl, helper_methods):
    pmat = [[0, 0.5, 0.5],
            [0.5, 0, 0.5],
            [0.5, 0.5, 0]]
    smat2 = np.eye(3, dtype='intc') * 2
    pmat2 = np.dot(np.linalg.inv(smat2), pmat)
    smat3 = np.eye(3, dtype='intc') * 3
    pmat3 = np.dot(np.linalg.inv(smat3), pmat)

    cell = convcell_nacl
    scell2 = get_supercell(cell, smat2)
    scell3 = get_supercell(cell, smat3)
    n = len(scell3) // 2
    # swap first and last half of atomic order
    indices = [i + n for i in range(n)] + list(range(n))
    scell3_swap = PhonopyAtoms(
        cell=scell3.cell,
        scaled_positions=scell3.scaled_positions[indices],
        numbers=scell3.numbers[indices])
    tcell2 = TrimmedCell(pmat2, scell2)
    tcell3 = TrimmedCell(pmat3, scell3_swap,
                         positions_to_reorder=tcell2.scaled_positions)
    helper_methods.compare_cells_with_order(tcell2, tcell3)
