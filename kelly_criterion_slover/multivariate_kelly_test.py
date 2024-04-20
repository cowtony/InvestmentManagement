import unittest
import numpy as np

# Assuming your kellyReturns function is defined in a file named kelly.py
from multivariate_kelly import *

class TestKellyReturns(unittest.TestCase):
    def test_1D_2states(self):
        for p in np.arange(0, 1, 0.01):
            for x in np.arange(0, 1, 0.01):
                R = np.array([-1, 1])
                P = np.array([p, 1 - p])
                X = np.array([x])

                value, gradient, hessian = kellyCalculation(R, P, X)
                expected_value = np.sum(P * np.log(1 + R * X[0]))
                self.assertAlmostEqual(value, expected_value)
                
                # expected_gradient = kellyGradient(R, P, X)[0]
                expected_gradient = np.sum(P * R / (1 + R * X[0]))
                self.assertAlmostEqual(gradient[0], expected_gradient)
                
                # expected_hessian = kellyHessian(R, P, X)[0][0]
                expected_hessian = -np.sum(P * R ** 2 / (1 + R * X[0]) ** 2)
                self.assertAlmostEqual(hessian[0][0], expected_hessian)

    
    def test_1D_3states(self):
        for p1 in np.arange(0, 1, 0.05):
            for p2 in np.arange(0, 1 - p1, 0.05):
                for x in np.arange(0, 1, 0.01):
                    R = np.array([-1, 0, 1])
                    P = np.array([p1, p2, 1 - p1 - p2])
                    X = np.array([x])

                    value, gradient, hessian = kellyCalculation(R, P, X)
                    expected_value = np.sum(P * np.log(1 + R * X[0]))
                    self.assertAlmostEqual(value, expected_value)
                    
                    # expected_gradient = kellyGradient(R, P, X)[0]
                    expected_gradient = np.sum(P * R / (1 + R * X[0]))
                    self.assertAlmostEqual(gradient[0], expected_gradient)
                    
                    # expected_hessian = kellyHessian(R, P, X)[0][0]
                    expected_hessian = -np.sum(P * R ** 2 / (1 + R * X[0]) ** 2)
                    self.assertAlmostEqual(hessian[0][0], expected_hessian)


    def test_2D_2states(self):
        for p1 in np.arange(0, 1, 0.1):
            for p2 in np.arange(0, 1 - p1, 0.1):
                for p3 in np.arange(0, 1 - p1 - p2, 0.1):
                    for x in np.arange(0, 1, 0.1):
                        for y in np.arange(0, 1 - x, 0.1):
                            R = np.array([-1, 1])
                            P = np.array([p1, p2, p3, 1 - p1 - p2 - p3]).reshape(R.size, R.size)
                            X = np.array([x, y])

                            value, gradient, hessian = kellyCalculation(R, P, X)
                            expected_value = P[0][0] * np.log(1 + R[0] * X[0] + R[0] * X[1]) + \
                                             P[0][1] * np.log(1 + R[0] * X[0] + R[1] * X[1]) + \
                                             P[1][0] * np.log(1 + R[1] * X[0] + R[0] * X[1]) + \
                                             P[1][1] * np.log(1 + R[1] * X[0] + R[1] * X[1])
                            self.assertAlmostEqual(value, expected_value)
                            
                            # expected_gradient = kellyGradient(R, P, X)
                            expected_dx = P[0][0] * R[0] / (1 + R[0] * X[0] + R[0] * X[1]) + \
                                          P[0][1] * R[0] / (1 + R[0] * X[0] + R[1] * X[1]) + \
                                          P[1][0] * R[1] / (1 + R[1] * X[0] + R[0] * X[1]) + \
                                          P[1][1] * R[1] / (1 + R[1] * X[0] + R[1] * X[1])
                            self.assertAlmostEqual(gradient[0], expected_dx)
                            expected_dy = P[0][0] * R[0] / (1 + R[0] * X[0] + R[0] * X[1]) + \
                                          P[0][1] * R[1] / (1 + R[0] * X[0] + R[1] * X[1]) + \
                                          P[1][0] * R[0] / (1 + R[1] * X[0] + R[0] * X[1]) + \
                                          P[1][1] * R[1] / (1 + R[1] * X[0] + R[1] * X[1])
                            self.assertAlmostEqual(gradient[1], expected_dy)

                            # expected_hessian = kellyHessian(R, P, X)
                            expected_dxx = - P[0][0] * R[0] ** 2 / (1 + R[0] * X[0] + R[0] * X[1]) ** 2 \
                                           - P[0][1] * R[0] ** 2 / (1 + R[0] * X[0] + R[1] * X[1]) ** 2 \
                                           - P[1][0] * R[1] ** 2 / (1 + R[1] * X[0] + R[0] * X[1]) ** 2 \
                                           - P[1][1] * R[1] ** 2 / (1 + R[1] * X[0] + R[1] * X[1]) ** 2
                            expected_dyy = - P[0][0] * R[0] ** 2 / (1 + R[0] * X[0] + R[0] * X[1]) ** 2 \
                                           - P[0][1] * R[1] ** 2 / (1 + R[0] * X[0] + R[1] * X[1]) ** 2 \
                                           - P[1][0] * R[0] ** 2 / (1 + R[1] * X[0] + R[0] * X[1]) ** 2 \
                                           - P[1][1] * R[1] ** 2 / (1 + R[1] * X[0] + R[1] * X[1]) ** 2
                            expected_dxy = - P[0][0] * R[0] * R[0] / (1 + R[0] * X[0] + R[0] * X[1]) ** 2 \
                                           - P[0][1] * R[0] * R[1] / (1 + R[0] * X[0] + R[1] * X[1]) ** 2 \
                                           - P[1][0] * R[1] * R[0] / (1 + R[1] * X[0] + R[0] * X[1]) ** 2 \
                                           - P[1][1] * R[1] * R[1] / (1 + R[1] * X[0] + R[1] * X[1]) ** 2
                            self.assertAlmostEqual(hessian[0][0], expected_dxx)
                            self.assertAlmostEqual(hessian[0][1], expected_dxy)
                            self.assertAlmostEqual(hessian[1][0], expected_dxy)
                            self.assertAlmostEqual(hessian[1][1], expected_dyy)
                        

    def assertSequenceAlmostEqual(self, seq1, seq2, places=7, msg=None):
        self.assertEqual(len(seq1), len(seq2), msg=f"Lengths are different: {len(seq1)} and {len(seq2)}")
        for a, b in zip(seq1, seq2):
            self.assertAlmostEqual(a, b, places=places, msg=msg)


    def test_random_input_across_functions(self):
        for _ in range(100):
            R_RANGE = np.random.randint(2, 10)
            DIMENSION = np.random.randint(2, 12 - R_RANGE)
            print(f'Testing for r_range {R_RANGE}, dimension {DIMENSION}')
            R = np.linspace(-1, 1, R_RANGE)
            P = np.random.dirichlet(np.ones(R.size ** DIMENSION)).reshape((R.size,) * DIMENSION)
            X = np.random.rand(DIMENSION)
            X = X / (np.sum(X) * 1.5)  # Normalize X to ensure the sum is less than 1

            # Get results from the new combined function
            value, gradient, hessian = kellyCalculation(R, P, X)

            # Get results from the old separate functions
            old_value = kellyValueV1(R, P, X)
            old_gradient = kellyGradientV1(R, P, X)
            old_hessian = kellyHessianV1(R, P, X)

            # Compare the results using unittest assertions
            self.assertAlmostEqual(value, old_value, places=7, msg=f'{value}, {old_value}')
            self.assertSequenceAlmostEqual(gradient, old_gradient, places=7, msg=f'{gradient}, {old_gradient}')
            self.assertSequenceAlmostEqual(hessian.flatten(), old_hessian.flatten(), places=7, msg="Hessian does not match")

                    


if __name__ == '__main__':
    unittest.main()