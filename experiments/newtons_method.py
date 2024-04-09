import numpy as np
from multivariate_kelly import *


def newtonsIteration(R, P, X):
    gradient = kellyGradient(R, P, X)
    hessian = kellyHessian(R, P, X)
    
    # Check if the Hessian is singular
    if np.linalg.cond(hessian) > 1 / np.finfo(hessian.dtype).eps:
        raise np.linalg.LinAlgError('Hessian is singular or near-singular.')
    
    # Compute the search direction using the inverse of the Hessian
    search_direction = np.linalg.solve(hessian, -gradient)
    
    # Line search to find an appropriate step size (alpha)
    alpha = 1  # This can be replaced with a line search algorithm
    
    return np.clip(X + alpha * search_direction, 0, 1)

    

def newtonsMethod(R, P, X=None, tolerance=1e-10, max_iterations=100):
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

    for iteration in range(max_iterations):
        # Update the investment fractions
        X_new = newtonsIteration(R, P, X)
        print(X_new, kellyCriterion(R, P, X_new))
        
        # Check for convergence
        if np.linalg.norm(X_new - X) < tolerance:
            print(f"Converged in {iteration} iterations.")
            return X_new
        
        # Update X for the next iteration
        X = X_new
    
    print("Maximum number of iterations reached without convergence.")
    return X


# Example usage:
R = np.array([-0.1, 0, 0.1])  # Range of returns
P = np.random.dirichlet(np.ones(len(R)**3))  # Example 3D joint probability distribution
P = P.reshape((len(R), len(R), len(R)))  # Reshape to a 3D matrix for this example
initial_X = np.zeros(P.ndim)  # Starting from X = 0

# Find the optimal investment fractions
optimal_X = newtonsMethod(R, P, initial_X)
print("Optimal investment fractions:", optimal_X)