import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import numpy as np
from phonopy import Phonopy
from phonopy.phonon.moment import PhononMoment
from phonopy.interface.vasp import read_vasp
from phonopy.file_IO import parse_FORCE_SETS, parse_BORN
import os

data_dir = os.path.dirname(os.path.abspath(__file__))

result_full_range = """
1.000000  1.000000  1.000000
 4.063222  4.236805  3.889623
17.935854 19.412820 16.458756
 1.000000  1.000000  1.000000
 3.530039  3.621065  3.451029
12.557720 13.205191 11.995720
"""


class TestMoment(unittest.TestCase):
    def setUp(self):
        self._cell = read_vasp(os.path.join(data_dir, "..", "POSCAR_NaCl"))

    def tearDown(self):
        pass

    def test_moment(self):
        data = np.loadtxt(StringIO(result_full_range), dtype='double')

        phonon = self._get_phonon(self._cell)
        moment = phonon.run_mesh([13, 13, 13],
                                 with_eigenvectors=True,
                                 is_mesh_symmetry=False)
        num_atom = phonon.get_primitive().get_number_of_atoms()
        q = phonon.mesh.qpoints
        w = phonon.mesh.weights
        f = phonon.mesh.frequencies
        e = phonon.mesh.eigenvectors
        vals = np.zeros((6, num_atom + 1), dtype='double')

        moment = PhononMoment(f, w)
        for i in range(3):
            moment.run(order=i)
            vals[i, 0] = moment.get_moment()
            self.assertTrue(np.abs(moment.get_moment() - data[i, 0]) < 1e-5)

        moment = PhononMoment(f, w, eigenvectors=e)
        for i in range(3):
            moment.run(order=i)
            moms = moment.get_moment()
            vals[i, 1:] = moms
            self.assertTrue((np.abs(moms - data[i, 1:]) < 1e-5).all())

        moment = PhononMoment(f, w)
        moment.set_frequency_range(freq_min=3, freq_max=4)
        for i in range(3):
            moment.run(order=i)
            vals[i + 3, 0] = moment.get_moment()
            self.assertTrue(
                np.abs(moment.get_moment() - data[i + 3, 0]) < 1e-5)

        moment = PhononMoment(f, w, eigenvectors=e)
        moment.set_frequency_range(freq_min=3, freq_max=4)
        for i in range(3):
            moment.run(order=i)
            moms = moment.get_moment()
            vals[i + 3, 1:] = moms
            self.assertTrue((np.abs(moms - data[i + 3, 1:]) < 1e-5).all())

        # self._show(vals)

    def _show(self, vals):
        for v in vals:
            print(("%9.6f " * len(v)) % tuple(v))

    def _get_phonon(self, cell):
        phonon = Phonopy(cell,
                         np.diag([2, 2, 2]),
                         primitive_matrix=[[0, 0.5, 0.5],
                                           [0.5, 0, 0.5],
                                           [0.5, 0.5, 0]])
        filename = os.path.join(data_dir, "..", "FORCE_SETS_NaCl")
        force_sets = parse_FORCE_SETS(filename=filename)
        phonon.set_displacement_dataset(force_sets)
        phonon.produce_force_constants()
        filename_born = os.path.join(data_dir, "..", "BORN_NaCl")
        nac_params = parse_BORN(phonon.get_primitive(), filename=filename_born)
        phonon.set_nac_params(nac_params)

        return phonon


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMoment)
    unittest.TextTestRunner(verbosity=2).run(suite)
