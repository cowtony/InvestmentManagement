import numpy as np
from multivariate_kelly import kellyCalculation


def newtonsIteration(R, P, X):
    _, gradient, hessian = kellyCalculation(R, P, X)
    
    # Check if the Hessian is singular
    if np.linalg.cond(hessian) > 1 / np.finfo(hessian.dtype).eps:
        raise np.linalg.LinAlgError('Hessian is singular or near-singular.')
    
    # Compute the search direction using the inverse of the Hessian
    search_direction = np.linalg.solve(hessian, -gradient)
    
    # Line search to find an appropriate step size (alpha)
    alpha = 1  # This can be replaced with a line search algorithm
    
    return np.clip(X + alpha * search_direction, 0, 1)

    

def newtonsMethod(R, P, X=None, tolerance=1e-6, max_iterations=100):
    """
    Find the investment fractions that maximize the expected logarithmic return using Newton's method.

    :param R: 1D array representing the range of returns.
    :param P: N-dimensional matrix representing the joint probability distribution.
    :param initial_X: Initial guess for the investment fractions.
    :param tolerance: Convergence tolerance for the optimization.
    :param max_iterations: Maximum number of iterations to perform.
    :return: Investment fractions that approximate the maximum expected return.
    """
    if X is None:
        X = np.zeros(P.ndim)

    X_points = [X]
    for iteration in range(max_iterations):
        X_points.append(newtonsIteration(R, P, X_points[-1]))
        
        # Check for convergence
        if np.linalg.norm(X_points[-1] - X_points[-2]) < tolerance:
            print(f"Converged in {iteration} iterations.")
            return X_points
    
    print("Maximum number of iterations reached without convergence.")
    return X_points
