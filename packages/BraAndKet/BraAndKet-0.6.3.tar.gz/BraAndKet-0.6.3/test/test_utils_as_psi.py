import bnk
import unittest
import numpy as np


class TensorAsPsiAndRhoTestCase(unittest.TestCase):
    def test_as_psi(self):
        space = bnk.KetSpace(3)

        tensor = space.eigenstate(1) + space.eigenstate(0) + 2 * space.eigenstate(2)

        psi = tensor.as_psi()

        self.assertAlmostEqual(np.sum(np.square(psi.values)), 1)

    def test_as_rho(self):
        space = bnk.KetSpace(3)

        tensor = space.eigenstate(1) + space.eigenstate(0) + 2 * space.eigenstate(2)
        tensor = tensor @ tensor.ct

        rho = tensor.as_rho()

        self.assertAlmostEqual(float(rho.trace()), 1)
