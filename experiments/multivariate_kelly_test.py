import unittest
import numpy as np

# Assuming your kellyReturns function is defined in a file named kelly.py
from multivariate_kelly import kellyCriterion, kellyGradient, kellyHessian

class TestKellyReturns(unittest.TestCase):
    def test_1D_2states(self):
        for p in np.arange(0, 1, 0.01):
            for x in np.arange(0, 1, 0.01):
                R = np.array([-1, 1])
                P = np.array([p, 1 - p])
                X = np.array([x])

                expected_return = kellyCriterion(R, P, X)
                expected_manual = np.sum(P * np.log(1 + R * X[0]))
                self.assertAlmostEqual(expected_return, expected_manual)
                
                expected_gradient = kellyGradient(R, P, X)[0]
                expected_manual = np.sum(P * R / (1 + R * X[0]))
                self.assertAlmostEqual(expected_gradient, expected_manual)
                
                expected_hessian = kellyHessian(R, P, X)[0][0]
                expected_manual = -np.sum(P * R ** 2 / (1 + R * X[0]) ** 2)
                self.assertAlmostEqual(expected_hessian, expected_manual)

    
    def test_1D_3states(self):
        for p1 in np.arange(0, 1, 0.05):
            for p2 in np.arange(0, 1 - p1, 0.05):
                for x in np.arange(0, 1, 0.01):
                    R = np.array([-1, 0, 1])
                    P = np.array([p1, p2, 1 - p1 - p2])
                    X = np.array([x])

                    expected_return = kellyCriterion(R, P, X)
                    expected_manual = np.sum(P * np.log(1 + R * X[0]))
                    self.assertAlmostEqual(expected_return, expected_manual)
                    
                    expected_gradient = kellyGradient(R, P, X)[0]
                    expected_manual = np.sum(P * R / (1 + R * X[0]))
                    self.assertAlmostEqual(expected_gradient, expected_manual)
                    
                    expected_hessian = kellyHessian(R, P, X)[0][0]
                    expected_manual = -np.sum(P * R ** 2 / (1 + R * X[0]) ** 2)
                    self.assertAlmostEqual(expected_hessian, expected_manual)


    def test_2D_2states(self):
        for p1 in np.arange(0, 1, 0.1):
            for p2 in np.arange(0, 1 - p1, 0.1):
                for p3 in np.arange(0, 1 - p1 - p2, 0.1):
                    for x in np.arange(0, 1, 0.1):
                        for y in np.arange(0, 1 - x, 0.1):
                            R = np.array([-1, 1])
                            P = np.array([p1, p2, p3, 1 - p1 - p2 - p3]).reshape(R.size, R.size)
                            X = np.array([x, y])

                            expected_return = kellyCriterion(R, P, X)
                            expected_manual = P[0][0] * np.log(1 + R[0] * X[0] + R[0] * X[1]) + \
                                            P[0][1] * np.log(1 + R[0] * X[0] + R[1] * X[1]) + \
                                            P[1][0] * np.log(1 + R[1] * X[0] + R[0] * X[1]) + \
                                            P[1][1] * np.log(1 + R[1] * X[0] + R[1] * X[1])
                            self.assertAlmostEqual(expected_return, expected_manual)
                            
                            expected_gradient = kellyGradient(R, P, X)
                            expected_dx = P[0][0] * R[0] / (1 + R[0] * X[0] + R[0] * X[1]) + \
                                          P[0][1] * R[0] / (1 + R[0] * X[0] + R[1] * X[1]) + \
                                          P[1][0] * R[1] / (1 + R[1] * X[0] + R[0] * X[1]) + \
                                          P[1][1] * R[1] / (1 + R[1] * X[0] + R[1] * X[1])
                            self.assertAlmostEqual(expected_gradient[0], expected_dx)
                            expected_dy = P[0][0] * R[0] / (1 + R[0] * X[0] + R[0] * X[1]) + \
                                          P[0][1] * R[1] / (1 + R[0] * X[0] + R[1] * X[1]) + \
                                          P[1][0] * R[0] / (1 + R[1] * X[0] + R[0] * X[1]) + \
                                          P[1][1] * R[1] / (1 + R[1] * X[0] + R[1] * X[1])
                            self.assertAlmostEqual(expected_gradient[1], expected_dy)

                            expected_hessian = kellyHessian(R, P, X)
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
                            self.assertAlmostEqual(expected_hessian[0][0], expected_dxx)
                            self.assertAlmostEqual(expected_hessian[0][1], expected_dxy)
                            self.assertAlmostEqual(expected_hessian[1][0], expected_dxy)
                            self.assertAlmostEqual(expected_hessian[1][1], expected_dyy)
                        

                
                    


if __name__ == '__main__':
    unittest.main()