from typing import Tuple
import numpy as np
from kelly_solver.multivariate_kelly import kellyCalculation


def project_onto_simplex(v):
    """
    Project an N-dimensional vector onto the simplex (x1 + x2 + ... + xn = 1 and each xi >= 0).
    
    :param v: An N-dimensional numpy array.
    :return: The projected vector.
    """
    if v.sum() <= 1 and np.alltrue(v >= 0):
        # If v is already in the simplex, return it
        return v
    else:
        # Sort the vector in descending order
        u = np.sort(v)[::-1]
        # Compute the cumulative sum of the sorted vector
        cssv = np.cumsum(u)
        # Find the number of elements that belong to the simplex
        rho = np.nonzero(u * np.arange(1, len(u) + 1) > (cssv - 1))[0][-1]
        # Compute the threshold theta
        theta = (cssv[rho] - 1) / (rho + 1.0)
        # Project the original vector onto the simplex
        w = np.maximum(v - theta, 0)
        return w
    
# TODO: newton's method has some problem at edge.
def newtonsIteration(X: np.ndarray, gradient: np.ndarray, hessian: np.ndarray) -> np.ndarray:
    """
    Based on the current X, calculate next X for newton method.

    :param R: 1D array representing the range of returns.
    :param P: X-dimensional matrix representing the joint probability distribution. The shape is R^X
    :param X: current investment fractions.

    :return: the value for current X, and the new X for next iteration.
    """
    # Check if the Hessian is singular
    if np.linalg.cond(hessian) > 1 / np.finfo(hessian.dtype).eps:
        raise np.linalg.LinAlgError('Hessian is singular or near-singular.')

    # Compute the search direction using the inverse of the Hessian
    search_direction = np.linalg.solve(hessian, -gradient)
    
    alpha = 1 # Line search to find an appropriate step size (alpha)
    new_X = X + alpha * search_direction  # Update the investment fractions
    new_X = np.clip(new_X, 0, 1)
    if np.sum(new_X) > 1:
        new_X /= np.sum(new_X)

    return new_X

    

def newtonsMethod(R: np.ndarray, P: np.ndarray, X=None, tolerance=1e-6, max_iterations=100, verbose=False) -> np.ndarray:
    """
    Find the investment fractions that maximize the expected logarithmic return using Newton's method.

    :param R: 1D array representing the range of returns.
    :param P: N-dimensional matrix representing the joint probability distribution.
    :param X: Initial guess for the investment fractions.
    :param tolerance: Convergence tolerance for the optimization.
    :param max_iterations: Maximum number of iterations to perform.

    :return: Investment fractions that approximate the maximum expected return.
    """
    if X is None:
        X = np.zeros(P.ndim)

    X_points = [X]
    for iteration in range(max_iterations):
        X = X_points[-1]
        value, gradient, hessian = kellyCalculation(R, P, X)
        if verbose:
            X_formatted = ", ".join(f"{x * 100:.2f}%" for x in X)
            print(f'Iteration {iteration}: Investment fraction is: {X_formatted}, Log Return is: {value:.5f}')

        next_X = newtonsIteration(X, gradient, hessian)
        X_points.append(next_X)

        # Check for convergence
        if np.linalg.norm(X - next_X) < tolerance:
            if verbose:
                print(f'Converged in {iteration} iterations.')
            return X_points
    
    if verbose:
        print('Maximum number of iterations reached without convergence.')
    return X_points
